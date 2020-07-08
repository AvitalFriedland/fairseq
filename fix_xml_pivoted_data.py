
def find_talk_ids(lang):
    with open(f'data/fix_preprocessed/train.tags.en-{lang}.{lang}') as f:
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
    italian_talk_ids = find_talk_ids('it')
    spanish_talk_ids = find_talk_ids('es')
    intersecting_talk_ids = set(italian_talk_ids).intersection(set(spanish_talk_ids))

    with open('data/fix_preprocessed/train.tags.en-es.es') as f:
        lines = f.readlines()
        with open('data/fix_preprocessed/fixed_spanish', 'a') as new_file:
            for talk_id in intersecting_talk_ids:
                start, end = spanish_talk_ids[talk_id][0], spanish_talk_ids[talk_id][1]
                print(f'writing to spanish file {start} {end}')
                new_file.writelines(lines[start:end])
    with open('data/fix_preprocessed/train.tags.en-it.it') as f:
        lines = f.readlines()
        with open('data/fix_preprocessed/fixed_italian', 'a') as new_file:
            for talk_id in intersecting_talk_ids:
                start, end = italian_talk_ids[talk_id][0], italian_talk_ids[talk_id][1]
                print(f'writing to italian file {start} {end}')
                new_file.writelines(lines[start:end])
# main()
def find_talk_ids_check_fixed(lang):
    with open(f'data/fix_preprocessed/fixed_{lang}') as f:
        talk_ids = []
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.startswith('<talkid>'):
                talk_id = line.split(">")[1].split("<")[0]
                talk_ids.append(talk_id)
    return talk_ids

spanish = find_talk_ids_check_fixed('spanish')
italian = find_talk_ids_check_fixed('italian')

print(set(spanish).difference(set(italian)))
print(set(italian).difference(set(spanish)))

