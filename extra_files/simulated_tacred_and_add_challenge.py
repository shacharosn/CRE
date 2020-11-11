import json
from sklearn.metrics import classification_report
import string
from sklearn.metrics import accuracy_score
from collections import Counter

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




with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples = json.load(tacred_test_file)

with open('gold_annotations.json') as json_file:
    gold_annotations_challenge = json.load(json_file)


# with open("/home/nlp/sharos/span_bert/SpanBERT/SpanBERT/out_tacred/tacred/predictions.txt", 'r') as f:
#     annotated_date_tacred = f.readlines()

# with open("../span_bert/SpanBERT/bert_big_size_tacred_dir/predictions.txt", 'r') as f:
#     annotated_date_tacred = f.readlines()

# with open("../span_bert/SpanBERT/RoBERTa_baseline_TACRED/predictions.txt", 'r') as f:
#     annotated_date_tacred = f.readlines()

with open("/home/nlp/sharos/kb/know_bert_predictions_TACRED.txt", 'r') as f:
    annotated_date_tacred = f.readlines()


#spanbert
# with open("/home/nlp/sharos/span_bert/SpanBERT/SpanBERT/out_tacred/tacred/predictions_challenge.txt", 'r') as f:
#     challenge_annotated_date_tacred = f.readlines()


# with open("../span_bert/SpanBERT/bert_big_size_tacred_dir/predictions_challenge.txt", 'r') as f:
#     challenge_annotated_date_tacred = f.readlines()

with open("/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/predictions_challenge.txt", 'r') as f:
    challenge_annotated_date_tacred = f.readlines()



IS_POSITIVE = True # True # False

NA = "NA"


annotated_data = {}
for l in annotated_date_tacred + challenge_annotated_date_tacred:
    line_split = l.split()
    if line_split[1] != 'invalid':
        annotated_data[line_split[0]] = line_split[1]


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

    y_true__by_rel[rel] = []
    y_pred_by_rel[rel] = []

    dic_of_set2rel = {}

    # if rel not in gold_annotations_challenge:
    #     continue

    curr_rel_challenge_samples = []
    if rel in gold_annotations_challenge:
        for num in gold_annotations_challenge[rel]:
            for idx_sents, batch in enumerate(gold_annotations_challenge[rel][num]):
                for index, ts in enumerate(batch, 1):
                    temp_samp = ts.copy()
                    temp_samp["relation"] = ts["gold"]

                    if IS_POSITIVE:
                        if ts["gold"] != "no_relation":
                            curr_rel_challenge_samples.append(temp_samp)

                    else:
                        if ts["gold"] == "no_relation":
                            curr_rel_challenge_samples.append(temp_samp)




    for samp in tacred_real_samples+curr_rel_challenge_samples:

        if (samp['subj_type'], samp['obj_type']) not in ALL_RELATIONS_TYPES[rel]:
            continue

        curr_sent_tup = tuple(samp['token'] + [samp['subj_type'] + samp['obj_type'] + rel])
        sent_of_sentences_concat_rel.add(curr_sent_tup)

        if curr_sent_tup not in dic_of_set2rel:
            dic_of_set2rel[curr_sent_tup] = set()

        dic_of_set2rel[curr_sent_tup].add(samp['relation'])


        if samp['relation'] == rel:
            y_true__by_rel[rel].append(rel)
            # dic_of_set2rel[curr_sent_tup].add(rel)
        else:
            y_true__by_rel[rel].append(NA)
            # dic_of_set2rel[curr_sent_tup].add(NA)

        if annotated_data[samp['id']] == rel:
            y_pred_by_rel[rel].append(rel)
        else:
            y_pred_by_rel[rel].append(NA)

    y_true_total += y_true__by_rel[rel]
    y_pred_total += y_pred_by_rel[rel]







    # print(classification_report(y_true__by_rel[rel], y_pred_by_rel[rel]))

    total_count_more_than_one_rel += sum([1 for t in dic_of_set2rel if len(dic_of_set2rel[t]) > 1])



    print(rel)
    print()
    print(compute_f1(y_pred_by_rel[rel], y_true__by_rel[rel]))
    print()
    print()
    print()

    true_positive = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == y_t and y_t != NA])
    false_positive = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p != NA and y_t != rel])
    true_negative = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == y_t and y_t == NA])
    false_negative = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_p == NA and y_t != NA])

    num_of_positive_examples = sum([1 for y_t in y_true__by_rel[rel] if y_t == rel])
    num_of_negative_examples = sum([1 for y_t in y_true__by_rel[rel] if y_t != rel])

    print("TRUE POSITIVE:  ", round(true_positive / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", true_positive)
    print()
    print("FALSE POSITIVE:  ", round(false_positive / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", false_positive)
    print()
    print("TRUE NEGATIVE:  ", round(true_negative / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", true_negative)
    print()
    print("FALSE NEGATIVE:  ", round(false_negative / len(y_true__by_rel[rel]), 4), "\t\tNUMBER: ", false_negative)

    print("number of POSITIVE examples:", num_of_positive_examples, "({})".format(round(num_of_positive_examples / (num_of_positive_examples + num_of_negative_examples), 2)))
    print("number of NEGATIVE examples:", num_of_negative_examples, "({})".format(round(num_of_negative_examples / (num_of_positive_examples + num_of_negative_examples), 2)))
    print()

    accuracy_score_positive = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_t != NA and y_p == y_t]) / num_of_positive_examples
    accuracy_score_negative = sum([1 for y_p, y_t in zip(y_pred_by_rel[rel], y_true__by_rel[rel]) if y_t == NA and y_p == y_t]) / num_of_negative_examples
    print("accuracy score positive: ", accuracy_score_positive)
    print()
    print("accuracy negative score: ", accuracy_score_negative)
    print()
    print(print(compute_f1(y_pred_by_rel[rel], y_true__by_rel[rel])))

    print("-------------------------------------------------------------------------")
    print()

    # dic_classification_report = classification_report(y_true__by_rel[rel], y_pred_by_rel[rel], output_dict=True)





total_positive_examples = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t != NA])
total_negative_examples = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t == NA])

total_accuracy_score_positive =  sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t != NA and y_p == y_t]) / total_positive_examples
total_accuracy_score_negative = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_t == NA and y_p == y_t]) / total_negative_examples

print()
print("total_positive_examples:", total_positive_examples, "({})".format(round(total_positive_examples / (total_positive_examples + total_negative_examples),2)))
print("total_negative_examples:", total_negative_examples, "({})".format(round(total_negative_examples / (total_positive_examples + total_negative_examples),2)))

print()




print("total accuracy_score: ", accuracy_score(y_true_total, y_pred_total))
print()
print("accuracy positive: ", total_accuracy_score_positive)
print()
print("accuracy negative : ", total_accuracy_score_negative)

print()
# print(compute_f1())
print()

total_true_positive = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == y_t and y_t != NA ])
total_false_positive = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p != NA and y_t != y_p])
total_true_negative = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == y_t and y_t == NA ])
total_false_negative = sum([1 for y_p, y_t in zip(y_pred_total, y_true_total) if y_p == NA and y_t != y_p])





print("TOTAL TRUE POSITIVE:  ",round(total_true_positive / len(y_true_total), 4), "\t\tNUMBER: ", total_true_positive)
print()
print("TOTAL FALSE POSITIVE:  ",round(total_false_positive / len(y_true_total),4), "\t\tNUMBER: ", total_false_positive)
print()
print("TOTAL TRUE NEGATIVE:  ", round(total_true_negative / len(y_true_total), 4), "\t\tNUMBER: ", total_true_negative)
print()
print("TOTAL FALSE NEGATIVE:  ", round(total_false_negative / len(y_true_total), 4), "\t\tNUMBER: ", total_false_negative)

print()

print(compute_f1(y_pred_total, y_true_total))


print()
print("total_count_more_than_one_rel", total_count_more_than_one_rel, total_count_more_than_one_rel / len(sent_of_sentences_concat_rel), len(sent_of_sentences_concat_rel))
