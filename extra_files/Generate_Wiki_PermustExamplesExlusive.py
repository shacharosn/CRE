import json
from collections import Counter
from stanfordcorenlp import StanfordCoreNLP
from termcolor import colored
from tqdm import tqdm

from nltk.tokenize.treebank import TreebankWordDetokenizer
import elasticsearch
import os
from os import listdir
from os.path import isfile, join
import os.path as path
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support
import codecs
import time

import argparse
import uuid


# nlp = StanfordCoreNLP('../span_bert/SpanBERT/stanford-corenlp-full-2018-10-05')
# nlp.close()

count_of_used_regex = 0

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

SET_OF_ALL_TYPES = {('PERSON', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'DATE'),
                    ('PERSON', 'DATE'), ('ORGANIZATION', 'LOCATION'), ('PERSON', 'LOCATION'), ('PERSON', 'NATIONALITY'),
                    ('ORGANIZATION', 'URL'), ('PERSON', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'),
                    ('PERSON', 'CITY'), ('PERSON', 'TITLE'), ('ORGANIZATION', 'CITY'), ('PERSON', 'RELIGION'),
                    ('PERSON', 'CRIMINAL_CHARGE'), ('ORGANIZATION', 'RELIGION'), ('PERSON', 'COUNTRY'),
                    ('ORGANIZATION', 'NUMBER'), ('PERSON', 'PERSON'), ('PERSON', 'NUMBER'),
                    ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'STATE_OR_PROVINCE'), ('PERSON', 'DURATION')}

ID_COUNTER = 0


# def make_model_sample_of_sentece(idd, rel, sss, span_of_subj_obj):
#     tokens = nlp.word_tokenize(sss)
#
#     if tokens.index('<e1>') < tokens.index('<e2>'):
#         subj_start, subj_end = get_start_end_and_clean_sent(tokens, 'e1')
#         obj_start, obj_end = get_start_end_and_clean_sent(tokens, 'e2')
#     else:
#         obj_start, obj_end = get_start_end_and_clean_sent(tokens, 'e2')
#         subj_start, subj_end = get_start_end_and_clean_sent(tokens, 'e1')
#
#     clean_sent = TreebankWordDetokenizer().detokenize(tokens)
#
#     ner = [tok[1] for tok in nlp.ner(clean_sent)]
#     ner  = ['NUMBER' if x == 'DURATION' else x for x in ner]
#
#
#     new_sample = {'id': idd, 'docid': 2, 'relation': rel, 'token': tokens, 'subj_start': subj_start,
#                   'subj_end': subj_end, 'obj_start': obj_start, 'obj_end': obj_end,
#                   'stanford_pos': [tok[1] for tok in nlp.pos_tag(clean_sent)],
#                   'stanford_ner': ner,
#                   'span_of_subj_obj': span_of_subj_obj}
#
#     new_sample['subj_type'] = new_sample['stanford_ner'][subj_start]
#     new_sample['obj_type'] = new_sample['stanford_ner'][obj_start]
#
#
#
#     return new_sample


def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<e1>' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</e1>'

    s[samp['obj_start']] = '<e2>' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</e2>'

    s_detokenize = TreebankWordDetokenizer().detokenize(s)

    s_detokenize = s_detokenize.replace(">>", ">")
    s_detokenize = s_detokenize.replace("<<", "<")

    return {'id': samp['id'], 'relation': samp['relation'], 'token': s_detokenize, 'subj_type': samp['subj_type'],
            'obj_type': samp['obj_type']}


def get_start_end_and_clean_sent(sent, arg_label):
    start_tag = '<' + arg_label + '>'
    end_tag = '</' + arg_label + '>'
    arg_start = sent.index(start_tag)
    sent.remove(start_tag)
    arg_end = sent.index(end_tag) - 1
    sent.remove(end_tag)
    return arg_start, arg_end


def generator_model_input(indxs_subject, indxs_object, wiki_ner_list_all, toks, tacred_id, et_of_subj, et_of_obj):
    global ID_COUNTER
    ID_COUNTER += 1



    new_sample = {'id': tacred_id + "_" + et_of_subj + "_" + et_of_obj + "_" + str(ID_COUNTER), 'docid': 2,
                  'token': toks, 'relation': "no_relation",
                  'subj_start': indxs_subject[0], 'subj_end': indxs_subject[1], 'obj_start': indxs_object[0],
                  'obj_end': indxs_object[1], 'stanford_ner': wiki_ner_list_all, 'subj_type': et_of_subj,
                  'obj_type': et_of_obj}

    return new_sample

def merge_ents_3(ner_list, re):
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
                ents_types_list.append(type_stack[0])
                ents_spans_list.append((span_stack[0], span_stack[-1]))
                ents_text_list.append(' '.join(text_stack))

            type_stack = [ent[1]]
            text_stack = [ent[0]]
            span_stack = [i]
        elif ent[1] in type_stack and ent[1] != 'O':
            type_stack.append(ent[1])
            text_stack.append(ent[0])
            span_stack.append(i)

    if text_stack is not [] and type_stack[0] != 'O':
        assert len(set(type_stack)) == 1, type_stack
        ents_types_list.append(type_stack[0])
        ents_spans_list.append((span_stack[0], span_stack[-1]))
        ents_text_list.append(' '.join(text_stack))

    return ents_types_list, ents_text_list, ents_spans_list


def merge_ents_2(ner_list, regex2type):
    text_stack = []
    span_stack = []
    type_stack = []

    ents_types_list = []
    ents_text_list = []
    ents_spans_list = []

    global count_of_used_regex

    for i, ent in enumerate(ner_list):

        if ent[1] not in type_stack:
            if type_stack != [] and type_stack[0] != 'O':
                assert len(set(type_stack)) == 1, type_stack
                ents_spans_list.append((span_stack[0], span_stack[-1]))
                ents_text_list.append(' '.join(text_stack))
                if ' '.join(text_stack).lower() in regex2type:
                    ents_types_list.append(regex2type[' '.join(text_stack).lower()])
                    count_of_used_regex += 1
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
            count_of_used_regex += 1
            # print(regex2type[' '.join(text_stack)])

        else:
            ents_types_list.append(type_stack[0])

    return ents_types_list, ents_text_list, ents_spans_list


def get_span_of_subj_obj(sample):
    subj_span = sample['token'][sample['subj_start']:sample['subj_end']+1]
    obj_span = sample['token'][sample['obj_start']:sample['obj_end']+1]
    return [subj_span, obj_span]


# with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
#     test_tacred_real_samples = json.load(tacred_test_file)
#
# with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/dev.json") as tacred_dev_file:
#     dev_tacred_real_samples = json.load(tacred_dev_file)

# tacred_real_samples = test_tacred_real_samples + dev_tacred_real_samples

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



count = []
count_ORGANIZATION_PERSON = []  # ['ORGANIZATION', 'PERSON']

count_all = 0

data_examples = []

SENTENCES_SET = set()

FUCK = 0

set_of_ids = set()

files_path = "../span_bert/SpanBERT/yoav_files"
onlyfiles = [join(files_path, f) for f in listdir(files_path) if isfile(join(files_path, f))]

print(onlyfiles[59:60])
# print(onlyfiles[423423])
# ID_IDEXES = "14-23" # onlyfiles[1:11]
# ID_IDEXES = "24-33" # onlyfiles[11:21]
# ID_IDEXES = "34" # onlyfiles[21:22]
# ID_IDEXES = "35" # onlyfiles[22:23]
# ID_IDEXES = "36-45" # onlyfiles[23:33]
# ID_IDEXES = "46" # onlyfiles[33:34]
# ID_IDEXES = "47-51" # onlyfiles[34:39]
# ID_IDEXES = "52-56" # onlyfiles[39:44]
# ID_IDEXES = "57" # onlyfiles[44:45]
# ID_IDEXES = "58" # onlyfiles[45:46]
# ID_IDEXES = "59" # onlyfiles[46:47]
# ID_IDEXES = "60" # onlyfiles[47:48]
# ID_IDEXES = "61" # onlyfiles[48:49]
# ID_IDEXES = "62" # onlyfiles[49:50]
# ID_IDEXES = "64" # onlyfiles[51:52]
# ID_IDEXES = "65" # onlyfiles[52:53]
# ID_IDEXES = "66" # onlyfiles[53:54]
# ID_IDEXES = "67" # onlyfiles[54:55]
# ID_IDEXES = "68" # onlyfiles[55:56]
######################################
# ID_IDEXES = "69" # onlyfiles[56:57]
# ID_IDEXES = "70" # onlyfiles[57:58]
# ID_IDEXES = "71" # onlyfiles[58:59]
ID_IDEXES = "72" # onlyfiles[59:60]



for path in onlyfiles[59:60]:

    all_samps = []

    with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as parsed_wiki_file:
        # parsed_wiki_samples = json.load(parsed_wiki_file)
        for i, samp in enumerate(parsed_wiki_file):
            all_samps.append(samp)

    for samp_idx, samp in tqdm(enumerate(all_samps)):

        # if tuple(samp['token']) in SENTENCES_SET:
        #     continue
        #
        # SENTENCES_SET.add(tuple(samp['token']))
        if FUCK % 70000 == 0:
            print("FUCK: ", FUCK)

        FUCK += 1
        #
        # readable = make_readable_sampl(samp)
        # # print("AAAA")
        # # print()
        # # print(samp['token'])
        # # print()
        # # print("BBB")
        # # print()
        # # print(readable)
        # span_of_subj_obj = get_span_of_subj_obj(samp)

        # model_samp = make_model_sample_of_sentece(readable['id'], readable['relation'], readable['token'], span_of_subj_obj)

        samp2 = [w.split(':') for w in samp.split() if len(w.split(':')) == 3]

        ner_list_word_and_type = [[tok, e_type] for (tok, lem, e_type) in samp2]

        ents_types_list, ents_text_list, entity_spans = merge_ents_2(ner_list_word_and_type, regex2type)  # TODO

        # print("----------------------------------")
        # print(ents_types_list)
        # print()
        # print(ents_text_list)
        # print()
        # print(entity_spans)
        # print("----------------------------------")
        # print()


        while True:
            curr_id = ID_IDEXES +"-"+ str(uuid.uuid4())
            if curr_id not in set_of_ids:
                set_of_ids.add(curr_id)
                break

        for curr_ents in SET_OF_ALL_TYPES:

            curr_num_of_permutations = 0
            curr_num_of_permutations_ORGANIZATION_PERSON = 0
            curr_tup = []

            for i, et_subj in enumerate(ents_types_list):
                if et_subj == curr_ents[0]:

                    indxs_subject = entity_spans[i]

                    for j, et_obj in enumerate(ents_types_list):
                        if et_obj == curr_ents[1] and i != j:

                            if j >= len(entity_spans):
                                print(ents_types_list, ents_text_list, entity_spans)
                                print()
                                print(ner_list_word_and_type)
                            indxs_object = entity_spans[j]

                            curr_num_of_permutations += 1


                            count_all += 1
                            curr_tup.append([str(i) + "_" + et_subj, str(j) + "_" + et_obj])

                            the_new_model_inputs = generator_model_input(indxs_subject, indxs_object,
                                                                         [e_type for (tok, lem, e_type) in samp2],
                                                                         [tok for (tok, lem, e_type) in samp2],
                                                                         curr_id, et_subj, et_obj)

                            data_examples.append(the_new_model_inputs)

            if curr_num_of_permutations != 0:
                count.append(curr_num_of_permutations)


print("count_of_used_regex: ", count_of_used_regex)

print("len(data_examples): ")
print()
print(len(data_examples))

with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_"+ID_IDEXES+".json", "w") as f:
    json.dump(data_examples, f)

# print(count_all)
#
# for cc in count:
#     print(cc)
#
# print(len(count))
#
# print(count)
#
# c = Counter(count_ORGANIZATION_PERSON)
#
# print(c)
# summ = 0
# for c1, c2 in c.items():
#     print(c1, c2)
#     summ += c1 * c2
# print(summ)
# print(len(data_examples))
#
# print("SENTENCES_SET len:  ", SENTENCES_SET)
#
# # nlp.close()