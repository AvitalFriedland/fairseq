src=$1
tgt=$2
epochs=$3

mkdir results/bleu/bleu-$src-$tgt
  for num in 20 30 40 ; do
    echo "================================================== Preprocessing: ${src}-${tgt} ${num}================================================== "

    python preprocess.py --source-lang $src \
      --target-lang $tgt \
      --trainpref data/iwslt14.tokenized.$src-"$tgt"/subsample_$num/train --validpref data/iwslt14.tokenized.$src-"$tgt"/valid --testpref data/iwslt14.tokenized.$src-"$tgt"/test \
      --destdir data-bin/iwslt14.tokenized.$src-$tgt-$num \
      --workers 20 \
      --joined-dictionary
    echo "================================================== Preprocessing: ${src}-${tgt} ${num} Done==================================================




  "
    echo "================================================== Training: ${src}-${tgt} ${num} ================================================== "
    python train.py \
      data-bin/iwslt14.tokenized.$src-$tgt-$num \
      --source-lang $src --target-lang $tgt \
      --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
      --save-dir baseline/$src-$tgt-$num \
      --max-epoch $epochs \
      --optimizer adam --adam-betas "(0.9, 0.98)" --clip-norm 0.0 \
      --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
      --dropout 0.3 --weight-decay 0.0001 \
      --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
      --max-tokens 8000 \
      --eval-bleu \
      --eval-bleu-detok moses \
      --eval-bleu-remove-bpe --eval-bleu-print-samples \
      --best-checkpoint-metric bleu \
      --maximize-best-checkpoint-metric \
      --eval-tokenized-bleu \
      --fp16 \
      --encoder-embed-dim 256 --decoder-embed-dim 256 \
      --encoder-layers 6 --decoder-layers 6 \
      --tensorboard-logdir log \
      --encoder-attention-heads 4 \
      --decoder-attention-heads 4\
      --share-all-embeddings \
      --save-interval 50\
      --log-format json | tee results/train_$src-$tgt-$num.log
       cat tee results/train_$src-$tgt-$num.log | grep valid_bleu | tee results/bleu/bleu-$src-$tgt/bleu_$src-$tgt-$num.log

    echo "================================================== Training: ${src}-${tgt} ${num} Done================================================== "
    echo "================================================== Evaluating: ${src}-${tgt} ${num} ================================================== "
    fairseq-generate data-bin/iwslt14.tokenized.$src-$tgt-$num --path baseline/$src-$tgt-$num/checkpoint_best.pt \
    --batch-size 128 \
    --beam 5 --remove-bpe \
    --fp16 \
    -s fr \
    -t ro \
    --log-format json | tee results/test_$src-$tgt-$num.log
    cat tee results/test_$src-$tgt-$num.log | grep BLEU4 | tee results/bleu/test_bleu_$src-$tgt-$num.log
    echo "================================================== Evaluating: ${src}-${tgt} ${num} Done================================================== "


done