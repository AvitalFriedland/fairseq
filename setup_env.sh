#!/usr/bin/bash


username=$1
device=$2

echo "=== Creating virtualenv ===

"
#cd /vol/scratch/$username
virtualenv --system-site-packages -p python3.7 ./nlp
source ./nlp/bin/activate.csh

setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib
pip install --upgrade pip

echo "=== Installing relevant libraries ===

"


pip install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install sacrebleu sacremoses pandas tqdm


echo "=== Installing Apex ===

"
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" \
  --global-option="--deprecated_fused_adam" --global-option="--xentropy" \
  --global-option="--fast_multihead_attn" ./
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" \
  --global-option="--deprecated_fused_adam" --global-option="--xentropy" \
  --global-option="--fast_multihead_attn" ./


echo "=== Installing fairseq ===

"

#git clone https://github.com/AvitalFriedland/fairseq.git
cd fairseq
pip install --editable .


setenv CUDA_VISIBLE_DEVICES $device


echo "=== CUDA device set to ${device} ===

"

echo "Environment ready to preprocess and train"