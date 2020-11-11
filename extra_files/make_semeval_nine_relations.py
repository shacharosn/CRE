import json

with open('/home/nlp/sharos/TRE/datasets/train.jsonl', 'r') as json_file:
    json_list = list(json_file)

all_examples_to_save = []

set_of_rels = set ()


for json_str in json_list:
    result = json.loads(json_str)
    # print("result: {}".format(result))
    # print(isinstance(result, dict))


    label = result['label']
    if '(e2,e1)' in label:
        subj_start, subj_end = result['entities'][1]
        obj_start, obj_end = result['entities'][0]

    else:
        subj_start, subj_end = result['entities'][0]
        obj_start, obj_end = result['entities'][1]

    if label == 'Other':
        label = 'no_relation'
    else:
        label = label.split('(')[0]
    curr_samp = {'id': result['id'], 'token': result['tokens'], 'relation': label, 'subj_start': subj_start, 'subj_end': subj_end-1, 'obj_start': obj_start, 'obj_end': obj_end-1}
    all_examples_to_save.append(curr_samp)

    set_of_rels.add(label)
    # print(curr_samp)
    # print()

print("len(all_examples_to_save)", len(all_examples_to_save))
print(set_of_rels)

with open('/home/nlp/sharos/TRE/datasets/train_semeval_as_tacred.json', 'w') as outfile:
    json.dump(all_examples_to_save, outfile)