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
    --log-format json | tee results/test_$src-$tgt-$num.log
    cat tee results/test_$src-$tgt-$num.log | grep BLEU4 | tee results/bleu/test_bleu_$src-$tgt-$num.log
    echo "================================================== Evaluating: ${src}-${tgt} ${num} Done================================================== "
done