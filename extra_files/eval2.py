import json
from termcolor import colored
import pickle
from collections import Counter





ALL_RELATIONS_TYPES = {'per:title': ['PERSON', 'TITLE'], 'org:top_members/employees': ['ORGANIZATION', 'PERSON'],
                       'org:country_of_headquarters': ['ORGANIZATION', 'COUNTRY'], 'per:parents': ['PERSON', 'PERSON'],
                       'per:age': ['PERSON', 'NUMBER'], 'per:countries_of_residence': ['PERSON', 'COUNTRY'],
                       'per:children': ['PERSON', 'PERSON'], 'org:alternate_names': ['ORGANIZATION', 'ORGANIZATION'],
                       'per:charges': ['PERSON', 'CRIMINAL_CHARGE'], 'per:cities_of_residence': ['PERSON', 'CITY'],
                       'per:origin': ['PERSON', 'NATIONALITY'], 'org:founded_by': ['ORGANIZATION', 'PERSON'],
                       'per:employee_of': ['PERSON', 'ORGANIZATION'], 'per:siblings': ['PERSON', 'PERSON'],
                       'per:alternate_names': ['PERSON', 'PERSON'], 'org:website': ['ORGANIZATION', 'URL'],
                       'per:religion': ['PERSON', 'RELIGION'], 'per:stateorprovince_of_death': ['PERSON', 'LOCATION'],
                       'org:parents': ['ORGANIZATION', 'ORGANIZATION'],
                       'org:subsidiaries': ['ORGANIZATION', 'ORGANIZATION'], 'per:other_family': ['PERSON', 'PERSON'],
                       'per:stateorprovinces_of_residence': ['PERSON', 'STATE_OR_PROVINCE'],
                       'org:members': ['ORGANIZATION', 'ORGANIZATION'],
                       'per:cause_of_death': ['PERSON', 'CAUSE_OF_DEATH'],
                       'org:member_of': ['ORGANIZATION', 'LOCATION'],
                       'org:number_of_employees/members': ['ORGANIZATION', 'NUMBER'],
                       'per:country_of_birth': ['PERSON', 'COUNTRY'],
                       'org:shareholders': ['ORGANIZATION', 'ORGANIZATION'],
                       'org:stateorprovince_of_headquarters': ['ORGANIZATION', 'STATE_OR_PROVINCE'],
                       'per:city_of_death': ['PERSON', 'CITY'], 'per:date_of_birth': ['PERSON', 'DATE'],
                       'per:spouse': ['PERSON', 'PERSON'], 'org:city_of_headquarters': ['ORGANIZATION', 'CITY'],
                       'per:date_of_death': ['PERSON', 'DATE'], 'per:schools_attended': ['PERSON', 'ORGANIZATION'],
                       'org:political/religious_affiliation': ['ORGANIZATION', 'RELIGION'],
                       'per:country_of_death': ['PERSON', 'COUNTRY'], 'org:founded': ['ORGANIZATION', 'DATE'],
                       'per:stateorprovince_of_birth': ['PERSON', 'STATE_OR_PROVINCE'],
                       'per:city_of_birth': ['PERSON', 'CITY'], 'org:dissolved': ['ORGANIZATION', 'DATE']}


def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<e1>' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</e1>'

    s[samp['obj_start']] = '<e2>' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</e2>'

    s_detokenize = " ".join(s)

    return {'id': samp['id'], 'pred': samp['pred'], 'token': s_detokenize}


def get_clor_entitis(sent):
    subject_str = sent[sent.find('<e1>') + 4: sent.find('</e1>')]
    object_str = sent[sent.find('<e2>') + 4: sent.find('</e2>')]
    sent = sent.replace("-LRB-", "(")
    sent = sent.replace("-RRB-", ")")
    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))

    return color_sent


def is_valid_type(ts, rel, ALL_RELATIONS_TYPES):
    if ts['subj_type'] == ALL_RELATIONS_TYPES[rel][0] and ts['obj_type'] == ALL_RELATIONS_TYPES[rel][1]:
        return True
    return False


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return subj_span, obj_span


# with open('wiki_13_34_35_14-23_36-45_47-51_52-56_not_fixed.pkl', 'rb') as f:
#     dic_to_annotate_unfiltterd = pickle.load(f)

with open('wiki_57_58_59_60_61_62_63_64_65_not_fixed' + '.pkl', 'rb') as f:
    dic_to_annotate_unfiltterd = pickle.load(f)

print("read dic_to_annotate_unfiltterd")

with open('wiki_66_67_68_69_70_71_72_not_fixed' + '.pkl', 'rb') as f:
    dic_to_annotate_unfiltterd_66_67_68_69_70_71_72 = pickle.load(f)

print("read dic_to_annotate_unfiltterd_66_67_68_69_70_71_72")


for rel in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72:
    if rel not in dic_to_annotate_unfiltterd:
        dic_to_annotate_unfiltterd[rel] = {}

    for num in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72[rel]:
        if num not in dic_to_annotate_unfiltterd[rel]:
            dic_to_annotate_unfiltterd[rel][num] = []

        for batch in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72[rel][num]:
            dic_to_annotate_unfiltterd[rel][num].append(batch)




count_city = 0

# for num in dic_to_annotate_unfiltterd['per:city_of_birth']:
#     for batch in dic_to_annotate_unfiltterd['per:city_of_birth'][num]:
#         count_city += 1
#         for ts in batch:
#             if ts['obj_type'] == 'CITY':
#                 print(ts)
#                 print()
#                 # count_city += 1

print("count_city:", count_city)
# print("ss"[21341])
# with open('wiki_13_34_35_14-23_36-45_47-51_52-56_not_fixed.json', 'w') as fp:
#     json.dump(dic_to_annotate_unfiltterd, fp)

# with open('wiki_13_34_35_14-23_36-45_47-51_52-56_not_fixed.json', 'r') as fp:
#     dic_to_annotate_unfiltterd = json.load(fp)



second_counter = 0

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_per-children.txt", 'r') as f:
    marge_annotated1 = f.readlines()

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_per-employee_of.txt", 'r') as f:
    marge_annotated2 = f.readlines()

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_per-children.txt", 'r') as f:
    marge_annotated3 = f.readlines()

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_org-political_or_or_or_religious_affiliation.txt", 'r') as f:
    marge_annotated4 = f.readlines()

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_per-spouse.txt", 'r') as f:
    marge_annotated5 = f.readlines()

with open("ALL_ANNOTATED_DATA/ANNOTATED_DATA_per-date_of_birth.txt", 'r') as f:
    marge_annotated6 = f.readlines()


marge_annotated_to_check_if_already_in = marge_annotated1 + marge_annotated2 + marge_annotated3 + marge_annotated4 + marge_annotated5 + marge_annotated6


annotated_data_to_check_if_already_in = {}

for l in marge_annotated_to_check_if_already_in:
    line_split = l.split()
    # if line_split[1] != 'invalid':
    annotated_data_to_check_if_already_in[line_split[0]] = line_split[1]





print("AAA")
for rel in dic_to_annotate_unfiltterd:
    for num in dic_to_annotate_unfiltterd[rel]:
        for batch in dic_to_annotate_unfiltterd[rel][num]:
            for ts in batch:
                if ts['id'] == "52-56-842fb55f-47cc-4beb-aa62-0a88c28c3b73_PERSON_PERSON_6040440":
                    print("FIND!!!!!!!")


print("BBBB")

filterd_by_types_dic_to_annotate = {}




number_of_batchs_annotated = 0

for rel in dic_to_annotate_unfiltterd:
    filterd_by_types_dic_to_annotate[rel] = {}
    for num in dic_to_annotate_unfiltterd[rel]:
        filterd_by_types_dic_to_annotate[rel][num] = []
        for batch in dic_to_annotate_unfiltterd[rel][num]:

            if any([1 for ts in batch if ts['id'] in annotated_data_to_check_if_already_in]): # and annotated_data_to_check_if_already_in[ts['id']] != 'invalid']):
                number_of_batchs_annotated += 1
                continue

            obj_indexs = [(ts['obj_start'], ts['obj_end']) for ts in batch]
            subj_indexs = [(ts['subj_start'], ts['subj_end']) for ts in batch]


            # if "second" in set([(get_span_of_subj_obj(ts))[1] for ts in batch]):
            #     second_counter += 1
            #     continue

            # set_subjs = set([(get_span_of_subj_obj(ts))[0] for ts in batch])
            # set_objs = set([(get_span_of_subj_obj(ts))[1] for ts in batch])
            #
            # if any([1 for o in set_objs for s in set_subjs if o in s]):
            #     continue

            if len(set([(get_span_of_subj_obj(ts))[1] for ts in batch])) == 1 and len(set([(get_span_of_subj_obj(ts))[0] for ts in batch])) == 1:
                continue

            if any([1 for tup, tup_count in Counter([(get_span_of_subj_obj(ts)) for ts in batch]).items() if tup_count > 1]):
                continue


            if any([first for i, first in enumerate(obj_indexs) for j, second in enumerate(obj_indexs) if
                    i != j and (abs(second[0] - first[1]) == 2 or abs(first[0] - second[1]) == 2)]):
                continue

            if any([first for i, first in enumerate(subj_indexs) for j, second in enumerate(subj_indexs) if
                    i != j and (abs(second[0] - first[1]) == 2 or abs(first[0] - second[1]) == 2)]):
                continue

            if any([first for i, first in enumerate(subj_indexs) for j, second in enumerate(subj_indexs) if
                    i != j and (abs(second[0] - first[1]) == 3 or abs(first[0] - second[1]) == 3)]):
                continue


            if is_valid_type(batch[0], rel, ALL_RELATIONS_TYPES):
                if ALL_RELATIONS_TYPES[rel][0] == ALL_RELATIONS_TYPES[rel][1]:
                    if sum([1 for ts in batch if ts['pred'] == rel]) > 2:
                        filterd_by_types_dic_to_annotate[rel][num].append(batch)
                else:
                    filterd_by_types_dic_to_annotate[rel][num].append(batch)


dic_to_annotate = filterd_by_types_dic_to_annotate    # dic_to_annotate_unfiltterd #filterd_by_types_dic_to_annotate

"""
       sample uniformly without replacement!
"""


import random
from collections import Counter

# RELS_TO_ANNOTATE = ['org:founded','per:schools_attended','org:founded_by','org:city_of_headquarters']

# RELS_TO_ANNOTATE = 'org:founded'


FILE_TO_WRITE = "ANNOTATED_data.txt"

NUM_OF_EXAMPLES = 120


def sample(n, upper):
    lower = 0
    result = []
    pool = {}
    for _ in range(n):
        i = random.randint(lower, upper)
        x = pool.get(i, i)
        pool[i] = pool.get(lower, lower)
        lower += 1
        result.append(x)
    return result



list_of_all_num_and_sents_per_rel = {}


for rel in dic_to_annotate:

    list_of_all_num_and_sents_per_rel[rel] = []

    for num in sorted([n for n in dic_to_annotate[rel]]):
        if num == 1 or num > 10:
            continue

        for idx_sents, batch in enumerate(dic_to_annotate[rel][num]):
            list_of_all_num_and_sents_per_rel[rel].append([num, idx_sents])

DICT_TO_SAVE = {}

for rel in dic_to_annotate:

    if rel == "no_relation":
        continue
    # if rel not in RELS_TO_ANNOTATE:
    #     continue


    DICT_TO_SAVE[rel] = {}

    list_of_tuples_selected_examples = list_of_all_num_and_sents_per_rel[rel]
    print("AAAA")
    print(rel)
    print(len(list_of_tuples_selected_examples))
    print(Counter([i[0] for i in list_of_tuples_selected_examples]))
    if len(list_of_tuples_selected_examples) < NUM_OF_EXAMPLES:
        continue
    sampled_idxs = sample(NUM_OF_EXAMPLES, len(list_of_tuples_selected_examples) - 1)
    counter_of_nums = Counter([list_of_tuples_selected_examples[i][0] for i in sampled_idxs])
    print(counter_of_nums)

    for i in sorted(sampled_idxs):
        num, idx_sent = list_of_tuples_selected_examples[i]
        batch = dic_to_annotate[rel][num][idx_sent]

        if num not in DICT_TO_SAVE[rel]:
            DICT_TO_SAVE[rel][num] = []

        DICT_TO_SAVE[rel][num].append(batch)

# with open('DICT_TO_ANNOTATE_ALL_RELS.pkl', 'wb') as f:
#     pickle.dump(DICT_TO_SAVE, f, pickle.HIGHEST_PROTOCOL)

with open('DICT_TO_ANNOTATE_ALL_RELS_same_type_then_more_then_2_57_58_59_60_61_62_63_64_65_66_67_68_69_70_71_72_obj_and_subj_distance_2_threshold_150_with_more_ids.json', 'w') as fp:
    json.dump(DICT_TO_SAVE, fp)



# for num in dic_to_annotate_unfiltterd['per:city_of_birth']:
#     for batch in dic_to_annotate_unfiltterd['per:city_of_birth'][num]:
#         for ts in batch:
#             print(ts)
#             print()
#             print()



print("number_of_batchs_annotated: ", number_of_batchs_annotated)

print()

print("second_counter: ", second_counter)
