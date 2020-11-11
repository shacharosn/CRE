import json
from collections import Counter
from collections import defaultdict
from IPython.display import display, Markdown
from tabulate import tabulate
from termcolor import colored
from nltk.tokenize.treebank import TreebankWordDetokenizer

ALL_RELATIONS_TYPES = {'per:title': ['PERSON', 'TITLE'], 'org:top_members/employees': ['ORGANIZATION', 'PERSON'],
                       'org:country_of_headquarters': ['ORGANIZATION', 'COUNTRY'], 'per:parents': ['PERSON', 'PERSON'],
                       'per:age': ['PERSON', 'DURATION'], 'per:countries_of_residence': ['PERSON', 'COUNTRY'],
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

    s_detokenize = TreebankWordDetokenizer().detokenize(s)


    return {'id': samp['id'],'pred': samp['pred'], 'token': s_detokenize}


def get_clor_entitis(sent):
    subject_str = sent[sent.find('<e1>') + 4: sent.find('</e1>')]
    object_str = sent[sent.find('<e2>') + 4: sent.find('</e2>')]

    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))

    return color_sent


with open("../span_bert/SpanBERT/permut_stanford_ner_pred_tacred/data/json/test.json") as json_file:
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

with open("../span_bert/SpanBERT/permut_stanford_ner_tacred_dir_pred/predictions.txt", "r") as f:
    contents = f.read()
    for i, example in enumerate(contents.splitlines()):
        example_id = example.strip().split("\t")[0]
        pred = example.strip().split("\t")[1]
        wiki_list_of_preds.append(pred)

        # iidd, subj_type, obj_type, id_counter = example_id.split("_")
        # cuted_id = "_".join([iidd, subj_type, obj_type])

        split_by_ = example_id.split("_")
        cuted_id = "_".join(split_by_[:-1])

        if cuted_id not in distreb_wiki:
            distreb_wiki[cuted_id] = defaultdict(int)

        distreb_wiki[cuted_id][pred] += 1


        # if dic_data_examples[example_id]['id'] !=  example_id:
        #     print(dic_data_examples[example_id]['id'] , example_id)
        #
        # assert dic_data_examples[example_id] ==  example_id



        curr_data_example = dic_data_examples[example_id]
        curr_data_example['pred'] = pred

        if cuted_id not in combine_sentences_per_id:
            combine_sentences_per_id[cuted_id] = []

        combine_sentences_per_id[cuted_id].append(curr_data_example)

sents_per_rel = {}



for e_id in combine_sentences_per_id:
    # iidd, subj_type, obj_type = e_id.split("_")

    most_common_preds = get_most_common_preds(combine_sentences_per_id[e_id])

    for p in most_common_preds:

        if p not in sents_per_rel:
            sents_per_rel[p] = []

        sents_per_rel[p].append(e_id)




        # if subj_type == ents_types[0] and obj_type == ents_types[1]:
        #     sents_per_rel[rel].append(e_id)





ALL_PERMUTS_PER_REL = {}

set_of_all_nums = set()

for r in sents_per_rel:

    ALL_PERMUTS_PER_REL[r] = {}

    for _id in sents_per_rel[r]:
        num_of_permuts_by_id = len(combine_sentences_per_id[_id])
        set_of_all_nums.add(num_of_permuts_by_id)

        if num_of_permuts_by_id not in ALL_PERMUTS_PER_REL[r]:
            ALL_PERMUTS_PER_REL[r][num_of_permuts_by_id] = []

        ALL_PERMUTS_PER_REL[r][num_of_permuts_by_id].append(combine_sentences_per_id[_id])  # list of lists of dics

Metric1 = {}

for r in ALL_PERMUTS_PER_REL:
    Metric1[r] = {}
    for num in ALL_PERMUTS_PER_REL[r]:
        score_of_num = []
        for list_of_same_sents in ALL_PERMUTS_PER_REL[r][num]:
            assert len(list_of_same_sents) == num

            score_of_sents = sum([1 for x in list_of_same_sents if x['pred'] == r]) / len(list_of_same_sents)
            score_of_num.append(score_of_sents)


        Metric1[r][num] = round(sum(score_of_num) / len(score_of_num),3), len(score_of_num)
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

# print(r)
# print()
# print(curr_counts_of_prnuts)
# print("----------------------")


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


print("sss")


with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    test_tacred_real_samples = json.load(tacred_test_file)

with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/dev.json") as tacred_dev_file:
    dev_tacred_real_samples = json.load(tacred_dev_file)

tacredww_real_samples = test_tacred_real_samples + dev_tacred_real_samples
print("tacredww_real_samples:",len(tacredww_real_samples))