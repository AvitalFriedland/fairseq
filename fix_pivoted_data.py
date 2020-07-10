import argparse
import os
'''Proper alignment of text data that is pivoted through english.
'''
def main():
    '''Example usage:
    python3 fix_pivoted_data.py --src='es' --tgt='it' --tgt_path='data/fix_preprocessed' --src_path='data/fix_preprocessed' --o='aligned' --mode='train'

    creates the following files:
    train.tags.en-es.es_aligned
    train.tags.en-it.it_aligned

    python3 fix_pivoted_data.py --src='es' --tgt='it' --tgt_path='data/fix_preprocessed' --src_path='data/fix_preprocessed' --o='aligned' --mode='test'

    creates the following files:
    total-test-es.es.xml_aligned
    total-test-it.it.xml_aligned
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src', '-s', type=str, required=True, help='Source language. e.g. es or it'
    )
    parser.add_argument(
        '--tgt', '-t', type=str, required=True, help='Target language. e.g. es or it'
    )
    parser.add_argument(
        '--src_path', '-sp', type=str, required=False, default='.', help='Path to files of source language.'
    )
    parser.add_argument(
        '--tgt_path', '-tp', type=str, required=False, default='.', help='Path to files of target language.'
    )
    parser.add_argument('--out', '-o', type=str, required=True, help='Output tag to append at the end of the new, '
                                                                     'aligned train/test files.')
    parser.add_argument('--mode', '-m', type=str, required=True,
                        help='Mode of parsing- either train (and then train.tags is parsed) or test'
                                 '(and then IWSLT14.TED.tst2010 and others are parsed)')
    args = parser.parse_args()
    src, tgt, src_path, tgt_path, mode, output= args.src, args.tgt, \
                                                args.src_path, args.tgt_path, args.mode, args.out
    if mode=='test':
        test_file_src_en, test_file_src, test_file_tgt_en, test_file_tgt = concat_test_files(src, tgt, src_path,
                                                                                             tgt_path, output)
        align_files(test_file_src_en, test_file_src, test_file_tgt_en, test_file_tgt, output, src, tgt)

    elif mode=='train':
        train_file_src_en, train_file_src, train_file_tgt_en, train_file_tgt = get_train_files_paths(src,tgt,src_path,tgt_path)
        align_files(train_file_src_en, train_file_src, train_file_tgt_en, train_file_tgt, output, src, tgt)
    else:
        print('Unknown mode, use train or test')

def concat_test_files(src, tgt, src_path, tgt_path, out_path):
    '''Concats all the test files into one test file per language
    (one per source, source_english, target, target_english).
    Returns filenames of test files created.
    :param out_path: '''
    file_suffix = '.xml'
    test_data_src_en = []
    test_data_src = []
    test_data_tgt_en = []
    test_data_tgt = []
    for test_file in {
        'IWSLT14.TED.dev2010.en-',
        'IWSLT14.TED.tst2010.en-',
        'IWSLT14.TED.tst2011.en-',
        'IWSLT14.TED.tst2012.en-'}:
        with open(f'{src_path}/{test_file}{src}.{src}{file_suffix}') as f:
            test_data_src.extend(f.readlines())
        with open(f'{src_path}/{test_file}{src}.en{file_suffix}') as f:
            test_data_src_en.extend(f.readlines())
        with open(f'{tgt_path}/{test_file}{tgt}.{tgt}{file_suffix}') as f:
            test_data_tgt.extend(f.readlines())
        with open(f'{tgt_path}/{test_file}{tgt}.en{file_suffix}') as f:
            test_data_tgt_en.extend(f.readlines())

    test_file_src_en, test_file_src, test_file_tgt_en, test_file_tgt = (f'{src_path}/total-test-{src}.en{file_suffix}',
    f'{src_path}/total-test-{src}.{src}{file_suffix}',
    f'{tgt_path}/total-test-{tgt}.en{file_suffix}',
    f'{tgt_path}/total-test-{tgt}.{tgt}{file_suffix}')
    with open(test_file_src_en, 'w+') as f:
        f.writelines(test_data_src_en)
    with open(test_file_src, 'w+') as f:
        f.writelines(test_data_src)
    with open(test_file_tgt_en, 'w+') as f:
        f.writelines(test_data_tgt_en)
    with open(test_file_tgt, 'w+') as f:
        f.writelines(test_data_tgt)
    return test_file_src_en, test_file_src, test_file_tgt_en, test_file_tgt

def get_train_files_paths(src,tgt,src_path,tgt_path):
    file_prefix = 'train.tags.en-'
    file_suffix = ''
    train_file_src_en= f'{src_path}/{file_prefix}{src}.en'
    train_file_src= f'{src_path}/{file_prefix}{src}.{src}'
    train_file_tgt_en= f'{tgt_path}/{file_prefix}{tgt}.en'
    train_file_tgt= f'{tgt_path}/{file_prefix}{tgt}.{tgt}'
    return train_file_src_en, train_file_src, train_file_tgt_en, train_file_tgt

def align_files(src_file_en_path, src_file_path, tgt_file_en_path, tgt_file_path, output, src, tgt):
    '''Creates proper alignment between src and tgt language through the english data of each.
    Writes new correct files with 'output'
    :param src:
    :param tgt: '''
    src_file_handler = open(src_file_path)
    src_data = src_file_handler.readlines()
    tgt_file_handler = open(tgt_file_path)
    tgt_data = tgt_file_handler.readlines()

    mapping_src_to_tgt = []
    max_diff = abs(len(src_data)-len(tgt_data))
    print(f'max difference between files is {max_diff}')
    with open(src_file_en_path) as src_en:
        en_lines_src = src_en.readlines()
        with open(tgt_file_en_path) as tgt_en:
            en_lines_tgt = tgt_en.readlines()
            for src_ind, line in enumerate(en_lines_src[:10000]):
                tgt_ind = find_line_in_tgt(en_lines_tgt, line, index=src_ind, max_diff=max_diff)
                if src_ind%10000==0:
                    print(f'found line src {src_ind} in tgt {tgt_ind}')
                mapping_src_to_tgt.append((src_ind, tgt_ind))

    src_output_path, tgt_output_path = f'{output}.{src}', f'{output}.{tgt}'
    with open(src_output_path, 'a') as src_output:
        with open(tgt_output_path, 'a') as tgt_output:
            for src_index, tgt_ind in mapping_src_to_tgt:
                if tgt_ind!=-1:
                    print(f'writing src {src_output_path}, and tgt {tgt_output_path}')
                    src_output.writelines(src_data[src_index])
                    tgt_output.writelines(tgt_data[tgt_ind])

    src_file_handler.close()
    tgt_file_handler.close()
    return mapping_src_to_tgt

def find_line_in_tgt(tgt_lines, current_line, index=0, max_diff=0):
    '''Looks for src english line in tgt english text file to find the correct index mapping.
    First looks in a range around the current index, then looks through the whole file.
    Returns -1 if it is missing completely.'''
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