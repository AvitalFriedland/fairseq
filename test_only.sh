src=$1
tgt=$2
epochs=$3

mkdir results/bleu/bleu-$src-$tgt
  for num in 20 30 40 50 60 70 80 90 100; do
    echo "================================================== Evaluating: ${src}-${tgt} ${num} ================================================== "
    fairseq-generate data-bin/iwslt14.tokenized.$src-$tgt-$num --path baseline/$src-$tgt-$num/checkpoint_best.pt \
    --batch-size 128 \
    --beam 5 --remove-bpe \
    --fp16 \
    -s $src \
    -t $tgt \
    --quiet \
    --results-path results/bleu/test_bleu-$src-$tgt-$num
    echo "================================================== Evaluating: ${src}-${tgt} ${num} Done================================================== "
done

