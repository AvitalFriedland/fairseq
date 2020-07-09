#!/usr/bin/env bash


echo 'Cloning Moses github repository (for tokenization scripts)...'
git clone https://github.com/moses-smt/mosesdecoder.git

echo 'Cloning Subword NMT repository (for BPE pre-processing)...'
git clone https://github.com/rsennrich/subword-nmt.git

SCRIPTS=mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
BPEROOT=subword-nmt/subword_nmt
BPE_TOKENS=10000

src=$1
tgt=$2
lang=$src-$tgt
prep=iwslt14.tokenized.$src-$tgt
tmp=$prep/tmp
#orig=orig

mkdir -p  $tmp $prep


echo "pre-processing train data..."
for l in $src $tgt; do
    f=fixed.$l
    tok=fixed.tok.$l

    cat $f | \
    grep -v '<url>' | \
    grep -v '<talkid>' | \
    grep -v '<keywords>' | \
    sed -e 's/<title>//g' | \
    sed -e 's/<\/title>//g' | \
    sed -e 's/<description>//g' | \
    sed -e 's/<\/description>//g' | \
    perl $TOKENIZER -threads 8 -l $l > $tmp/$tok
    echo ""
done
perl $CLEAN -ratio 1.5 $tmp/fixed.tok $src $tgt $tmp/fixed.clean 1 175
for l in $src $tgt; do
    perl $LC < $tmp/fixed.clean.$l > $tmp/fixed.$l
done


# echo "pre-processing valid/test data..."
# for l in $src $tgt; do
#     for o in `ls IWSLT17.TED*.$l.xml`; do
#     fname=${o##*/}
#     f=$tmp/${fname%.*}
#     echo $o $f
#     grep '<seg id' $o | \
#         sed -e 's/<seg id="[0-9]*">\s*//g' | \
#         sed -e 's/\s*<\/seg>\s*//g' | \
#         sed -e "s/\’/\'/g" | \
#     perl $TOKENIZER -threads 8 -l $l | \
#     perl $LC > $f
#     echo ""
#     done
# done


echo "creating train, valid, test..."
for l in $src $tgt; do
    awk '{if (NR%23 == 0)  print $0; }' $tmp/fixed.$l > $tmp/valid.$l
    awk '{if (NR%23 != 0)  print $0; }' $tmp/fixed.$l > $tmp/train.$l

    # cat $tmp/IWSLT17.TED.dev2010.$lang.$l \
    #     $tmp/IWSLT17.TED.tst2010.$lang.$l \
    #     > $tmp/test.$l
done

TRAIN=$tmp/train.$lang
BPE_CODE=$prep/code
rm -f $TRAIN
for l in $src $tgt; do
    cat $tmp/train.$l >> $TRAIN
done

echo "learn_bpe.py on ${TRAIN}..."
python $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

for L in $src $tgt; do
    for f in train.$L valid.$L ; do
        echo "apply_bpe.py to ${f}..."
        python $BPEROOT/apply_bpe.py -c $BPE_CODE < $tmp/$f > $prep/$f
    done
done
