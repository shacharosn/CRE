import json
from termcolor import colored
import pickle
from collections import Counter
import os
from os import listdir
from os.path import isfile, join


first_6 = ['org:founded_by','per:age','per:date_of_birth',
          'org:founded','per:schools_attended','per:employee_of']

shachar = ['org:country_of_headquarters', 'per:alternate_names', 'per:children', 'per:city_of_birth',
           'per:city_of_death', 'per:date_of_death', 'per:religion', 'per:spouse', 'org:alternate_names',
           'per:title', 'org:parents', 'per:other_family',
           'per:stateorprovince_of_birth', 'org:political/religious_affiliation']




alon_final = ['per:siblings', 'per:origin', 'per:cities_of_residence', 'org:city_of_headquarters',
              'per:countries_of_residence', 'per:parents', 'per:stateorprovinces_of_residence',
              'org:top_members/employees', 'org:stateorprovince_of_headquarters', 'org:number_of_employees/members']


all_30_relations = first_6 + shachar + alon_final



high = ['org:political/religious_affiliation', 'per:alternate_names', 'per:stateorprovince_of_birth', 'per:other_family', 'org:parents',
        'per:spouse', 'per:religion', 'per:city_of_death', 'per:city_of_birth', 'org:country_of_headquarters', 'per:date_of_birth', 'org:founded_by']
# with open('wiki_57_58_59_60_61_62_63_64_65_not_fixed' + '.pkl', 'rb') as f:
#     dic_to_annotate_unfiltterd = pickle.load(f)
#
# print("read dic_to_annotate_unfiltterd")
#
# with open('wiki_66_67_68_69_70_71_72_not_fixed' + '.pkl', 'rb') as f:
#     dic_to_annotate_unfiltterd_66_67_68_69_70_71_72 = pickle.load(f)
#
# print("read dic_to_annotate_unfiltterd_66_67_68_69_70_71_72")
#
# with open('wiki_13_34_35_14-23_36-45_47-51_52-56_not_fixed.pkl', 'rb') as f:
#     dic_to_annotate_13_34_35 = pickle.load(f)
#
#
#
# for rel in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72:
#     if rel not in dic_to_annotate_unfiltterd:
#         dic_to_annotate_unfiltterd[rel] = {}
#
#     for num in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72[rel]:
#         if num not in dic_to_annotate_unfiltterd[rel]:
#             dic_to_annotate_unfiltterd[rel][num] = []
#
#         for batch in dic_to_annotate_unfiltterd_66_67_68_69_70_71_72[rel][num]:
#             dic_to_annotate_unfiltterd[rel][num].append(batch)
#
#
# for rel in dic_to_annotate_13_34_35:
#     if rel not in dic_to_annotate_unfiltterd:
#         dic_to_annotate_unfiltterd[rel] = {}
#
#     for num in dic_to_annotate_13_34_35[rel]:
#         if num not in dic_to_annotate_unfiltterd[rel]:
#             dic_to_annotate_unfiltterd[rel][num] = []
#
#         for batch in dic_to_annotate_13_34_35[rel][num]:
#             dic_to_annotate_unfiltterd[rel][num].append(batch)
#
#
#
# with open('data_jason_20_relations.txt', 'w') as outfile:
#     json.dump(dic_to_annotate_unfiltterd, outfile)


with open('data_jason_20_relations.txt') as json_file:
    data_jason_20_relations = json.load(json_file)


# with open('DICT_TO_ANNOTATE_ALL_RELS_same_type_then_more_then_2_57_58_59_60_61_62_63_64_obj_and_subj_distance_2_threshold_150_with_more_ids_what_i_sent_to_alon.json') as json_file:
#     alooooooooon = json.load(json_file)
#
# print("noy1")
#
# set_of_alon = set()
# for rel in alooooooooon:
#     for num in alooooooooon[rel]:
#         all_original_batches = [set( t['id'] for t in b) for b in data_jason_20_relations[rel][str(num)]]
#         for batch in alooooooooon[rel][num]:
#             ids_of_batch = set([ts['id'] for ts in batch])
#             if any([1 for a_o_b in all_original_batches if a_o_b == ids_of_batch]):
#                 continue
#             print("Fdsfsdf"[42423])
#
# print("noy2")



files_path = "ALL_ANNOTATED_DATA"


onlyfiles = [join(files_path, f) for f in listdir(files_path)]

annotated_data = {}

for fname in onlyfiles:
    rel_annotated = fname.split("ALL_ANNOTATED_DATA/ANNOTATED_DATA_")
    rel_annotated = rel_annotated[1].replace('-', ':').replace('_or_or_or_', '/')
    rel_annotated = rel_annotated.split(".txt")[0]

    annotated_data[rel_annotated] = {}

    with open(fname, 'r') as f:
        marge_annotated = f.readlines()
        for l in marge_annotated:
            line_split = l.split()
            #     if line_split[1] != 'invalid':
            annotated_data[rel_annotated][line_split[0]] = 'no_relation' if line_split[1] == 'NA' else line_split[1]





gold_annotations = {}


for rel in all_30_relations:
    print(rel)

    num_of_batches = 0
    with_invalid = 0

    if rel not in all_30_relations:
        continue

    gold_annotations[rel] = {}

    for num in data_jason_20_relations[rel]:

        for batch in data_jason_20_relations[rel][num]:

            annotated_combinations = [annotated_data[rel][ts['id']] for ts in batch if ts['id'] in annotated_data[rel]]

            if not annotated_combinations:
                continue

            if 'invalid' in set(annotated_combinations):
                with_invalid += 1
                continue

            num_of_batches += 1

            if num not in gold_annotations[rel]:
                gold_annotations[rel][num] = []

            gold_batch = []
            for ts in batch:
                ts_gold = ts.copy()
                ts_gold["gold"] = annotated_data[rel][ts['id']]
                gold_batch.append(ts_gold)


            gold_annotations[rel][num].append(gold_batch)

            if str(len(annotated_combinations)) != str(num):
                print(rel)
                print(num)
                print(str(len(annotated_combinations)))
                print(annotated_combinations)
                print("ss"[4233])



    print(rel, "num_of_batches: ", num_of_batches)


print(onlyfiles)
print(len(onlyfiles))

with open('gold_annotations.json', 'w') as outfile:
    json.dump(gold_annotations, outfile)
