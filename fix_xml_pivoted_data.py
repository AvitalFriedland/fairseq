import argparse



def find_talk_ids(lang, path='.'):
    with open(f'{path}/train.tags.en-{lang}.{lang}') as f:
        talk_ids = {}
        start, end = -1,-1
        lines = f.readlines()
        index = 0
        for index, line in enumerate(lines):
            if line.startswith('<url>'):
                start = index
            if line.startswith('<talkid>'):
                talk_id = line.split(">")[1].split("<")[0]
                end = find_next_keywords(lines, index)
                talk_ids[talk_id] = (start,end)
            index+=1
    return talk_ids

def find_next_keywords(lines, index):
    for end, line in enumerate(lines[index:]):
        if line.startswith('<keywords>'):
            return index+end


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src', '-s', type=str, required=True
    )
    parser.add_argument(
        '--tgt', '-t', type=str, required=True
    )
    parser.add_argument(
        '--path', '-p', type=str, required=False, default='.'
    )
    parser.add_argument('--out', '-o', type=str, required=True)
    args = parser.parse_args()

    source_talk_ids = find_talk_ids(args.src,path=args.path)
    target_talk_ids = find_talk_ids(args.tgt,path=args.path)
    intersecting_talk_ids = set(source_talk_ids).intersection(set(target_talk_ids))

    with open(f'{args.path}/train.tags.en-{args.src}.{args.src}') as f_src:
        lines_src = f_src.readlines()
        with open(f'{args.path}/train.tags.en-{args.tgt}.{args.tgt}') as f_tgt:
            lines_tgt = f_tgt.readlines()
            with open(f'{args.path}/{args.out}.{args.src}', 'a') as src_new:
                with open(f'{args.path}/{args.out}.{args.tgt}', 'a') as tgt_new:
                    for talk_id in intersecting_talk_ids:
                        start_src, end_src = source_talk_ids[talk_id][0], source_talk_ids[talk_id][1]
                        start_tgt, end_tgt = target_talk_ids[talk_id][0], target_talk_ids[talk_id][1]
                        print(f'writing talkid {talk_id} src: {source_talk_ids[talk_id]}, tgt: {target_talk_ids[talk_id]}')
                        src_new.writelines(lines_src[start_src:end_src])
                        tgt_new.writelines(lines_tgt[start_tgt:end_tgt])


# main()
# def find_talk_ids_check_fixed(lang):
#     with open(f'{args.path}/{arg{lang}') as f:
#         talk_ids = []
#         lines = f.readlines()
#         for index, line in enumerate(lines):
#             if line.startswith('<talkid>'):
#                 talk_id = line.split(">")[1].split("<")[0]
#                 talk_ids.append(talk_id)
#     return talk_ids

# spanish = find_talk_ids_check_fixed('spanish')
# italian = find_talk_ids_check_fixed('italian')
#
# print(set(spanish).difference(set(italian)))
# print(set(italian).difference(set(spanish)))
#
if __name__ == '__main__':
    main()