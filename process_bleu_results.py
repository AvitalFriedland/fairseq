import glob, os
import pandas as pd

results = {'train size': [i for i in range(20, 100, 20)], }
data_for_langs = {}
for file in glob.glob("bleu_*"):
    src, tgt, samplesize = file.split("_")[-1].split("-")
    samplesize = int(samplesize[:-4])
    with open(file) as f:
        line = eval(f.readlines()[0].split("|")[3])
        print(f'Results src:{src} tgt: {tgt} size: {samplesize} bleu: {line["valid_bleu"]}')
        print(f'loss: {line["valid_loss"]}')
        data_for_langs[samplesize] = line["valid_loss"]
results[f'{src}_{tgt}'] = [data_for_langs[i] for i in range(20,100,20)]
df = pd.DataFrame(results)
print(df)
