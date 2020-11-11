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


with open('/home/nlp/sharos/py_ch/gold_annotations_100_SENTS_TO_EACH_REL.json') as json_file:
    dic_to_annotate = json.load(json_file)

with open("challeng_as_tacred_FIXED.json") as tacred_test_file:
     test_only_challenge_part = json.load(tacred_test_file)

set_ids_test_only_challenge_part = {sample["id"] for sample in test_only_challenge_part}


# SpanBERT trained only on tacred
# with open("/home/nlp/sharos/span_bert/SpanBERT/SpanBERT/out_TACRED_spanbert_large/preds_test_only_challenge_part_BUT_TRAINED_ONLY_ON_TACRED.txt", 'r') as f:
#     annotated_date_tacred = f.readlines()

# know_bert trained only on tacred
with open("/home/nlp/sharos/kb/know_bert_predictions_challenge.txt", 'r') as f:
    annotated_date_tacred = f.readlines()

print(len(annotated_date_tacred))
print(len(test_only_challenge_part))
print("SASSSS")


pred_data = {}
for s, p in zip(test_only_challenge_part, annotated_date_tacred):
    # line_split = l.split()
    p_strip = p.strip().split()[-1]
    pred_data[s["id"]] = p_strip
    # print("aaaaaa" + p_strip + "bbbbbbb")
    # print(p.strip().split()[0], s["id"])
    # if p.strip().split()[0] != s["id"]:
    #     print("AAAAAAAAAAAAA")
    #     print(p.strip().split()[0])
    #     print(s["id"])
    #     print("Dfs"[4234])

with open("challeng_as_tacred_100_sents_per_rel_FINAL.json") as tacred_test_file:
    test_only_challenge_part_2 = json.load(tacred_test_file)


ids_of_100_per_rel = {ts["id"] for ts in test_only_challenge_part_2}

with open("/home/nlp/sharos/kb2/kb/preds_test_only_challenge_part_BUT_TRAINED_ONLY_ON_TACRED_ONLY_100.txt", "w") as f:
    for ex_id in pred_data:
        if ex_id in ids_of_100_per_rel:
            f.write("%s\t%s\n" % (ex_id, pred_data[ex_id]))

print("BBBBB")
print(len(ids_of_100_per_rel))
print(len(test_only_challenge_part_2))
print(len(pred_data))




ssss = set()
for eee in test_only_challenge_part_2:
    if eee["id"] in ssss:
        print(eee["id"])
    ssss.add(eee["id"])










