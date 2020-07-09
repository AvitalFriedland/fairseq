import sys
import os

def split_file(top_path, lang):
    sub_files = [50,60,70,80,90,100]
    with open(f'{top_path}/train.{lang}') as f:
        lines = f.readlines()
        num_lines = len(lines)
        for sub in sub_files:
            try:
                os.mkdir(f'{top_path}/subsample_{str(sub)}/')
            except:
                pass
            with open(f'{top_path}/subsample_{str(sub)}/train.{lang}', 'w+') as new_file:
                end =int( (sub / 100.0) * num_lines)
                new_file.writelines(lines[0:end])
                print(f'wrote {new_file.name}')
def fix_pt(path):
    import glob
    os.rename(f'{path}', f'{path[:-3]}')
    for file in glob.glob(f"{path[:-3]}/subsample_*/train.pt-br"):
        print(file)
        os.rename(f'{file}', f'{file[:-3]}')
        print(file[:-3])
    for file in glob.glob(f"{path[:-3]}/*.pt-br"):
        print(file)
        os.rename(f'{file}', f'{file[:-3]}')
        print(file[:-3])
    return path[:-3]

if __name__ == "__main__":
    for _, arg in enumerate(sys.argv[1:]):
        path = str(arg)
        # path = fix_pt(path)
        try:
            src, tgt = path.split(".")[-1].split("-")
        except:
            src, tgt1, tgt2 = path.split(".")[-1].split("-")
            tgt = tgt1+'-'+tgt2
        print(f'src language {src} tgt language {tgt}')
        split_file(path, src)
        split_file(path, tgt)



