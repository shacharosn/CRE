import json
from termcolor import colored
import pickle
import random
from collections import Counter
import json
from termcolor import colored
import pickle
import os
from os import listdir
from os.path import isfile, join
from sklearn.metrics import classification_report
from collections import Counter
import numpy as np
from sklearn.metrics import accuracy_score
from random import randrange


high = ['org:political/religious_affiliation', 'per:alternate_names', 'per:stateorprovince_of_birth', 'per:other_family', 'org:parents',
        'per:spouse', 'per:religion', 'per:city_of_death', 'per:city_of_birth', 'org:country_of_headquarters', 'per:date_of_birth', 'org:founded_by']




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
    #     sent = sent.replace("-LRB-", "(")
    #     sent = sent.replace("-RRB-", ")")
    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))
    sent = sent.replace("-LRB-", "(")
    sent = sent.replace("-RRB-", ")")

    return color_sent


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return subj_span, obj_span


with open('gold_annotations.json') as json_file:
    dic_to_annotate = json.load(json_file)



num_of_combination_per_rel = {}
num_of_combination_total = []
num_of_total_examples = 0


no_one_true_gold_rel = {}
at_least_one_true_rel = {}
more_than_one_pred_rel = {}

num_of_share_arg = 0

list_of_num_of_rels_per_sentence = []

num_of_sents = {}

count_only_one_relation_in_sent_that_is_no_relation = 0
num_of_total_sents = 0
total_at_least_one_true_rel = 0

num_of_tokens = []

dic_gold_positive_per_rel = {}
dic_gold_negative_per_rel = {}


num_of_sents_to_check = 0
num_of_examples_to_check = 0



for rel in dic_to_annotate:

    num_of_combination_per_rel[rel] = []
    no_one_true_gold_rel[rel] = 0
    at_least_one_true_rel[rel] = 0
    more_than_one_pred_rel[rel] = 0
    num_of_sents[rel] = 0

    dic_gold_positive_per_rel[rel] = 0
    dic_gold_negative_per_rel[rel] = 0


    for num in dic_to_annotate[rel]:

        for idx_sents, batch in enumerate(dic_to_annotate[rel][num]):

            if num_of_sents[rel] >= 100:
                continue

            num_of_tokens.append(len(batch[0]['token']))

            num_of_sents[rel] += 1

            if num_of_sents[rel] > 100:
                aaaa = idx_sents
                print(num_of_sents[rel])

            num_of_total_sents += 1

            assert len(batch) == int(num)

            num_of_combination_per_rel[rel].append(len(batch))
            num_of_combination_total.append(len(batch))

            batch_pred_rel = sum([1 for tss in batch if tss['pred'] == rel])
            batch_true_rel = sum([1 for tss in batch if tss['gold'] == rel])
            all_rels_in_the_sent = set([tss['gold'] for tss in batch])

            dic_gold_positive_per_rel[rel] += sum([1 for tss in batch if tss['gold'] == rel])
            dic_gold_negative_per_rel[rel] += sum([1 for tss in batch if tss['gold'] != rel])


            list_of_num_of_rels_per_sentence.append(len(all_rels_in_the_sent))
            if len(all_rels_in_the_sent) == 1 and all_rels_in_the_sent == {"no_relation"}:
                count_only_one_relation_in_sent_that_is_no_relation += 1

            cur_set_of_ents = set()
            for tss in batch:
                num_of_total_examples += 1
                if tss['pred'] == rel:
                    curr_subj, curr_obj = get_span_of_subj_obj(tss)
                    cur_set_of_ents.add(curr_subj)
                    cur_set_of_ents.add(curr_obj)

            if len(cur_set_of_ents) < 4:
                num_of_share_arg += 1


            rand_num = randrange(10)
            if rand_num == 3:
                num_of_sents_to_check += 1
                print(rel)
                for tss in batch:
                    print(get_clor_entitis(make_readable_sampl(tss)['token']), tss["gold"])
                    num_of_examples_to_check += 1
                    print()
                print("------------------")

            r""" get sents with some attributes """
            # if int(num) == 4:
            #     if batch_true_rel < 2 and batch_pred_rel > 1:
            #         print("ABCDEFG")
            #         for tss in batch:
            #             print(tss['pred'], get_clor_entitis(make_readable_sampl(tss)['token']), tss["gold"])
            #             print()
            #         print("------------------")



            if batch_true_rel == 0:
                no_one_true_gold_rel[rel] += 1


            if batch_true_rel > 0:
                at_least_one_true_rel[rel] += 1
                total_at_least_one_true_rel += 1

            if batch_pred_rel > 1:
                more_than_one_pred_rel[rel] += 1






for rel in num_of_combination_per_rel:

    assert len(num_of_combination_per_rel[rel]) >= 100

    print(rel)
    print()
    print(Counter(num_of_combination_per_rel[rel]))
    print("no_one_true_gold_rel", no_one_true_gold_rel[rel])
    print()
    print("more_than_one_pred_rel", more_than_one_pred_rel[rel])
    assert len(num_of_combination_per_rel[rel]) == more_than_one_pred_rel[rel]
    print("--------------------------------------------")



print("no_one_true_gold_rel: ", no_one_true_gold_rel)
print()
print("TOTAL_no_one_true_gold_rel: ", sum([no_one_true_gold_rel[r] for r in no_one_true_gold_rel]))
print()
print("num_of_combination_total", Counter(num_of_combination_total).most_common())

print()

print("num_of_share_arg", num_of_share_arg)

print()

print("len(list_of_num_of_rels_per_sentence)", len(list_of_num_of_rels_per_sentence))
print("Counter(list_of_num_of_rels_per_sentence)", Counter(list_of_num_of_rels_per_sentence))
print(sum([1 for i in list_of_num_of_rels_per_sentence if i > 1]))
print(num_of_sents)
print(sum([num_of_sents[i] for i in num_of_sents]))
print(count_only_one_relation_in_sent_that_is_no_relation)
print()
print("num_of_total_sents: ", num_of_total_sents)
print()
print("total_at_least_one_pred_rel: ", total_at_least_one_true_rel)
print()
print(at_least_one_true_rel)

rels_to_print = []
for rel in dic_to_annotate:
    rels_to_print.append(rel)

print(rels_to_print)
print(len(rels_to_print))
print()
print("num_of_tokens: ", sum(num_of_tokens)/len(num_of_tokens))



all_pos = sum([dic_gold_positive_per_rel[r] for r in dic_gold_positive_per_rel])
all_neg = sum([dic_gold_negative_per_rel[r] for r in dic_gold_negative_per_rel])

print()
print("all_pos:", all_pos, all_pos*100/(all_pos+all_neg))
print("all_neg:", all_neg, all_neg*100/(all_pos+all_neg))
print("all_pos+all_neg:", all_pos+all_neg)
print()
for iii, r in enumerate(dic_gold_positive_per_rel):
    print(r, dic_gold_positive_per_rel[r], dic_gold_negative_per_rel[r])
    print()



print("num_of_sents_to_check:", num_of_sents_to_check)
print()
print("num_of_examples_to_check:", num_of_examples_to_check)
print()
print("num_of_total_examples:", num_of_total_examples)

