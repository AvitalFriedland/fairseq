import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src', '-s', type=str, required=True
    )
    parser.add_argument(
        '--tgt', '-t', type=str, required=True
    )
    parser.add_argument(
        '--src_path', '-p', type=str, required=False, default='.'
    )
    parser.add_argument(
        '--tgt_path', '-p', type=str, required=False, default='.'
    )
    parser.add_argument('--out', '-o', type=str, required=True)
    args = parser.parse_args()
    src, tgt, src_path, tgt_path = args.src, args.tgt, args.src_path, args.tgt_path
    src_file = open(f'{src_path}/train.tags.en-{src}.{src}')
    src_data = src_file.readlines()
    tgt_file = open(f'{tgt_path}/train.tags.en-{tgt}.{tgt}')
    tgt_data = tgt_file.readlines()
    mapping_src_to_tgt = []
    max_diff = abs(len(src_data)-len(tgt_data))
    print(f'max difference between files is {max_diff}')
    with open(f'{src_path}/train.tags.en-{src}.en') as src_en:
        en_lines_src = src_en.readlines()
        with open(f'{tgt_file}/train.tags.en-{tgt}.en') as tgt_en:
            en_lines_tgt = tgt_en.readlines()
            for src_ind, line in enumerate(en_lines_src):
                tgt_ind = find_line_in_tgt(en_lines_tgt, line, index=src_ind, max_diff=max_diff)
                if src_ind%1000==0:
                    print(f'found line src {src_ind} in tgt {tgt_ind}')
                mapping_src_to_tgt.append((src_ind, tgt_ind))

    with open(f'{args.out}.{src}', 'a') as src_output:
        with open(f'{args.out}.{tgt}', 'a') as tgt_output:
            for src_index, tgt_ind in mapping_src_to_tgt:
                if tgt_ind!=-1:
                    print('writing src and tgt')
                    src_output.writelines(src_data[src_index])
                    tgt_output.writelines(tgt_data[tgt_ind])
    src_file.close()
    tgt_file.close()

def find_line_in_tgt(tgt_lines, current_line, index=0, max_diff=0):
    low_limit, high_limit = max(index-max_diff, 0), min(index+max_diff, len(tgt_lines))
    for index, line in enumerate(tgt_lines[low_limit:high_limit]):
        if line==current_line:
            return low_limit+index
    for index, line in enumerate(tgt_lines):
        if line==current_line:
            return index
    return -1




if __name__ == '__main__':
    main()