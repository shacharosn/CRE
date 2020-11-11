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
from sklearn.metrics import accuracy_score

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


with open('gold_annotations.json') as json_file:
    dic_to_annotate = json.load(json_file)

# del dic_to_annotate['per:other_family']


with open('tacred_results.json') as json_file:
    tacred_results = json.load(json_file)



count_intersection_empty = 0

batch_counter_per_rel = {}
examples_counter_per_rel = {}

failed_examples = 0

y_true_all_rel = {}
y_pred_all_rel = {}

cnt = Counter()

subj_percentage_of_exclus = []
obj_percentage_of_exclus = []

micro_avg_f1 = []
total_weight = 0

for rel in dic_to_annotate:

    # if rel == "per:alternate_names":
    #     continue0ce21db90818_PERSON_PERSON_1525277

    y_true_all_rel[rel] = []
    y_pred_all_rel[rel] = []

    batch_counter_per_rel[rel] = 0
    examples_counter_per_rel[rel] = 0

    for num in dic_to_annotate[rel]:
        for idx_sents, batch in enumerate(dic_to_annotate[rel][num]):

            if rel == "per:countries_of_residence":
                cnt[len(batch)] += 1


            batch_counter_per_rel[rel] += 1

            if int(num) == 3 and rel != 'per:other_family':
                batch_pred_rel = sum([1 for tss in batch if tss['pred'] == rel])
                batch_true_rel = sum([1 for tss in batch if tss['gold'] == rel])
                if batch_pred_rel == 3 and batch_true_rel == 1:
                    for tss in batch:
                        print(tss['pred'], get_clor_entitis(make_readable_sampl(tss)['token']))
                        print()
                    print("------------------")



            # if int(num) > 3 and rel != 'per:other_family':
            #     batch_pred_rel = sum([1 for tss in batch if tss['pred'] == rel])
            #     batch_true_rel = sum([1 for tss in batch if tss['gold'] == rel])
            #     batch_list_of_sets_subj_obj = [set(get_span_of_subj_obj(tss)) for tss in batch]
            #
            #     if batch[0]['id'] == '35-d5790a8f-8a1b-4f4d-988f-9564347d98bd_ORGANIZATION_DATE_354782':
            #         print("fsdfsdfd")
            #
            #     contain_intersection_empty = False
            #
            #     for i_pair, pair1 in enumerate(batch_list_of_sets_subj_obj):
            #         for j_pair, pair2 in enumerate(batch_list_of_sets_subj_obj):
            #             aaaa = pair1 & pair2
            #             if i_pair != j_pair:
            #                 if pair1 & pair2 == set():
            #                     contain_intersection_empty = True
            #
            #     if contain_intersection_empty:
            #         count_intersection_empty += 1
            #
            #         if batch_pred_rel >= int(num)-1:# and batch_true_rel ==1:
            #             print(rel)
            #             for tss in batch:
            #                 print(tss['id'])
            #                 print(tss['pred'], get_clor_entitis(make_readable_sampl(tss)['token']))
            #                 print()
            #             print("------------------")


            for index, ts in enumerate(batch, 1):

                failed_examples += 1
                examples_counter_per_rel[rel] += 1



                # if rel == 'per:alternate_names':
                #     if ts['gold'] == rel:
                #         print("AAAAAAAAAAA")
                #         print(ts['id'])
                #         print(get_clor_entitis(make_readable_sampl(ts)['token']))
                #         print()

                        # for tttsss in batch:
                        #     print(tttsss['id'], tttsss['pred'])
                        #     print(get_clor_entitis(make_readable_sampl(tttsss)['token']))
                        #     print()

                        # print("------------------")
                y_true_all_rel[rel].append(ts['gold'])

                if ts['pred'] == rel:
                    y_pred_all_rel[rel].append(ts['pred'])
                else:
                    y_pred_all_rel[rel].append("no_relation")


                # make positive/ negative ratio like tacred ! (80% negativ examples)

                # if ts['gold'] == 'no_relation':
                #     y_true_all_rel[rel].append(ts['gold'])
                #     y_true_all_rel[rel].append(ts['gold'])
                #
                #     if ts['pred'] == rel:
                #         y_pred_all_rel[rel].append(ts['pred'])
                #         y_pred_all_rel[rel].append(ts['pred'])
                #     else:
                #         y_pred_all_rel[rel].append("no_relation")
                #         y_pred_all_rel[rel].append("no_relation")


            # print("--------------------------------------------------------------------------------------------------------------------------")

total_positive_examples = 0
total_negative_examples = 0

total_all_rel_y_true = []
total_all_rel_y_pred = []

things_to_plot = {}


for rel in dic_to_annotate:
    # if rel == "per:alternate_names":
    #     continue
    things_to_plot[rel] = {}
    print(rel)
    print()

    true_positive = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_p == rel and y_t == rel])
    false_positive =  sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_p == rel and y_t != rel])
    true_negative = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_p != rel and y_t != rel])
    false_negative = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_p != rel and y_t == rel])


    print(tacred_results[rel])
    print()
    print(Counter(y_true_all_rel[rel]))
    print()
    print(classification_report(y_true_all_rel[rel], y_pred_all_rel[rel]))
    print()

    print("TRUE POSITIVE:  ", round(true_positive / len(y_true_all_rel[rel]), 4), "\t\tNUMBER: ", true_positive)
    print()
    print("FALSE POSITIVE:  ", round(false_positive / len(y_true_all_rel[rel]), 4), "\t\tNUMBER: ", false_positive)
    print()
    print("TRUE NEGATIVE:  ", round(true_negative / len(y_true_all_rel[rel]), 4), "\t\tNUMBER: ", true_negative)
    print()
    print("FALSE NEGATIVE:  ", round(false_negative / len(y_true_all_rel[rel]), 4), "\t\tNUMBER: ", false_negative)


    print()
    print("number of examples:", len(y_pred_all_rel[rel]))
    print()


    number_of_pred_true = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_p == rel])
    percentage_of_pred_true =  round(number_of_pred_true / len(y_true_all_rel[rel]), 4)
    things_to_plot[rel]["percentage_of_pred_true"] = percentage_of_pred_true

    print("percentage_of_pred_true: ", percentage_of_pred_true)
    print()


    things_to_plot[rel]["true_positive"] = round(true_positive / len(y_true_all_rel[rel]), 4)
    things_to_plot[rel]["false_positive"] = round(false_positive / len(y_true_all_rel[rel]), 4)

    num_of_positive_examples = sum([1 for y_t in y_true_all_rel[rel] if y_t == rel])
    num_of_negative_examples = sum([1 for y_t in y_true_all_rel[rel] if y_t != rel])

    total_positive_examples += num_of_positive_examples
    total_negative_examples += num_of_negative_examples


    print("number of POSITIVE examples:", num_of_positive_examples, "({})".format(round(num_of_positive_examples / (num_of_positive_examples+num_of_negative_examples),2)))
    print("number of NEGATIVE examples:", num_of_negative_examples, "({})".format(round(num_of_negative_examples / (num_of_positive_examples+num_of_negative_examples),2)))
    print()
    print("pred true (there is a relation) : ", sum([1 for y_p in y_pred_all_rel[rel] if y_p != 'no_relation']), sum([1 for y_p in y_pred_all_rel[rel] if y_p != 'no_relation']) / len(y_pred_all_rel[rel]))


    assert len(y_pred_all_rel[rel]) == len(y_true_all_rel[rel])

    print()

    accuracy_score_positive = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_t != 'no_relation' and y_p == y_t]) / num_of_positive_examples
    accuracy_score_negative = sum([1 for y_p, y_t in zip(y_pred_all_rel[rel], y_true_all_rel[rel]) if y_t == 'no_relation' and y_p == y_t]) / num_of_negative_examples

    things_to_plot[rel]["accuracy_score_positive"] = accuracy_score_positive
    things_to_plot[rel]["accuracy_score_negative"] = accuracy_score_negative



    print("accuracy score positive: ", accuracy_score_positive)
    print()

    print("accuracy negative score: ", accuracy_score_negative)

    print()

    print(accuracy_score(y_true_all_rel[rel], y_pred_all_rel[rel]))

    print()

    print("compute_f1: ",compute_f1(y_pred_all_rel[rel], y_true_all_rel[rel]))

    dic_classification_report = classification_report(y_true_all_rel[rel], y_pred_all_rel[rel], output_dict=True)
    micro_avg_f1.append(dic_classification_report[rel]['f1-score'] * dic_classification_report[rel]['support'])
    total_weight += dic_classification_report[rel]['support']

    total_all_rel_y_true += y_true_all_rel[rel]
    total_all_rel_y_pred += y_pred_all_rel[rel]

    print(
        "-------------------------------------------------------------------------------------------------------------------")




# print("AAAA")
# for rel in dic_to_annotate:
#     print(rel)

print(len(set([rel for rel in dic_to_annotate])))



print("f1 (accuracy) without 'no_relation':  ", sum([f1 for f1 in micro_avg_f1])/total_weight)



print("total_positive_examples:", total_positive_examples, "({})".format(round(total_positive_examples / (total_positive_examples + total_negative_examples),2)))
print("total_negative_examples:", total_negative_examples, "({})".format(round(total_negative_examples / (total_positive_examples + total_negative_examples),2)))





print("failed_examples:", failed_examples)
print()


print("total accuracy_score: ", accuracy_score(total_all_rel_y_true, total_all_rel_y_pred))

# print()
#
# print("total_positive_examples:", total_positive_examples)
# print("total_negative_examples:", total_negative_examples)

print()
print()

total_accuracy_score_positive =  sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_t != 'no_relation' and y_p == y_t]) / total_positive_examples
total_accuracy_score_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_t == 'no_relation' and y_p == y_t]) / total_negative_examples


print("accuracy positive: ", total_accuracy_score_positive)
print()
print("accuracy negative : ", total_accuracy_score_negative)

total_true_positive = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p != 'no_relation' and y_t != 'no_relation' and y_p == y_t])
total_false_positive = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p != 'no_relation' and y_t == 'no_relation'])
total_true_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p == 'no_relation' and y_t == 'no_relation'])
total_false_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p == 'no_relation' and y_t != 'no_relation'])

print("AAAAAAAAAA")
print(total_false_positive)
print()
print()
print((total_true_positive+total_false_positive+total_true_negative+total_false_negative)/len(total_all_rel_y_true))

print()

print("TOTAL TRUE POSITIVE:  ", round(total_true_positive / len(total_all_rel_y_true), 4), "\t\tNUMBER: ", total_true_positive)
print()
print("TOTAL FALSE POSITIVE:  ", round(total_false_positive / len(total_all_rel_y_true), 4), "\t\tNUMBER: ", total_false_positive)
print()
print("TOTAL TRUE NEGATIVE:  ", round(total_true_negative / len(total_all_rel_y_true), 4), "\t\tNUMBER: ", total_true_negative)
print()
print("TOTAL FALSE NEGATIVE:  ", round(total_false_negative / len(total_all_rel_y_true), 4), "\t\tNUMBER: ", total_false_negative)



things_to_plot["total"] = {}

things_to_plot["total"]["accuracy_score_positive"] = total_accuracy_score_positive
things_to_plot["total"]["accuracy_score_negative"] = total_accuracy_score_negative

things_to_plot["total"]["true_positive"] = round(total_true_positive / len(total_all_rel_y_true), 4)
things_to_plot["total"]["false_positive"] = round(total_false_positive / len(total_all_rel_y_true), 4)

total_number_of_pred_true = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p != 'no_relation'])
total_percentage_of_pred_true = round(total_number_of_pred_true / len(total_all_rel_y_true), 4)
things_to_plot["total"]["percentage_of_pred_true"] = total_percentage_of_pred_true

print()
print("total_percentage_of_pred_true:", total_percentage_of_pred_true)

with open('things_to_plot.json', 'w') as outfile:
    json.dump(things_to_plot, outfile)


# for r in examples_counter_per_rel:
#     print(r, examples_counter_per_rel[r])
#
# print()
# print(cnt)



print("pred true (there is a relation) : " , sum([1 for y_p in total_all_rel_y_pred if y_p != 'no_relation']), sum([1 for y_p in total_all_rel_y_pred if y_p != 'no_relation'])/len(total_all_rel_y_pred))

print(count_intersection_empty)
print()
print(compute_f1(total_all_rel_y_pred, total_all_rel_y_true))
print()
print(len(total_all_rel_y_pred))