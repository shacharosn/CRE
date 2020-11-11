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

NEW_SHORT_ALL_RELATIONS_TYPES = {'org:founded_by': {('ORGANIZATION', 'PERSON')}, 'per:employee_of': {('PERSON', 'ORGANIZATION'), ('PERSON', 'LOCATION')},
        'org:alternate_names': {('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:cities_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')},
        'per:children': {('PERSON', 'PERSON')}, 'per:title': {('PERSON', 'TITLE')}, 'per:siblings': {('PERSON', 'PERSON')}, 'per:religion': {('PERSON', 'RELIGION')},
        'per:age': {('PERSON', 'NUMBER'), ('PERSON', 'DURATION')}, 'org:website': {('ORGANIZATION', 'URL')}, 'per:stateorprovinces_of_residence': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:member_of': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'org:top_members/employees': {('ORGANIZATION', 'PERSON')}, 'per:countries_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')},
        'org:city_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'CITY')}, 'org:members': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:country_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'COUNTRY')}, 'per:spouse': {('PERSON', 'PERSON')},
        'org:stateorprovince_of_headquarters': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION')}, 'org:number_of_employees/members': {('ORGANIZATION', 'NUMBER')},
        'org:parents': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:subsidiaries': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'per:origin': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'org:political/religious_affiliation': {('ORGANIZATION', 'RELIGION'), ('ORGANIZATION', 'IDEOLOGY')},
        'per:other_family': {('PERSON', 'PERSON')}, 'per:stateorprovince_of_birth': {('PERSON', 'STATE_OR_PROVINCE')}, 'org:dissolved': {('ORGANIZATION', 'DATE')},
        'per:date_of_death': {('PERSON', 'DATE')}, 'org:shareholders': {('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:alternate_names': {('PERSON', 'MISC'), ('PERSON', 'PERSON')},
        'per:parents': {('PERSON', 'PERSON')}, 'per:schools_attended': {('PERSON', 'ORGANIZATION')}, 'per:cause_of_death': {('PERSON', 'CAUSE_OF_DEATH')},
        'per:city_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:stateorprovince_of_death': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:founded': {('ORGANIZATION', 'DATE')}, 'per:country_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'per:date_of_birth': {('PERSON', 'DATE')},
        'per:city_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:charges': {('PERSON', 'CRIMINAL_CHARGE')},
        'per:country_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}}



set_of_all_ents_pairs = {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'NUMBER'), ('ORGANIZATION', 'URL'), ('PERSON', 'CRIMINAL_CHARGE'),
                         ('PERSON', 'DURATION'), ('PERSON', 'CITY'), ('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'COUNTRY'),
                         ('ORGANIZATION', 'LOCATION'), ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'MISC'), ('PERSON', 'TITLE'), ('ORGANIZATION', 'PERSON'),
                         ('PERSON', 'COUNTRY'), ('ORGANIZATION', 'DATE'), ('PERSON', 'DATE'), ('ORGANIZATION', 'IDEOLOGY'), ('ORGANIZATION', 'CITY'),
                         ('ORGANIZATION', 'RELIGION'), ('PERSON', 'RELIGION'), ('PERSON', 'ORGANIZATION'), ('PERSON', 'NUMBER'), ('PERSON', 'NATIONALITY'),
                         ('PERSON', 'MISC'), ('PERSON', 'PERSON'), ('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')}




ALL_PAIRS_TYPES_ASSIGNED_TO_ONE_REL = {('PERSON', 'RELIGION'), ('PERSON', 'CRIMINAL_CHARGE'), ('PERSON', 'MISC'), ('PERSON', 'TITLE'),
                                      ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'RELIGION'), ('PERSON', 'NUMBER'), ('ORGANIZATION', 'URL'),
                                      ('PERSON', 'DURATION'), ('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'NUMBER'), ('ORGANIZATION', 'CITY'), ('ORGANIZATION', 'IDEOLOGY')}

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




preds_dic =  {}

wiki_list_of_preds = []
distreb_wiki = {}  # defaultdict(int)
combine_sentences_per_id = {}

print("START!!!")

ENTS_TYPE_BOUND_TO_REL = {('PERSON', 'RELIGION'):'per:religion', ('ORGANIZATION', 'RELIGION'): 'org:political/religious_affiliation',
                          ('PERSON', 'TITLE'): 'per:title',  ('ORGANIZATION', 'CITY'):  'org:city_of_headquarters',  ('PERSON', 'DURATION'): 'per:age'}


str_ENTS_TYPE_BOUND_TO_REL = {str(('PERSON', 'RELIGION')):'per:religion', str(('ORGANIZATION', 'RELIGION')): 'org:political/religious_affiliation',
                          str(('PERSON', 'TITLE')): 'per:title',  str(('ORGANIZATION', 'CITY')):  'org:city_of_headquarters',  str(('PERSON', 'DURATION')): 'per:age'}




y_true_by_pair = {}

for tup in ENTS_TYPE_BOUND_TO_REL:
    y_true_by_pair[tup] = {}

    REL_TO_ANNOTATE = str(tup)
    FILE_TO_WRITE = tup[0] + "_" + tup[1] + "_ROBERTA.txt"
    # FILE_TO_WRITE = tup[0] + "_" + tup[1] + ".txt"


    with open(FILE_TO_WRITE, 'r') as f:
        annotated_date_tacred = f.readlines()

    for l in annotated_date_tacred:
        line_split = l.strip().split('\t')
        if line_split[1] != 'invalid':
            y_true_by_pair[tup][line_split[0]] = line_split[1]
            # if line_split[1] == "no_relation":
            #     y_true_by_pair[tup][line_split[0]] = line_split[1]
            # else:
            #     y_true_by_pair[tup][line_split[0]] = str_ENTS_TYPE_BOUND_TO_REL[line_split[1]]

    print(tup)
    print(len(y_true_by_pair[tup]))
    print("sum:", sum([1 for y in y_true_by_pair[tup] if y_true_by_pair[tup][y] != "no_relation"]))
    print("----------------------------------------------------")
    print()


dic_of_pairs_by_list_of_all_predictions = {}

IS_ONLY_MORE_THAN_ONE_PAIR = True

dic_to_save_preds = {}



count_number_of_pairs_in_sent = {}

total_more_than_once = 0
total_only_once = 0

total_more_than_once_2 = 0
total_only_once_2 = 0
total_only_twice_2 = 0

set_of_all_sents = set()



y_pred_by_pair = {}





for fname in ['66', '67', '68', '69', '70', '71', '72']:
    print("fname: ", fname)

    with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_"+fname+".json") as json_file:
        data_examples = json.load(json_file)
        dic_data_examples = {samp['id']: samp for samp in data_examples}

    with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive__dir_pred/predictions_"+fname+".txt", "r") as f:
    # with open("/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/predictions_" + fname + ".txt", "r") as f:
        contents = f.read()
        for i, example in enumerate(contents.splitlines()):
            example_id = example.strip().split("\t")[0]
            pred = example.strip().split("\t")[1]
            wiki_list_of_preds.append(pred)

            curr_data_example = dic_data_examples[example_id].copy()

            curr_data_example['pred'] = pred




            curr_sent_tup = tuple(curr_data_example['token'] + [curr_data_example['subj_type'] + curr_data_example['obj_type']])

            # if curr_sent_tup in set_of_all_sents:
            #     continue

            set_of_all_sents.add(curr_sent_tup)

            if (curr_data_example['subj_type'], curr_data_example['obj_type']) in set_of_all_ents_pairs:

                if IS_ONLY_MORE_THAN_ONE_PAIR:

                    ner_list_word_and_type = [[tok, e_type] for tok, e_type in zip(curr_data_example['token'], curr_data_example['stanford_ner'])]
                    ents_types_list, ents_text_list, entity_spans = merge_ents_2(ner_list_word_and_type, regex2type)  # TODO
                    curr_number_of_combinations_per_types = get_number_of_combinations_per_types(ents_types_list, curr_data_example['subj_type'], curr_data_example['obj_type'])

                    if curr_number_of_combinations_per_types == 1:
                        total_only_once_2 += 1
                    elif curr_number_of_combinations_per_types > 1:
                        total_more_than_once_2 += 1

                    if curr_number_of_combinations_per_types == 2:
                        total_only_twice_2 += 1



                    # if curr_number_of_combinations_per_types > 30:
                    #     print(get_clor_entitis(make_readable_sampl(curr_data_example)['token']))
                    #     print()


                    if (curr_data_example['subj_type'], curr_data_example['obj_type']) not in count_number_of_pairs_in_sent:
                        count_number_of_pairs_in_sent[(curr_data_example['subj_type'], curr_data_example['obj_type'])] = []

                    count_number_of_pairs_in_sent[(curr_data_example['subj_type'], curr_data_example['obj_type'])].append(curr_number_of_combinations_per_types)

                    # if curr_number_of_combinations_per_types < 2:
                    #     continue



                if (curr_data_example['subj_type'], curr_data_example['obj_type']) not in dic_of_pairs_by_list_of_all_predictions:
                    dic_of_pairs_by_list_of_all_predictions[(curr_data_example['subj_type'], curr_data_example['obj_type'])] = []

                dic_of_pairs_by_list_of_all_predictions[(curr_data_example['subj_type'], curr_data_example['obj_type'])].append(pred)




                if (curr_data_example['subj_type'], curr_data_example['obj_type']) in ENTS_TYPE_BOUND_TO_REL:

                    if (curr_data_example['subj_type'], curr_data_example['obj_type']) not in y_pred_by_pair:
                        y_pred_by_pair[(curr_data_example['subj_type'], curr_data_example['obj_type'])] = {}

                    y_pred_by_pair[(curr_data_example['subj_type'], curr_data_example['obj_type'])][curr_data_example['id']] = pred



                    if pred != 'no_relation':#ENTS_TYPE_BOUND_TO_REL[(curr_data_example['subj_type'], curr_data_example['obj_type'])]:

                        if str((curr_data_example['subj_type'], curr_data_example['obj_type'])) not in dic_to_save_preds:
                            dic_to_save_preds[str((curr_data_example['subj_type'], curr_data_example['obj_type']))] = []

                        dic_to_save_preds[str((curr_data_example['subj_type'], curr_data_example['obj_type']))].append(curr_data_example)



    total_more_than_once = 0
    total_only_once = 0

    for pair in count_number_of_pairs_in_sent:
        counter_list = Counter(count_number_of_pairs_in_sent[pair])
        print()
        print("1. ", pair)
        print()
        print("2. ", counter_list)
        print()
        only_once = counter_list[1]
        more_than_once = sum([counter_list[i] for i in counter_list if i != 1])

        total_only_once += only_once
        total_more_than_once += more_than_once


        print("3. only once", only_once, "({} %)".format(round(only_once / (only_once + more_than_once), 2)))
        print()
        print("4. only once", more_than_once, "({} %)".format(round(more_than_once / (only_once + more_than_once), 2)))
        print("-----------------------------------------------------------------------------")
        print()

    print("total_only_once:",total_only_once, "total_more_than_once:", total_more_than_once)
    print()
    print("NUMBER OF SENTENCES: ", len(set_of_all_sents))
    print()
    print("total_more_than_once_2:", total_more_than_once_2)
    print("total_only_once_2:", total_only_once_2)
    print("total_only_twice_2:", total_only_twice_2)
    print()






for tup in y_true_by_pair:
    curr_y_true = [y_true_by_pair[tup][iidd] for iidd in y_true_by_pair[tup]]
    temp_curr_y_pred = [y_pred_by_pair[tup][iidd] for iidd in y_true_by_pair[tup]]
    curr_y_pred = []
    for y_p in temp_curr_y_pred:
        if y_p == ENTS_TYPE_BOUND_TO_REL[tup]:
            curr_y_pred.append(y_p)
        else:
            curr_y_pred.append("no_relation")

    true_positive = sum([1 for y_p, y_t in zip(curr_y_pred, curr_y_true) if y_p == y_t and y_t != "no_relation"])
    false_positive = sum([1 for y_p, y_t in zip(curr_y_pred, curr_y_true) if y_p != "no_relation" and y_p != y_t])
    true_negative = sum([1 for y_p, y_t in zip(curr_y_pred, curr_y_true) if y_p == y_t and y_t == "no_relation"])
    false_negative = sum([1 for y_p, y_t in zip(curr_y_pred, curr_y_true) if y_p == "no_relation" and y_t != "no_relation"])

    num_of_positive_examples = sum([1 for y_t in curr_y_true if y_t == ENTS_TYPE_BOUND_TO_REL[tup]])
    num_of_negative_examples = sum([1 for y_t in curr_y_true if y_t != ENTS_TYPE_BOUND_TO_REL[tup]])

    print(tup)
    print(ENTS_TYPE_BOUND_TO_REL[tup])
    print()
    print("accuracy_score: ", accuracy_score(curr_y_true, curr_y_pred))
    print()

    print("true_positive:  ", true_positive)
    print("false_positive:  ", false_positive)
    print("true_negative:  ", true_negative)
    print("false_negative:  ", false_negative)
    print()
    print(compute_f1(curr_y_pred, curr_y_true))
    print()
    print(len(curr_y_true))



#     for pair in dic_of_pairs_by_list_of_all_predictions:
#         counter_list = Counter(dic_of_pairs_by_list_of_all_predictions[pair])
#         print()
#         print("1. ", pair)
#         print()
#         print("2. ", counter_list)
#         # print("Number of different relations: ", len(counter_list) - 1)
#         print()
#         print("3. ", "%  ", [(curr_pred, round(counter_list[curr_pred] * 100.0 / len(dic_of_pairs_by_list_of_all_predictions[pair]),2)) for curr_pred, curr_count in counter_list.most_common()])
#         filtered_list_whithout_no_relation = [ppp for ppp in dic_of_pairs_by_list_of_all_predictions[pair] if ppp != 'no_relation']
#         filtered_counter_list_whithout_no_relation = Counter(filtered_list_whithout_no_relation)
#         most_comm = filtered_counter_list_whithout_no_relation.most_common(1)[0]
#         print()
#         print("4. ",most_comm[0], round(most_comm[1]*100.0 / len(filtered_list_whithout_no_relation), 2))
#         print("-----------------------------------------------------------------------------")
#         print()
#
#
#
#
#

# with open('unambiguous_ents_types_ROBERTA.json', 'w') as outfile:
#     json.dump(dic_to_save_preds, outfile)