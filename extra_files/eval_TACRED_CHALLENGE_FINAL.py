import json
from termcolor import colored
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from collections import Counter


NO_RELATION = "no_relation"

def compute_f1(preds, labels):
    n_gold = n_pred = n_correct = 0
    for pred, label in zip(preds, labels):
        if pred != NO_RELATION:
            n_pred += 1
        if label != NO_RELATION:
            n_gold += 1
        if (pred != NO_RELATION) and (label != NO_RELATION) and (pred == label):
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
    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))
    sent = sent.replace("-LRB-", "(")
    sent = sent.replace("-RRB-", ")")

    return color_sent


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return subj_span, obj_span


with open('gold_annotations_100_SENTS_TO_EACH_REL_FINAL.json', "r") as json_file:
    dic_to_annotate = json.load(json_file)

with open("challeng_as_tacred_100_sents_per_rel_FINAL.json", "r") as tacred_test_file:
    test_only_challenge_part = json.load(tacred_test_file)


with open("/home/nlp/sharos/kb2/kb/preds_test_only_challenge_part_BUT_TRAINED_ONLY_ON_TACRED_ONLY_100.txt", "r") as f:
    annotated_date_tacred = f.readlines()


pred_data = {}
for l in annotated_date_tacred:
    line_split = l.split()
    pred_data[line_split[0]] = line_split[1]


true_y = []
pred_y = []

for row in test_only_challenge_part:

    true_y.append(row['gold_relation'])

    if pred_data[row['id']] == row['id_relation']:

        pred_y.append(row['id_relation'])
    else:
        pred_y.append(NO_RELATION)


true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

for row, pp, tt in zip(test_only_challenge_part, pred_y, true_y):

    curr_id_relation = row["id_relation"]

    true_positive += 1  if pp == curr_id_relation and tt == curr_id_relation else 0
    false_positive += 1 if pp == curr_id_relation and tt != curr_id_relation else 0
    true_negative += 1  if pp != curr_id_relation and tt != curr_id_relation else 0
    false_negative += 1 if pp != curr_id_relation and tt == curr_id_relation else 0

    # print(row['id_relation'], get_clor_entitis(make_readable_sampl(row)['token']))


print("ACCURACY:   {:.2%} \n".format(accuracy_score(true_y, pred_y)))


total_accuracy_score_positive_3 = true_positive / (true_positive + false_negative)
total_accuracy_score_negative_3 = true_negative / (false_positive + true_negative)

print("POSITIVE ACCURACY:   {:.2%} \n".format(total_accuracy_score_positive_3))
print("NEGATIVE ACCURACY:   {:.2%} \n".format(total_accuracy_score_negative_3))

print("-------------------------------------------------------------------\n")

number_of_examples = len(true_y)

print("TRUE POSITIVE:   {:.3f} \t\t (NUMBER:   {})\n".format(true_positive / number_of_examples, true_positive))
print("TRUE POSITIVE:   {:.3f} \t\t (NUMBER:   {})\n".format(false_positive / number_of_examples, false_positive))
print("TRUE POSITIVE:   {:.3f} \t\t (NUMBER:   {})\n".format(true_negative / number_of_examples, true_negative))
print("TRUE POSITIVE:   {:.3f} \t\t (NUMBER:   {})\n".format(false_negative / number_of_examples, false_negative))

print("-------------------------------------------------------------------\n")

f1 = compute_f1(pred_y, true_y)

print("Precision: {:.2%}\t Recall: {:.2%}\t  F1: {:.2%}\n".format(f1["precision"], f1["recall"], f1["f1"]))






