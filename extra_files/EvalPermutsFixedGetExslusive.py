import json
from collections import Counter
from collections import defaultdict
from IPython.display import display, Markdown
from tabulate import tabulate
from termcolor import colored
import csv
import pickle
from termcolor import colored, cprint


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
                       'per:city_of_birth': ['PERSON', 'CITY'], 'org:dissolved': ['ORGANIZATION', 'DATE'], 'no_relation': []}


def get_score_of_sents(rel, list_of_same_sents):
    good = bad = 0
    for sent in list_of_same_sents:
        if sent['pred'] == rel:
            good += 1
        else:
            bad += 1

    return good / (good + bad)


def get_most_common_preds(list_of_samples):
    preds = [samp['pred'] for samp in list_of_samples]
    counts = Counter(preds)
    sorted_counts = counts.most_common()

    max_value = sorted_counts[0][1]
    most_commons = [p[0] for p in sorted_counts if p[1] == max_value]

    return most_commons


def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<e1>' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</e1>'

    s[samp['obj_start']] = '<e2>' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</e2>'

    s_detokenize = " ".join(s)

    return {'id': samp['id'],'pred': samp['pred'], 'token': s_detokenize}


def get_clor_entitis(sent):
    subject_str = sent[sent.find('<e1>') + 4: sent.find('</e1>')]
    object_str = sent[sent.find('<e2>') + 4: sent.find('</e2>')]

    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))

    return color_sent


with open("../span_bert/SpanBERT/permut_stanford_ner_pure_exlusive_pred_tacred_DEV_and_TEST/data/json/test.json") as json_file:
    data_examples = json.load(json_file)

dic_data_examples = {samp['id'] : samp for samp in data_examples}

for i,j in enumerate(data_examples):
    print(j['id'])
    if i == 30:
        break

preds_dic = {}

wiki_list_of_preds = []
distreb_wiki = {}  # defaultdict(int)
combine_sentences_per_id = {}

with open("../span_bert/SpanBERT/permut_stanford_ner_tacred_pure_exlusive_pred_tacred_DEV_and_TEST_dir_pred/predictions.txt", "r") as f:
    contents = f.read()
    for i, example in enumerate(contents.splitlines()):
        example_id = example.strip().split("\t")[0]
        pred = example.strip().split("\t")[1]
        wiki_list_of_preds.append(pred)


        split_by_ = example_id.split("_")
        cuted_id = "_".join(split_by_[:-1])

        if cuted_id not in distreb_wiki:
            distreb_wiki[cuted_id] = defaultdict(int)

        distreb_wiki[cuted_id][pred] += 1

        curr_data_example = dic_data_examples[example_id]
        curr_data_example['pred'] = pred

        if cuted_id not in combine_sentences_per_id:
            combine_sentences_per_id[cuted_id] = []

        combine_sentences_per_id[cuted_id].append(curr_data_example)



fixed_combine_sentences_per_id = {}

for e_id in combine_sentences_per_id:

    for samp in combine_sentences_per_id[e_id]:
        id_fixed = e_id + "_" + str(samp['subj_start']) + str(samp['subj_end'])

        if id_fixed not in fixed_combine_sentences_per_id:
            fixed_combine_sentences_per_id[id_fixed] = []

        fixed_combine_sentences_per_id[id_fixed].append(samp)

sents_per_rel = {}

for f_id in fixed_combine_sentences_per_id:

    # rels = [samp['relation'] for samp in fixed_combine_sentences_per_id[f_id] if samp['relation'] != 'no_relation' and set(ALL_RELATIONS_TYPES[samp['relation']]) == {
    #     samp['subj_type'], samp['obj_type']}]

    rels = set([samp['relation'] for samp in fixed_combine_sentences_per_id[f_id] if ALL_RELATIONS_TYPES[samp['relation']] ==  [samp['subj_type'], samp['obj_type']]])

    # if fixed_combine_sentences_per_id[f_id][0]['relation'] == 'per:age' and rels == []:
    #     for samp in fixed_combine_sentences_per_id[f_id]:
    #             print()
    #             print(colored(samp['relation'] + '\t', 'magenta', attrs=['bold']), get_clor_entitis(make_readable_sampl(samp)['token']))
    #             print()


    # counts = Counter(preds)
    # sorted_counts = counts.most_common()
    #
    # # max_value = sorted_counts[0][1]
    # # more_then_one_pred = [p[0] for p in sorted_counts if p[1] > 1]
    # at_least_one_pred = [p for p in preds if p != 'NA']

    for p in rels:

        if p not in sents_per_rel:
            sents_per_rel[p] = []

        sents_per_rel[p].append(f_id)



ALL_PERMUTS_PER_REL = {}

set_of_all_nums = set()

for r in sents_per_rel:

    ALL_PERMUTS_PER_REL[r] = {}

    for _id in sents_per_rel[r]:
        num_of_permuts_by_id = len(fixed_combine_sentences_per_id[_id])
        set_of_all_nums.add(num_of_permuts_by_id)

        if num_of_permuts_by_id not in ALL_PERMUTS_PER_REL[r]:
            ALL_PERMUTS_PER_REL[r][num_of_permuts_by_id] = []

        ALL_PERMUTS_PER_REL[r][num_of_permuts_by_id].append(fixed_combine_sentences_per_id[_id])  # list of lists of dics

set_dup = set()
for r in ALL_PERMUTS_PER_REL:
    for n in ALL_PERMUTS_PER_REL[r]:
        for batch in ALL_PERMUTS_PER_REL[r][n]:
            for ts in batch:
                print("DDDDDD")
                print(ts)
                if ts['id'] in set_dup:
                    print(ts['id'])
                    print(ts["ff"])
                set_dup.add(ts['id'])


Metric1 = {}

for r in ALL_PERMUTS_PER_REL:
    Metric1[r] = {}
    for num in ALL_PERMUTS_PER_REL[r]:
        score_of_num = []
        for list_of_same_sents in ALL_PERMUTS_PER_REL[r][num]:
            assert len(list_of_same_sents) == num

            # score_of_sents = sum([1 for x in list_of_same_sents if x['pred'] == r]) / len(list_of_same_sents)
            # condition_a = lambda candidate: 1 if sum()
            condition_c = lambda candidate: 1 if sum([1 for x in candidate if x['pred'] == r]) > 1 else 0
            score_of_sents = condition_c(list_of_same_sents)
            # score_of_sents = 1 if sum([1 for x in list_of_same_sents if x['pred'] == r]) > 1 else 0
            score_of_num.append(score_of_sents)


        Metric1[r][num] = sum(score_of_num), round(sum(score_of_num) / len(score_of_num),3), len(score_of_num)
        # print(Metric1[r][num])
    #         print(score_of_num[41412])

    for n in set_of_all_nums:
        if n not in Metric1[r]:
            Metric1[r][n] = "NA"

heads = ['num']
for r in ALL_PERMUTS_PER_REL:
    heads.append(r)

tabu = []

for num in sorted(set_of_all_nums):
    curr_tabu = [str(num)]
    for r in ALL_PERMUTS_PER_REL:
        if type(Metric1[r][num]) is tuple:
            curr_tabu.append(colored(str(Metric1[r][num]), 'blue', attrs=['bold']))
        else:
            curr_tabu.append(str(Metric1[r][num]))
    tabu.append(curr_tabu)

print(tabulate(tabu, headers=heads, tablefmt='orgtbl'))




count_p = count_n = 0

for k, i in enumerate(distreb_wiki):
    if sum([distreb_wiki[i][x] for x in distreb_wiki[i]]) > 1:
        if not (len(set(distreb_wiki[i])) == 1 and list(distreb_wiki[i].keys())[0] == 'no_relation'):

            if max([distreb_wiki[i][k] for k in distreb_wiki[i] if k != 'no_relation']) >= 2:

                print(k, distreb_wiki[i])
                count_p += 1
            else:
                count_n += 1

print(count_p + count_n)
print(count_p / (count_p + count_n))


print(tabulate(tabu, headers=heads, tablefmt='orgtbl'))
print()


print("ss")

SHIT = 0
TO_SAVE = {}
dup = set()
with open('exclusive_to_tag2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(["SN", "Name", "Contribution"])

    count_gold_age = 0
    count_examle_with_gold = {}
    PURE_EXLUSIVE = ['per:date_of_birth', 'per:date_of_death', 'org:founded', 'per:age','org:number_of_employees/members']
    for r in PURE_EXLUSIVE:
        for num in ALL_PERMUTS_PER_REL[r]:
            if num == 1:
                continue
            for batch in ALL_PERMUTS_PER_REL[r][num]:
                # if sum([1 for x in batch if x['relation'] == x["gold_label"]]) == 0:
                #     continue
                print(r, num)

                if r not in count_examle_with_gold:
                    count_examle_with_gold[r] = {}
                if num not in count_examle_with_gold[r]:
                    count_examle_with_gold[r][num] = 0

                if r not in TO_SAVE:
                    TO_SAVE[r] = {}
                if num not in TO_SAVE[r]:
                    TO_SAVE[r][num] = []

                count_examle_with_gold[r][num] += 1
                list_of_ts = []
                for index, ts in enumerate(batch):
                    if ts['id'] in dup:
                        print(ts['id'])
                        print(ts['id']["ff"])
                    dup.add(ts['id'])
                    if ts['relation'] == ts["gold_label"]:
                        if ts["gold_label"] == 'per:age':
                            count_gold_age += 1
                        print(colored(str(index)+'\t', 'yellow', attrs=['reverse', 'blink']), colored(ts['relation']+'\t', 'magenta', attrs=['bold']), get_clor_entitis(make_readable_sampl(ts)['token']))
                        print(ts['id'])
                        writer.writerow([str(index)+" -@@@@ ", ts['id'], ts['relation'], make_readable_sampl(ts)['token']])
                        writer.writerow([])
                        SHIT += 1
                        list_of_ts.append(ts)
                    else:
                        print(index, colored(ts['relation']+'\t', 'magenta', attrs=['bold']), get_clor_entitis(make_readable_sampl(ts)['token']))
                        print(ts['id'])
                        writer.writerow(
                            [str(index) + " -@@@@ ", ts['id'], ts['relation'], make_readable_sampl(ts)['token']])
                        writer.writerow([])
                        SHIT += 1
                        list_of_ts.append(ts)

                    print()
                TO_SAVE[r][num].append(list_of_ts)

            print("-------------------------------------------------------------------------------------------------------------------")
            writer.writerow(["-------------------------------------------------------------------------------------------------------------------"])


with open('to_annotate' + '.pkl', 'wb') as f:
    pickle.dump(TO_SAVE, f, pickle.HIGHEST_PROTOCOL)

print("ZZZ: " ,count_gold_age)
print("SHIT: ",SHIT)

for r in count_examle_with_gold:
    for n in count_examle_with_gold[r]:
        print(r, n," --- ",count_examle_with_gold[r][n])



my_id = set()
real_id = set()

# for batch in ALL_PERMUTS_PER_REL['per:age'][1]:
#     for ts in batch:
#         my_id.add(ts['id'].split("_")[0])
        # print(colored(ts['relation'] + '\t', 'magenta', attrs=['bold']),
        #       get_clor_entitis(make_readable_sampl(ts)['token']))
#         # print()
#         # print()
#         # print(ts['stanford_ner'])
#         # print(
#         #     "-------------------------------------------------------------------------------------------------------------------")
#


# for r in TO_SAVE:
#     if r not in PURE_EXLUSIVE:
#         continue
#     for n in TO_SAVE[r]:
#         for ts in TO_SAVE[r][n]:
#             my_id.add(ts['id'].split("_")[0])
#
# with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
#     test_tacred_real_samples = json.load(tacred_test_file)
#
#     dic_data_examples = {samp['id']: samp for samp in test_tacred_real_samples}
#
# for samp in test_tacred_real_samples:
#     real_id.add(samp['id'])
#
# all_age_types = []
# for idd in real_id:
#     if dic_data_examples[idd]["relation"] not in PURE_EXLUSIVE:
#         continue
#     if idd not in my_id:
#         print(idd)
#         for ts in data_examples:
#             if ts['id'].split("_")[0] == idd:
#                 print(colored(ts['relation'] + '\t', 'magenta', attrs=['bold']),
#                       get_clor_entitis(make_readable_sampl(ts)['token']))
#                 print()
#                 print()
#                 print(ts['stanford_ner'])
#                 print(ts['stanford_ner'])
#                 print(ts['id'])
#                 print()
#         print("-------------------------------------------------------------------------------------------------------------------")






