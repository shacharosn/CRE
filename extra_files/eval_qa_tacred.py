import json

import collections
import re
import string
from sklearn.metrics import classification_report
import  pickle
import numpy as np
# from qa_tacred import questions_dic

F1_THRESHOLD = 0.4


# RELS = 'per:age'
# RELS = 'org:founded_by'
# RELS = 'per:employee_of'
RELS = 'org:founded'
# RELS = 'per:date_of_birth'
# RELS = 'per:schools_attended'

REL_TO_WRITE = "_".join(RELS.split(':'))

REL_TO_WRITE += "_tacred"

q1_org_founded = lambda org,date: 'When was ' + org + ' founded?'
q2_org_founded = lambda org,date: 'What was founded on ' + date + '?'
q3_org_founded = lambda org,date: f'On what date was {org} founded?'

qg1_org_founded = lambda org,date: f'What organization was founded on some date ?'  #  TODO: ask yoav
qg4_org_founded = lambda org,date: f"What organization's founding date is mentioned ?"  #  TODO: ask yoav
qg2_org_founded = lambda org,date: 'On what date was an organization founded?'
qg3_org_founded = lambda org,date: 'When was any organization founded?'

q1_per_age = lambda per,age: "What is " + per + "'s age?"
q2_per_age = lambda per,age: "Whose age is "+ age + "?"

qg1_per_age = lambda per,age: f"Which number in the test is an age?"
qg2_per_age = lambda per,age: f"Whose age is mentioned in the text?" #GOOD

q1_per_date_of_birth = lambda per,date_of_birth: "What is " + per + "'s date of birth?"
q2_per_date_of_birth = lambda per,date_of_birth: "Who was born on " + date_of_birth + "?"

qg1_per_date_of_birth = lambda per,date_of_birth: f"Whose date of birth is mentioned?"
qg2_per_date_of_birth = lambda per,date_of_birth: f"When was anyone born?"

q1_org_founded_by = lambda org,per: "Who founded " + org + "?"
q2_org_founded_by = lambda org,per: "What did " + per + " found?"
# q2_org_founded_by = lambda org,per: "What was founded by " + per + "?"

qg1_org_founded_by = lambda org,date: 'Who founded an organization?'
qg2_org_founded_by = lambda org,date: f"What organization someone found?"
qg3_org_founded_by = lambda org,date: f"Which organization's founder is mentioned?"

q1_per_schools_attended = lambda per,org: "Which school did " + per + " attend?"
q2_per_schools_attended = lambda per,org: "Who attended " + org + "?"

qg1_per_schools_attended = lambda per,org: "Which school did someone attend?"
qg2_per_schools_attended = lambda per,org: "Who attended a school?"

q1_per_employee_of = lambda per,org: "Who employs " + per + "?"
q2_per_employee_of = lambda per,org: "Who is employee of " + org + "?"

qgg1_per_employee_of = lambda per,org: "Who employs someone?"
qgg2_per_employee_of = lambda per,org: "Who was employed by an organization?"

qg1_per_employee_of = lambda per,org: "Which organization's employee is mentioned?"
qg2_per_employee_of = lambda per,org: "Whose employing organization is mentioned?"

# q1_per_employee_of = lambda per,org: "What company does " + per + " work for?"
# q2_per_employee_of = lambda per,org: "Who works for " + org + "?"





questions_dic = {}

questions_dic['org:founded'] = [[q1_org_founded, 'subj'], [q2_org_founded, 'obj']]
questions_dic['per:age'] = [[q1_per_age, 'subj'], [q2_per_age, 'obj']]
questions_dic['per:date_of_birth'] = [[q1_per_date_of_birth, 'subj'], [q2_per_date_of_birth, 'obj']]
questions_dic['org:founded_by'] = [[q1_org_founded_by, 'subj'], [q2_org_founded_by, 'obj']]
questions_dic['per:schools_attended'] = [[q1_per_schools_attended, 'subj'], [q2_per_schools_attended, 'obj']]
questions_dic['per:employee_of'] = [[q1_per_employee_of, 'subj'], [q2_per_employee_of, 'obj']]






with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples_list = json.load(tacred_test_file)

tacred_real_samples = {samp['id']: samp for samp in tacred_real_samples_list}


with open("../span_bert/SpanBERT/SpanBERT/qa_rels/"+REL_TO_WRITE+".json") as json_file:
    gold_data = json.load(json_file)

with open("../span_bert/SpanBERT/SpanBERT/model_squad2/squad2/predictions_"+REL_TO_WRITE+".json") as json_file:
    preds_data = json.load(json_file)

# with open("../span_bert/SpanBERT/7squad_trans_new_load_model/transformers/qa_rels/"+REL_TO_WRITE+".json") as json_file:
#     gold_data = json.load(json_file)
#
# with open("../span_bert/SpanBERT/7squad_trans_new_load_model/transformers/wwm_cased_finetuned_squad/predictions_"+REL_TO_WRITE+".json") as json_file:
#     preds_data = json.load(json_file)

# /home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/qa_rels/org_founded.json

def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return subj_span, obj_span


def normalize_answer(s):
  """Lower text and remove punctuation, articles and extra whitespace."""
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

def get_tokens(s):
  if not s: return []
  return normalize_answer(s).split()

def compute_exact(a_gold, a_pred):
  return int(normalize_answer(a_gold) == normalize_answer(a_pred))

def compute_f1(a_gold, a_pred):
  gold_toks = get_tokens(a_gold)
  pred_toks = get_tokens(a_pred)
  # print(gold_toks, pred_toks)
  common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
  num_same = sum(common.values())
  if len(gold_toks) == 0 or len(pred_toks) == 0:
    # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
    return int(gold_toks == pred_toks)
  if num_same == 0:
    return 0
  precision = 1.0 * num_same / len(pred_toks)
  recall = 1.0 * num_same / len(gold_toks)
  f1 = (2 * precision * recall) / (precision + recall)
  # if f1 < 1.0:
  #     print(gold_toks, pred_toks)
  return f1



annotated_data = {}

for paragraph in gold_data['data'][0]['paragraphs']:
    context = paragraph['context']
    for qa in paragraph['qas']:

        new_qa = qa.copy()
        new_qa['context'] = context
        annotated_data[qa['id']] = new_qa


count_err = 0
count_all_err = 0

error_else = 0
error_recognize = 0

error_else_2 = 0
error_recognize_2 = 0

marged_preds = {}

marged_preds_in_ans = {}

for pred_id, pred in preds_data.items():
    # correct_answers = [ans['text'] for ans in annotated_data[pred_id]['answers']]
    # print(correct_answers, "  ---  ", pred)
    aaa = annotated_data[pred_id]
    gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
    if not gold_answers:
        # For unanswerable questions, only correct answer is empty string
        gold_answers = ['']

    if gold_answers != ['']:
        print()

    f1_score = max(compute_f1(a, pred) for a in gold_answers)
    if(len(gold_answers)) > 1:
        print("KKKK")
        print(gold_answers)

    slice_pred_id = pred_id.split('_')[0]

    if slice_pred_id not in marged_preds:
        marged_preds[slice_pred_id] = "no_relation"


    if slice_pred_id not in marged_preds_in_ans:
        marged_preds_in_ans[slice_pred_id] = "no_relation"


    if f1_score > F1_THRESHOLD:

        # marged_preds[slice_pred_id] = RELS
        if pred == '':
            marged_preds[slice_pred_id] = "no_relation"
        else:
            marged_preds[slice_pred_id] = tacred_real_samples[slice_pred_id]['relation']




    subj, obj = get_span_of_subj_obj(tacred_real_samples[slice_pred_id])

    for idxxx, (q, question_about) in enumerate(questions_dic[RELS]):

        curr_question = q(subj, obj)

        if annotated_data[pred_id]['question'] == curr_question and question_about == 'subj':
            if obj in pred or (pred != '' and pred in obj):
                marged_preds_in_ans[slice_pred_id] = RELS
                print("TTTTTTTT_22222_22222")
                print(curr_question)
                print(obj, "  --  ", pred)
                print("--------------------")
                if annotated_data[pred_id]['question'] != curr_question:
                    print(annotated_data[pred_id]['question'])
                    print(curr_question)
                    print("fsf"[324])


        elif annotated_data[pred_id]['question'] == curr_question and question_about == 'obj':
            if subj in pred or (pred != '' and pred in subj):
                marged_preds_in_ans[slice_pred_id] = RELS
                if annotated_data[pred_id]['question'] != curr_question:
                    print("fsf"[324])
                print("TTTTTTTT_11111_11111")
                print(curr_question)
                print(subj, "  --  ", pred)
                print(print("--------------------"))








    print(pred_id)
    print("aaaaa")
    print(annotated_data[pred_id]['context'])
    print()
    print(annotated_data[pred_id]['question'])
    print()
    print(gold_answers, "  ---  ", "'" + pred + "'")



    if marged_preds[slice_pred_id] != tacred_real_samples[slice_pred_id]['relation']:
            print(annotated_data[pred_id]['context'])
            print()
            print(annotated_data[pred_id]['question'])
            print()
            print(gold_answers, "  ---  ", "'" + pred + "'")
            print(f1_score)
            print()
            print(tacred_real_samples[slice_pred_id]['relation'])
            print(tacred_real_samples[slice_pred_id]['subj_type'],tacred_real_samples[slice_pred_id]['obj_type'])
            print(marged_preds[slice_pred_id], tacred_real_samples[slice_pred_id]['relation'])

            print("------------------------------------------------------------------------------------------------------------")


    if f1_score < 1.0: # 0.3:

        # if pred != "" and (gold_answers[0] in pred or pred in gold_answers[0]):
        #     # continue
        #     count_all_err += 1
        # if 0 < f1_score < 1:
            count_all_err += 1
            if not ((gold_answers[0] != "" and gold_answers[0] in pred) or (pred != "" and pred in gold_answers[0])):


                count_err += 1

                # print(annotated_data[pred_id]['context'])
                # print()
                # print(annotated_data[pred_id]['question'])
                # print()
                # print(gold_answers, "  ---  ","'"+pred+"'")
                # print(f1_score)
                # print()





                # if gold_answers == ['']:
                #     error_else += 1
                #     print("error_else")
                # # elif pred == '':
                # #     error_recognize += 1
                # else:
                #     error_recognize += 1
                #     print("error_recognize")


                if pred == '':
                    error_recognize_2 += 1

                else:
                    error_else_2 += 1





                print("-------------------------------------------------------------")






print("count_err: ",count_err)
print()
print(print("count_all_err: ",count_all_err))
print()
# print()
# print("error_else: ",error_else)
# print()
# print("error_recognize: ",error_recognize)
# print()
# assert count_err == error_else_2+error_recognize_2

print("error_else_2: ",error_else_2)
print()
print("error_recognize_2: ",error_recognize_2)


y_true = []
y_pred = []

for pred_id in marged_preds:

    if tacred_real_samples[pred_id]['relation'] != RELS:
        y_true.append('no_relation')
    else:
        y_true.append(tacred_real_samples[pred_id]['relation'])

    y_pred.append(marged_preds[pred_id])


print(classification_report(y_true, y_pred))
print()

print(len(preds_data))
print(len(marged_preds))


print("num of positive predictions:  ", sum([1 for y in y_pred if y == RELS]))


z1 = {"shachar", "noy", "or"}
z2 = {"shachar", "noy"}
z3 = {"shachar", "noy", "barak"}
z4 = set()


y_true_in_ans = []
y_pred_in_ans = []

for pred_id in marged_preds_in_ans:

    if tacred_real_samples[pred_id]['relation'] != RELS:
        y_true_in_ans.append('no_relation')
    else:
        y_true_in_ans.append(tacred_real_samples[pred_id]['relation'])

    y_pred_in_ans.append(marged_preds_in_ans[pred_id])


print(classification_report(y_true_in_ans, y_pred_in_ans))
print()

print("num of positive predictions:  ", sum([1 for y in y_pred_in_ans if y == RELS]))

print()

print("num of negative predictions:  ", sum([1 for y in y_true_in_ans if y != RELS]))

print()

print(RELS)


#                   DEBUG !!!!

# for pred_id, pred in preds_data.items():
#     slice_pred_id = pred_id.split('_')[0]
#     gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
#
#     if marged_preds_in_ans[slice_pred_id] == RELS and tacred_real_samples[slice_pred_id]['relation'] != RELS:
#
#         print("dadasgd")
#         print(slice_pred_id)
#         print(annotated_data[pred_id]['context'])
#         print()
#         print(annotated_data[pred_id]['question'])
#         print()
#         print(gold_answers, "  ---  ", "'" + pred + "'")







