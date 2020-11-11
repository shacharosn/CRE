import json
from collections import Counter
from collections import defaultdict
from IPython.display import display, Markdown
from tabulate import tabulate
from termcolor import colored
import pickle
import time
import math
from sklearn.metrics import accuracy_score

print("WWW !!!")




AAA = 0
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



ALL_PAIRS_TYPES_ASSIGNED_TO_ONE_REL = {('PERSON', 'RELIGION'), ('PERSON', 'CRIMINAL_CHARGE'), ('PERSON', 'MISC'), ('PERSON', 'TITLE'),
                                      ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'RELIGION'), ('PERSON', 'NUMBER'), ('ORGANIZATION', 'URL'),
                                      ('PERSON', 'DURATION'), ('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'NUMBER'), ('ORGANIZATION', 'CITY'), ('ORGANIZATION', 'IDEOLOGY')}


def compute_f1(preds, labels):
    n_gold = n_pred = n_correct = 0
    for pred, label in zip(preds, labels):
        if pred != 'no_relation':
            n_pred += 1
        if label != 'no_relation':
            n_gold += 1
        if (pred != 'no_relation') and (label != 'no_relation') and (pred == label):
            n_correct += 1
    if n_correct == 0:
        return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
    else:
        prec = n_correct * 1.0 / n_pred
        recall = n_correct * 1.0 / n_gold
        if prec + recall > 0:
            f1 = 2.0 * prec * recall / (prec + recall)
        else:
            f1 = 0.0
        return {'precision': prec, 'recall': recall, 'f1': f1}



regex2type = {}

for regexfilename in ['regexner_caseless.tab', 'regexner_cased.tab']:
    with open(regexfilename, encoding="utf-8") as f:
        for line in f:
            l = line.rstrip('\n')
            l_split = l.split('\t')
            regex = l_split[0].lower()
            if '/' in regex:
                for sp in regex.split('/'):
                    regex2type[sp] = l_split[1]
            else:
                regex2type[regex] = l_split[1]

regex2type['poland'] = 'STATE_OR_PROVINCE'
regex2type['china'] = 'STATE_OR_PROVINCE'
regex2type['canada'] = 'STATE_OR_PROVINCE'
regex2type['mexico'] = 'STATE_OR_PROVINCE'



def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<e1>' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</e1>'

    s[samp['obj_start']] = '<e2>' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</e2>'

    s_detokenize = " ".join(s)

    return {'id': samp['id'], 'token': s_detokenize}



def get_clor_entitis(sent):
    subject_str = sent[sent.find('<e1>') + 4: sent.find('</e1>')]
    object_str = sent[sent.find('<e2>') + 4: sent.find('</e2>')]
    sent = sent.replace("-LRB-", "(")
    sent = sent.replace("-RRB-", ")")
    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))

    return color_sent


def merge_ents_2(ner_list, regex2type):
    text_stack = []
    span_stack = []
    type_stack = []

    ents_types_list = []
    ents_text_list = []
    ents_spans_list = []


    for i, ent in enumerate(ner_list):

        if ent[1] not in type_stack:
            if type_stack != [] and type_stack[0] != 'O':
                assert len(set(type_stack)) == 1, type_stack
                ents_spans_list.append((span_stack[0], span_stack[-1]))
                ents_text_list.append(' '.join(text_stack))
                if ' '.join(text_stack).lower() in regex2type:
                    ents_types_list.append(regex2type[' '.join(text_stack).lower()])
                    # print(regex2type[' '.join(text_stack)])
                else:
                    ents_types_list.append(type_stack[0])

            type_stack = [ent[1]]
            text_stack = [ent[0]]
            span_stack = [i]
        elif ent[1] in type_stack and ent[1] != 'O':
            type_stack.append(ent[1])
            text_stack.append(ent[0])
            span_stack.append(i)

    if text_stack is not [] and type_stack[0] != 'O':
        assert len(set(type_stack)) == 1, type_stack
        ents_spans_list.append((span_stack[0], span_stack[-1]))
        ents_text_list.append(' '.join(text_stack))
        if ' '.join(text_stack).lower() in regex2type:
            ents_types_list.append(regex2type[' '.join(text_stack).lower()])
            # print(regex2type[' '.join(text_stack)])

        else:
            ents_types_list.append(type_stack[0])

    return ents_types_list, ents_text_list, ents_spans_list


def get_number_of_combinations_per_types(ents_list, subj_t, obj_t):
    counter_ents = Counter(ents_list)
    num_of_subj_t = counter_ents[subj_t]
    num_of_obj_t = counter_ents[obj_t]

    if subj_t == obj_t:
        if num_of_subj_t < 2:
            return 0
        else:
            return math.factorial(num_of_subj_t)/math.factorial(num_of_subj_t-2)

    return num_of_subj_t * num_of_obj_t


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end'] + 1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end'] + 1])
    return subj_span, obj_span
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


start_time = time.time()

ENTS_TYPE_BOUND_TO_REL = {('PERSON', 'RELIGION'):'per:religion', ('ORGANIZATION', 'RELIGION'): 'org:political/religious_affiliation',
                          ('PERSON', 'TITLE'): 'per:title',  ('ORGANIZATION', 'CITY'):  'org:city_of_headquarters',  ('PERSON', 'DURATION'): 'per:age'}


str_ENTS_TYPE_BOUND_TO_REL = {str(('PERSON', 'RELIGION')):'per:religion', str(('ORGANIZATION', 'RELIGION')): 'org:political/religious_affiliation',
                          str(('PERSON', 'TITLE')): 'per:title',  str(('ORGANIZATION', 'CITY')):  'org:city_of_headquarters',  str(('PERSON', 'DURATION')): 'per:age'}


with open("/home/nlp/sharos/py_ch/ORGANIZATION_CITY.txt", 'r') as f:
    ORGANIZATION_CITY_annotated_date = f.readlines()

with open("/home/nlp/sharos/py_ch/ORGANIZATION_RELIGION.txt", 'r') as f:
    ORGANIZATION_RELIGION_annotated_date = f.readlines()

with open("/home/nlp/sharos/py_ch/PERSON_DURATION.txt", 'r') as f:
    PERSON_DURATION_annotated_date = f.readlines()

with open("/home/nlp/sharos/py_ch/PERSON_RELIGION.txt", 'r') as f:
    PERSON_RELIGION_annotated_date = f.readlines()

with open("/home/nlp/sharos/py_ch/PERSON_TITLE.txt", 'r') as f:
    PERSON_TITLE_annotated_date = f.readlines()

ALL_annotated_date = ORGANIZATION_CITY_annotated_date + ORGANIZATION_RELIGION_annotated_date + PERSON_DURATION_annotated_date + PERSON_RELIGION_annotated_date + PERSON_TITLE_annotated_date

IS_POSITIVE = False # True # False

NA = "NA"


annotated_data = {}
for l in ALL_annotated_date:
    line_split = l.strip().split('\t')
    if line_split[1] != 'invalid':

        if line_split[1] == "no_relation":
            annotated_data[line_split[0]] = "no_relation"
        else:
            annotated_data[line_split[0]] = str_ENTS_TYPE_BOUND_TO_REL[line_split[1].strip()]
            # print(annotated_data[line_split[0]])




preds_dic =  {}

wiki_list_of_preds = []
distreb_wiki = {}  # defaultdict(int)
combine_sentences_per_id = {}

print("START!!!")




dic_of_pairs_by_list_of_all_predictions = {}

IS_ONLY_MORE_THAN_ONE_PAIR = False

dic_to_save_preds = {}



dic_of_preds = {}
dic_of_true = {}


for fname in ['66', '67', '68', '69', '70', '71', '72']:
    print("fname: ", fname)

    with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_"+fname+".json") as json_file:
        data_examples = json.load(json_file)
        dic_data_examples = {samp['id']: samp for samp in data_examples}

    # with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive__dir_pred/predictions_"+fname+".txt", "r") as f:
    with open("/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/predictions_" + fname + ".txt", "r") as f:
        contents = f.read()
        for i, example in enumerate(contents.splitlines()):
            example_id = example.strip().split("\t")[0]
            pred = example.strip().split("\t")[1]
            wiki_list_of_preds.append(pred)

            curr_data_example = dic_data_examples[example_id].copy()

            curr_data_example['pred'] = pred


            curr_tup = (curr_data_example['subj_type'], curr_data_example['obj_type'])

            if curr_tup in ENTS_TYPE_BOUND_TO_REL:

                if curr_data_example['id'] in annotated_data:

                    if curr_tup not in dic_of_preds:
                        dic_of_preds[curr_tup] = []

                    if curr_tup not in dic_of_true:
                        dic_of_true[curr_tup] = []


                    dic_of_true[curr_tup].append(annotated_data[curr_data_example['id']])

                    if pred == ENTS_TYPE_BOUND_TO_REL[curr_tup]:
                        dic_of_preds[curr_tup].append(pred)
                    else:
                        dic_of_preds[curr_tup].append('no_relation')





                if pred != 'no_relation':

                    if str((curr_data_example['subj_type'], curr_data_example['obj_type'])) not in dic_to_save_preds:
                        dic_to_save_preds[str((curr_data_example['subj_type'], curr_data_example['obj_type']))] = []

                    dic_to_save_preds[str((curr_data_example['subj_type'], curr_data_example['obj_type']))].append(curr_data_example)








for t in dic_of_preds:
    print(t)
    print(len(dic_of_true[t]), len(dic_of_preds[t]))
    print("accuracy_score:", accuracy_score(dic_of_true[t], dic_of_preds[t]))
    print()
    true_positive = sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == ENTS_TYPE_BOUND_TO_REL[t] and y_true == ENTS_TYPE_BOUND_TO_REL[t]])
    false_positive = sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == ENTS_TYPE_BOUND_TO_REL[t] and y_true == "no_relation"])
    true_negative = sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == "no_relation" and y_true == "no_relation"])
    false_negative = sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == "no_relation" and y_true == ENTS_TYPE_BOUND_TO_REL[t]])

    print("true_positive:", true_positive)
    print("false_positive:", false_positive)
    print("true_negative:", true_negative)
    print("false_negative:", false_negative)


    # print("false_positive: ", false_positive)
    # print()
    # print("y_pred_yes", sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == ENTS_TYPE_BOUND_TO_REL[t]]))
    # print("y_true_yes", sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_true == ENTS_TYPE_BOUND_TO_REL[t]]))
    # print()
    # print( "y_pred_no" ,sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_pred == "no_relation"]))
    # print( "y_true_no" ,sum([1 for y_true, y_pred in zip(dic_of_true[t], dic_of_preds[t]) if y_true == "no_relation"]))
    print()
    print(compute_f1(dic_of_preds[t], dic_of_true[t]))
    print("-----------------------------------------")


