import json
from sklearn.metrics import classification_report
import string
from sklearn.metrics import accuracy_score
from collections import Counter
import copy

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
    challenge_dic_to_annotate = json.load(json_file)



with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/train.json") as tacred_test_file:
    tacred_real_samples_train = json.load(tacred_test_file)

with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/dev.json") as tacred_test_file:
    tacred_real_samples_dev = json.load(tacred_test_file)

with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples_test = json.load(tacred_test_file)

# dic_tacred_test = {samp["id"] for iii, samp in enumerate(tacred_real_samples_test)}
#
# with open("/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/data/TACRED_WITH_CHALLENGE_FIX/test.json") as tacred_test_file:
#     tacred_with_challenge_test = json.load(tacred_test_file)
#
# print("tacred_with_challenge_test:", len(tacred_with_challenge_test))



# with open("../span_bert/SpanBERT/RoBERTa_baseline_TACRED/predictions.txt", 'r') as f:
#     annotated_date_tacred = f.readlines()
TO_TRAIN = []
TO_TEST = []
TO_ALL_CHALLENGE = []

NEW_gold_annotations_100_SENTS_TO_EACH_REL = {}
EDITED_NEW_gold_annotations_100_SENTS_TO_EACH_REL = {}

count_b = 0
count_no_relation = 0
count_sent_id = set()

cnt = Counter()
set_of_ids = {}

for rel in challenge_dic_to_annotate:
    count_b = 0
    count_test = 0
    count_train = 0
    num_of_sents = 0
    NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel] = {}
    EDITED_NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel] = {}
    set_of_ids[rel] = set()




    for num in challenge_dic_to_annotate[rel]:

        if num not in NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel]:
            NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel][num] = []

        if num not in EDITED_NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel]:
            EDITED_NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel][num] = []

        for idx_sents, batch in enumerate(challenge_dic_to_annotate[rel][num]):
            if num_of_sents >= 100:
                continue

            cpy_list = []
            for li in batch:
                d2 = copy.deepcopy(li)
                cpy_list.append(d2)

            NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel][num].append(cpy_list)


            count_b += 1
            num_of_sents += 1
            edited_cpy_list = []
            cnt[rel] += 1

            for index, ts in enumerate(batch, 1):



                curr_samp = ts.copy()
                curr_samp['relation'] = ts["gold"]
                curr_samp['id_relation'] = rel
                if ts["gold"] == 'no_relationv':
                    curr_samp['relation'] = 'no_relation'
                    curr_samp['gold'] = 'no_relation'


                curr_samp['gold_relation'] = curr_samp['gold']
                del curr_samp['gold']
                del curr_samp['pred']

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104449" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104450" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104451" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104452" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104453" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "35-8b1962e0-ee8c-4906-a173-662c554ef87d_PERSON_ORGANIZATION_104454" and curr_samp["id_relation"] == "per:schools_attended":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "58-55a9f783-faec-4e7f-aecc-ff4ade83c234_PERSON_STATE_OR_PROVINCE_153878" and curr_samp["id_relation"] == "per:stateorprovinces_of_residence":
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "58-55a9f783-faec-4e7f-aecc-ff4ade83c234_PERSON_STATE_OR_PROVINCE_153879" and curr_samp["id_relation"] == "per:stateorprovinces_of_residence":
                    curr_samp['gold_relation'] = "per:stateorprovinces_of_residence"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "58-55a9f783-faec-4e7f-aecc-ff4ade83c234_PERSON_STATE_OR_PROVINCE_153880" and curr_samp["id_relation"] == "per:stateorprovinces_of_residence":
                    curr_samp['gold_relation'] = "no_relation"
                    curr_samp['id'] += "i"

                if curr_samp["id"] == "58-55a9f783-faec-4e7f-aecc-ff4ade83c234_PERSON_STATE_OR_PROVINCE_153881" and curr_samp["id_relation"] == "per:stateorprovinces_of_residence":
                    curr_samp['id'] += "i"










                split_by_ = curr_samp['id'].split("_")
                sentence_id = "_".join(split_by_[:-1])
                curr_samp["sentence_id"] = sentence_id
                count_sent_id.add(sentence_id)



                if count_b % 2 == 0:
                    TO_TRAIN.append(curr_samp)
                    count_train += 1

                else:
                    TO_TEST.append(curr_samp)
                    count_test +=1

                TO_ALL_CHALLENGE.append(curr_samp)

                edited_cpy_list.append(curr_samp)
                # print("---------------------------------------------------------------")
                if curr_samp["id"] == "58-55a9f783-faec-4e7f-aecc-ff4ade83c234_PERSON_STATE_OR_PROVINCE_153881":
                    print(curr_samp["token"][curr_samp["subj_start"]])
                    print(curr_samp["token"][curr_samp["obj_start"]])


                    for fff in curr_samp:
                        print(fff, ":  ",curr_samp[fff])
                    print("---------------------------------------------------------------")
                    print()
                    print()

                assert rel == curr_samp['id_relation']
                if curr_samp['gold_relation'] == 'no_relation':
                    count_no_relation += 1

            EDITED_NEW_gold_annotations_100_SENTS_TO_EACH_REL[rel][num].append(edited_cpy_list)




    print(rel, count_b)
    print("count_test: ", count_test)
    print("count_train: ", count_train)
    print("------------------")
    print()


print("len(TO_TRAIN)", len(TO_TRAIN))
print()
print("len(TO_TEST)", len(TO_TEST))
print()


count_test = 0
count_train = 0

NEW_TRAIN = tacred_real_samples_train + TO_TRAIN

NEW_TEST = tacred_real_samples_test + TO_TEST


positive_TO_TRAIN = sum([1 for samp in TO_TRAIN if samp["relation"] != 'no_relation'])
negative_TO_TRAIN = sum([1 for samp in TO_TRAIN if samp["relation"] == 'no_relation'])

positive_TO_TEST = sum([1 for samp in TO_TEST if samp["relation"] != 'no_relation'])
negative_TO_TEST = sum([1 for samp in TO_TEST if samp["relation"] == 'no_relation'])


print("len(NEW_TRAIN)", len(NEW_TRAIN), "positive:", positive_TO_TRAIN, "negative: ", negative_TO_TRAIN)
print()
print("len(NEW_TEST)", len(NEW_TEST), "positive:", positive_TO_TEST, "negative: ", negative_TO_TEST)
print()
print()
print("len(tacred_real_samples_train)", len(tacred_real_samples_train))
print("len(tacred_real_samples_test)", len(tacred_real_samples_test))


# with open('TACRED_and_50_per_rel_CHALLENGE_train.json', 'w') as outfile:
#     json.dump(NEW_TRAIN, outfile)
#
# with open('TACRED_and_50_per_rel_CHALLENGE_test.json', 'w') as outfile:
#     json.dump(NEW_TEST, outfile)
#
# with open('/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/data/TACRED_WITH_CHALLENGE_FIX/train.json', 'w') as outfile:
#     json.dump(NEW_TRAIN, outfile)
#
# with open('/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/data/TACRED_WITH_CHALLENGE_FIX/test.json', 'w') as outfile:
#     json.dump(NEW_TEST, outfile)
#
# with open('/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/data/TACRED_WITH_CHALLENGE_FIX/dev.json', 'w') as outfile:
#     json.dump(NEW_TEST, outfile)
#
# test_to_dic = {ttss['id'] : ttss for ttss in TO_TEST}
# with open('CHALLENGE_50_per_rel_test.json', 'w') as outfile:
#     json.dump(test_to_dic, outfile)

print(len(TO_ALL_CHALLENGE))



# with open('gold_annotations_100_SENTS_TO_EACH_REL.json', 'w') as outfile:
#     json.dump(NEW_gold_annotations_100_SENTS_TO_EACH_REL, outfile)
#
# with open('challeng_as_tacred_100_sents_per_rel.json', 'w') as outfile:
#     json.dump(TO_ALL_CHALLENGE, outfile)

# with open('/home/nlp/sharos/span_bert/SpanBERT/RoBERTa_baseline_TACRED/data/TACRED_WITH_CHALLENGE_FIX/test_only_challenge_part.json', 'w') as outfile:
#     json.dump(TO_TEST, outfile)

# with open('challeng_as_tacred_FIXED.json', 'w') as outfile:
#     json.dump(TO_ALL_CHALLENGE, outfile)

# with open('challeng_as_tacred_100_sents_per_rel_FINAL.json', 'w') as outfile:
#     json.dump(TO_ALL_CHALLENGE, outfile)
#
# with open('gold_annotations_100_SENTS_TO_EACH_REL_FINAL.json', 'w') as outfile:
#     json.dump(NEW_gold_annotations_100_SENTS_TO_EACH_REL, outfile)

print(count_no_relation)
print(len(count_sent_id))
print(cnt)