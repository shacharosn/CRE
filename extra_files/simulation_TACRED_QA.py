import json
import re
import string
from collections import defaultdict
from sklearn.metrics import classification_report
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score


ALL_RELATIONS_TYPES = {'per:title': {('PERSON', 'TITLE')}, 'org:top_members/employees': {('ORGANIZATION', 'PERSON')},
                          'org:country_of_headquarters': {('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
                          'per:parents': {('PERSON', 'PERSON')}, 'per:age': {('PERSON', 'NUMBER'), ('PERSON', 'DURATION')},
                          'per:countries_of_residence': {('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY'), ('PERSON', 'LOCATION')},
                          'per:children': {('PERSON', 'PERSON')}, 'org:alternate_names': {('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'ORGANIZATION')},
                          'per:charges': {('PERSON', 'CRIMINAL_CHARGE')}, 'per:cities_of_residence': {('PERSON', 'CITY'), ('PERSON', 'LOCATION')},
                          'per:origin': {('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'org:founded_by': {('ORGANIZATION', 'PERSON')},
                          'per:employee_of': {('PERSON', 'ORGANIZATION'), ('PERSON', 'LOCATION')}, 'per:siblings': {('PERSON', 'PERSON')},
                          'per:alternate_names': {('PERSON', 'MISC'), ('PERSON', 'PERSON')}, 'org:website': {('ORGANIZATION', 'URL')},
                          'per:religion': {('PERSON', 'RELIGION')}, 'per:stateorprovince_of_death': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
                          'org:parents': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
                          'org:subsidiaries': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'LOCATION')}, 'per:other_family': {('PERSON', 'PERSON')},
                          'per:stateorprovinces_of_residence': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
                          'org:members': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')}, 'per:cause_of_death': {('PERSON', 'CAUSE_OF_DEATH')},
                          'org:member_of': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
                          'org:number_of_employees/members': {('ORGANIZATION', 'NUMBER')}, 'per:country_of_birth': {('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')},
                          'org:shareholders': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'PERSON')},
                          'org:stateorprovince_of_headquarters': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION')},
                          'per:city_of_death': {('PERSON', 'CITY'), ('PERSON', 'LOCATION')}, 'per:date_of_birth': {('PERSON', 'DATE')}, 'per:spouse': {('PERSON', 'PERSON')},
                          'org:city_of_headquarters': {('ORGANIZATION', 'CITY'), ('ORGANIZATION', 'LOCATION')}, 'per:date_of_death': {('PERSON', 'DATE')},
                          'per:schools_attended': {('PERSON', 'ORGANIZATION')}, 'org:political/religious_affiliation': {('ORGANIZATION', 'RELIGION')},
                          'per:country_of_death': {('PERSON', 'COUNTRY')}, 'org:founded': {('ORGANIZATION', 'DATE')}, 'per:stateorprovince_of_birth': {('PERSON', 'STATE_OR_PROVINCE')},
                          'per:city_of_birth': {('PERSON', 'CITY')}, 'org:dissolved': {('ORGANIZATION', 'DATE')}}

class RelData:
    def __init__(self):
        self.true_number = 0
        self.algo_pos = 0
        self.algo_correct = 0

    def recall(self):
        if self.true_number == 0:
            return 1
        else:
            return self.algo_correct / self.true_number

    def precision(self):
        if self.algo_pos == 0:
            return 1
        else:
            return self.algo_correct / self.algo_pos

    def f1(self):
        p = self.precision()
        r = self.recall()
        if p == 0 and r == 0:
            return 0
        return 2 * ((p * r) / (p + r))

def normalize_answer(s):

    def remove_articles(text):
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(s))))

def validate_strings(s1, s2):  # see if one string is contained in the other
    s1 = normalize_answer(s1)
    s2 = normalize_answer(s2)
    return s1 in s2 or s2 in s1


def get_rel(q, subj, obj):
    p1 = preds[q['id']]
    if p1 and (validate_strings(p1, subj) or validate_strings(p1, obj)):
        return q['rel']
    else:
        return None


def eval_na(qas, subj, obj, na_probs):
    qas = sorted(qas, key=lambda x: x['id'])
    pred_rels = []
    for i in range(0, len(qas), 2):
        q1 = qas[i]
        q2 = qas[i + 1]
        # if get_rel(q1, subj, obj) and get_rel(q1, subj, obj) == get_rel(q2, subj, obj):
        #     pred_rels.append(get_rel(q1, subj, obj))
        pred_rels.append((get_rel(q1, subj, obj), na_probs[q1['id']]))
        pred_rels.append((get_rel(q2, subj, obj), na_probs[q2['id']]))
    l = list(dict.fromkeys([x for x in pred_rels if x[0]]))
    if not l:
        return []
    l = sorted(l, key=lambda x: x[1])
    return [l[0][0]]

def eval_group(qas, subj, obj):
    qas = sorted(qas, key=lambda x: x['id'])
    pred_rels = []
    for i in range(0, len(qas), 2):
        q1 = qas[i]
        q2 = qas[i + 1]
        # if get_rel(q1, subj, obj) and get_rel(q1, subj, obj) == get_rel(q2, subj, obj):
        #     pred_rels.append(get_rel(q1, subj, obj))
        pred_rels.append(get_rel(q1, subj, obj))
        pred_rels.append(get_rel(q2, subj, obj))
    l = list(dict.fromkeys([x for x in pred_rels if x]))
    if l:
        return [l[0]]
    return []

def eval_single(qas, rels):
    for qa in qas:
        pred = preds[qa['id']]
        # if qa['is_impossible']:
        #     continue
        if pred == '' and qa['is_impossible']:
            continue
        if pred != '' and qa['is_impossible']:
            rels[qa['rel']].algo_pos += 1
            rels[all_rel].algo_pos += 1
            continue

        if pred == '' and not qa['is_impossible']:
            rels[qa['rel']].true_number += 1
            rels[all_rel].true_number += 1
            continue

        if validate_strings(pred, qa['answers'][0][
            'text']):  # pred.lower() == qa['answers'][0]['text'].lower():  # this is good only for the tacred version - we assume single question
            rels[qa['rel']].true_number += 1
            rels[qa['rel']].algo_pos += 1
            rels[qa['rel']].algo_correct += 1
            rels[all_rel].true_number += 1
            rels[all_rel].algo_pos += 1
            rels[all_rel].algo_correct += 1
            continue

        if not pred:
            rels[qa['rel']].true_number += 1
            rels[qa['rel']].algo_pos += 1
            rels[all_rel].true_number += 1
            rels[all_rel].algo_pos += 1
            continue

        else:
            rels[qa['rel']].true_number += 1
            rels[qa['rel']].algo_pos += 1
            rels[all_rel].true_number += 1
            rels[all_rel].algo_pos += 1
            continue

count_pred_maked_na = 0

def trim_preds(preds, na_probs, thresh):
    global count_pred_maked_na
    for k in preds:
        # print(na_probs[k], thresh)
        if na_probs[k] > thresh:
            count_pred_maked_na += 1
            # print("sfsdfdsdf")
            preds[k] = ''
    return preds


def compute_f1(preds, labels):
    n_gold = n_pred = n_correct = 0
    for pred, label in zip(preds, labels):
        if pred != 'NA':
            n_pred += 1
        if label != 'NA':
            n_gold += 1
        if (pred != 'NA') and (label != 'NA') and (pred == label):
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

if __name__ == '__main__':

    with open('gold_annotations.json') as json_file:
        challenge_samples = json.load(json_file)


    # gold_path = 'tac_test_amir.json'
    # pred_path = 'predictions_amir.json'
    # na_probs_path = 'na_probs_amir.json'

    gold_path = 'tac_test_amir.json'

    pred_path = '/home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/out_all_amir/predictions_tac_test_amir.json'
    na_probs_path = '/home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/out_all_amir/null_odds_tac_test_amir.json'

    # pred_path = '/home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/out_all_amir_albert/predictions_tac_test_amir.json'
    # na_probs_path = '/home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/out_all_amir_albert/null_odds_tac_test_amir.json'

    # pred_path = '/home/nlp/sharos/span_bert/SpanBERT/SpanBERT/model_squad2/squad2/predictions.json'
    # na_probs_path = '/home/nlp/sharos/span_bert/SpanBERT/SpanBERT/model_squad2/squad2/na_probs.json'


    with open("../span_bert/SpanBERT/SpanBERT/out_tacred/tacred/predictions.txt", 'r') as f:
        annotated_date_tacred = f.readlines()

    tacred_gold = {}
    for l in annotated_date_tacred:
        line_split = l.split()
        tacred_gold[line_split[0]] = line_split[1]


    with open(gold_path, 'r') as f:
        gold = json.load(f)
        gold = gold['data']

    with open(pred_path, 'r') as f:
        preds = json.load(f)

    with open(na_probs_path, 'r') as f:
        na_probs = json.load(f)





    # for idd in preds:
    #     if preds[idd] != preds2[idd]:
    #         if not preds[idd]:
    #             print("NNNNNAAAAA", preds2[idd])
    #         else:
    #             print("AFSDF",preds[idd], preds2[idd])
    #         print()

    # thresh = -1.530  # train
    # thresh = -2.5  #dev
    thresh = -3.0
    # test
    preds = trim_preds(preds, na_probs, thresh)

    rels = defaultdict(RelData)

    all_rel = 'all_rel'
    counter = 0
    total = 0

    y_true_old = []
    y_pred_old = []
    y_pred_re_model = []
    y_pred_union = []

    y_dic_pred = {}

    for r in gold:
        title = r['title']
        # if title != 'no_relation':
        #     rels[all_rel].true_number += 2
        # rels[title].true_number += 2
        p = r['paragraphs'][0]
        # print(p)
        # if len(p["qas"]) > 0:
        #     print(p["qas"][0]["id_rel"])
        eval_single(p['qas'], rels)

        if title != 'no_relation':
            rels[title].true_number += 1
            rels[all_rel].true_number += 1
        pred_rels = eval_group(p['qas'], p['subj'], p['obj'])

        y_true_old.append(title)
        if pred_rels == []:
            y_pred_old.append('no_relation')
            if p["qas"] == []:
                continue
            # print("AAAAA")
            # print()
            # print(p)
            # print(p["qas"])
            # print()
            y_dic_pred[p["qas"][0]["id_rel"]] = ['no_relation']
        else:
            y_pred_old.append(pred_rels[0])
            y_dic_pred[p["qas"][0]["id_rel"]] = pred_rels.copy()

        if len(y_dic_pred[p["qas"][0]["id_rel"]]) != 1:
            print("GGGGGG"[43242])
            print(y_dic_pred[p["qas"][0]["id_rel"]])


        # if p["qas"][0]["id_rel"] == "098f6fb926448e5c9f0f":
        #     print("QQQQQ")
        #     print(y_dic_pred["098f6fb926448e5c9f0f"])
        #
        # if "098f6fb926448e5c9f0f" in y_dic_pred:
        #     print("QAQAQAQAQA")
        #     print(y_dic_pred["098f6fb926448e5c9f0f"])


        if len(p["qas"]) > 0:
            y_pred_re_model.append(tacred_gold[p["qas"][0]["id_rel"]])
        else:
            y_pred_re_model.append('no_relation')


        if len(pred_rels) >= 2:
            counter += 1
        # pred_rels = eval_na(p['qas'], p['subj'], p['obj'], na_probs)
        if title in pred_rels:
            rels[title].algo_pos += 1
            rels[title].algo_correct += 1
            rels[all_rel].algo_pos += 1
            rels[all_rel].algo_correct += 1
            pred_rels.remove(title)
        for cur_rel in pred_rels:
            rels[cur_rel].algo_pos += 1
            rels[all_rel].algo_pos += 1
        if len(pred_rels) >= 2:
            counter += 1
        total+=1
    for rel, values in rels.items():
        print('{}: p: {}, r:{}, f1:{}'.format(rel, values.precision(), values.recall(), values.f1()))







    with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
        tacred_real_samples = json.load(tacred_test_file)


    print('098f6fb926448e5c9f0f', y_dic_pred['098f6fb926448e5c9f0f'])
    TOY_Y_PRED = []
    TOY_Y_TRUE = []
    for samp in tacred_real_samples:
        if samp["id"] in y_dic_pred:

            if samp["relation"] != "no_relation":
                print(samp["relation"], y_dic_pred[samp["id"]])
                print("Fdfgsdfg")
                xx = samp["id"]
                yy = y_dic_pred[samp["id"]]
                print()


            TOY_Y_TRUE.append("NA" if samp["relation"] == "no_relation" else samp["relation"])
            if samp["relation"] in y_dic_pred[samp["id"]]:
                TOY_Y_PRED.append(samp["relation"])

            else:
                TOY_Y_PRED.append("NA")







    NA = "NA"


    y_true = []
    y_pred = []

    y_true__by_rel = {}
    y_pred_by_rel = {}

    y_true_total = []
    y_pred_total = []

    person_org_no_rel = 0
    things_to_plot = {}

    count_no_rel = 0

    count_true_ia_neg_but_pred_is_rel = 0
    total_count_more_than_one_rel = 0

    sent_of_sentences_concat_rel = set()

    for rel in ALL_RELATIONS_TYPES:
        if rel == 'org:founded_by':
            print(rel)

        y_true__by_rel[rel] = []
        y_pred_by_rel[rel] = []

        dic_of_set2rel = {}

        for samp in tacred_real_samples:

            if (samp['subj_type'], samp['obj_type']) not in ALL_RELATIONS_TYPES[rel]:
                continue

            curr_sent_tup = tuple(samp['token'] + [samp['subj_type'] + samp['obj_type'] + rel])
            sent_of_sentences_concat_rel.add(curr_sent_tup)

            if curr_sent_tup not in dic_of_set2rel:
                dic_of_set2rel[curr_sent_tup] = set()

            dic_of_set2rel[curr_sent_tup].add(samp['relation'])

            if samp['relation'] == rel:
                y_true__by_rel[rel].append(rel)
                aa = rel
                # dic_of_set2rel[curr_sent_tup].add(rel)
            else:
                y_true__by_rel[rel].append(NA)
                aa = NA
                # dic_of_set2rel[curr_sent_tup].add(NA)

            if rel in y_dic_pred[samp['id']]:
                y_pred_by_rel[rel].append(rel)
                bb = rel
                # print("ABXDF")

            else:
                y_pred_by_rel[rel].append(NA)

        y_true_total += y_true__by_rel[rel]
        y_pred_total += y_pred_by_rel[rel]

        # print(classification_report(y_true__by_rel[rel], y_pred_by_rel[rel]))

        total_count_more_than_one_rel += sum([1 for t in dic_of_set2rel if len(dic_of_set2rel[t]) > 1])

        print(rel)
        print()
        print(compute_f1(y_true__by_rel[rel], y_pred_by_rel[rel]))
        print()
        print()
        print()

        true_positive = sum(
            [1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == y_t and y_t != NA])
        false_positive = sum(
            [1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p != NA and y_t != rel])
        true_negative = sum(
            [1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == y_t and y_t == NA])
        false_negative = sum(
            [1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == NA and y_t != NA])

        num_of_positive_examples = sum([1 for y_t in y_true__by_rel[rel] if y_t == rel])
        num_of_negative_examples = sum([1 for y_t in y_true__by_rel[rel] if y_t != rel])

        print("TRUE POSITIVE:  ", round(true_positive / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", true_positive)
        print()
        print("FALSE POSITIVE:  ", round(false_positive / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", false_positive)
        print()
        print("TRUE NEGATIVE:  ", round(true_negative / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", true_negative)
        print()
        print("FALSE NEGATIVE:  ", round(false_negative / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", false_negative)

        print("number of POSITIVE examples:", num_of_positive_examples,
              "({})".format(round(num_of_positive_examples / (num_of_positive_examples + num_of_negative_examples), 2)))
        print("number of NEGATIVE examples:", num_of_negative_examples,
              "({})".format(round(num_of_negative_examples / (num_of_positive_examples + num_of_negative_examples), 2)))
        print()

        accuracy_score_positive = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if
                                       y_t != NA and y_p == y_t]) / num_of_positive_examples
        accuracy_score_negative = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if
                                       y_t == NA and y_p == y_t]) / num_of_negative_examples
        print("accuracy score positive: ", accuracy_score_positive)
        print()
        print("accuracy negative score: ", accuracy_score_negative)
        print("-------------------------------------------------------------------------")
        print()

        # dic_classification_report = classification_report(y_true__by_rel[rel], y_pred_by_rel[rel], output_dict=True)

    total_positive_examples = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t != NA])
    total_negative_examples = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t == NA])

    total_accuracy_score_positive = sum(
        [1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t != NA and y_p == y_t]) / total_positive_examples
    total_accuracy_score_negative = sum(
        [1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t == NA and y_p == y_t]) / total_negative_examples

    print()
    print("total_positive_examples:", total_positive_examples,
          "({})".format(round(total_positive_examples / (total_positive_examples + total_negative_examples), 2)))
    print("total_negative_examples:", total_negative_examples,
          "({})".format(round(total_negative_examples / (total_positive_examples + total_negative_examples), 2)))

    print()

    print("total accuracy_score: ", accuracy_score(y_true_total, y_pred_total))
    print()
    print("accuracy positive: ", total_accuracy_score_positive)
    print()
    print("accuracy negative : ", total_accuracy_score_negative)

    print()

    total_true_positive = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == y_t and y_t != NA])
    total_false_positive = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p != NA and y_t != y_p])
    total_true_negative = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == y_t and y_t == NA])
    total_false_negative = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == NA and y_t != y_p])

    print("TOTAL TRUE POSITIVE:  ", round(total_true_positive / len(y_true_total), 4), "\t\tNUMBER: ",
          total_true_positive)
    print()
    print("TOTAL FALSE POSITIVE:  ", round(total_false_positive / len(y_true_total), 4), "\t\tNUMBER: ",
          total_false_positive)
    print()
    print("TOTAL TRUE NEGATIVE:  ", round(total_true_negative / len(y_true_total), 4), "\t\tNUMBER: ",
          total_true_negative)
    print()
    print("TOTAL FALSE NEGATIVE:  ", round(total_false_negative / len(y_true_total), 4), "\t\tNUMBER: ",
          total_false_negative)

    print()

    print(compute_f1(y_pred_total, y_true_total))

    print()
    print("total_count_more_than_one_rel", total_count_more_than_one_rel,
          total_count_more_than_one_rel / len(sent_of_sentences_concat_rel), len(sent_of_sentences_concat_rel))

