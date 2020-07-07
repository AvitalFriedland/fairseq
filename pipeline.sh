epochs=$1

for dir in iwslt14.tokenized.es-fr iwslt14.tokenized.it-pt-br iwslt14.tokenized.es-pt-br iwslt14.tokenized.ro-es iwslt14.tokenized.fr-pt-br iwslt14.tokenized.ro-fr iwslt14.tokenized.it-es iwslt14.tokenized.ro-it iwslt14.tokenized.it-fr iwslt14.tokenized.ro-pt-br; do

  src=${dir:18:2}
  tgt=${dir:21:2}

  mkdir bleu/$src-$tgt
  for num in 20 40 60 80 100; do
    echo "================================================== Preprocessing: ${src}-${tgt} ${num}================================================== "

    python preprocess.py --source-lang $src \
      --target-lang $tgt \
      --trainpref data/iwslt14.tokenized.$src-"$tgt"/subsample_$num/train --validpref data/iwslt14.tokenized.$src-"$tgt"/valid --testpref data/iwslt14.tokenized.$src-"$tgt"/test \
      --destdir data-bin/iwslt14.tokenized.$src-$tgt-$num \
      --workers 20 \
      --tensorboard-logdir log
    echo "================================================== Preprocessing: ${src}-${tgt} ${num} Done==================================================




  "
    echo "================================================== Training: ${src}-${tgt} ${num} ================================================== "
    python train.py \
      data-bin/iwslt14.tokenized.$src-$tgt-$num \
      --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
      --save-dir baseline/$src-$tgt-$num \
      --max-epoch $epochs \
      --optimizer adam --adam-betas "(0.9, 0.98)" --clip-norm 0.0 \
      --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
      --dropout 0.3 --weight-decay 0.0001 \
      --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
      --max-tokens 12288 \
      --eval-bleu \
      --eval-bleu-detok moses \
      --eval-bleu-remove-bpe --eval-bleu-print-samples \
      --best-checkpoint-metric bleu \
      --maximize-best-checkpoint-metric \
      --eval-tokenized-bleu \
      --fp16 \
      --encoder-embed-dim 256 --decoder-embed-dim 256 \
      --encoder-layers 4 --decoder-layers 4 \
      --tensorboard-logdir log \
      --log-format json | tee train_$src-$tgt-$num.log | grep valid_bleu | tee blue-$src-$tgt/bleu_$src-$tgt-$num.log

    echo "================================================== Training: ${src}-${tgt} ${num} Done================================================== "
  done
done
