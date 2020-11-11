import json

import collections
import re
import string


# RELS = 'org:founded_by'
RELS = 'per:employee_of'


REL_TO_WRITE = "_".join(RELS.split(':'))

REL_TO_WRITE += "_tacred"


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


for pred_id, pred in preds_data.items():
    # correct_answers = [ans['text'] for ans in annotated_data[pred_id]['answers']]
    # print(correct_answers, "  ---  ", pred)
    gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
    if not gold_answers:
        # For unanswerable questions, only correct answer is empty string
        gold_answers = ['']
    f1_score = max(compute_f1(a, pred) for a in gold_answers)


    if f1_score < 1.0: # 0.3:

        # if pred != "" and (gold_answers[0] in pred or pred in gold_answers[0]):
        #     # continue
        #     count_all_err += 1
        # if 0 < f1_score < 1:
            count_all_err += 1
            if not ((gold_answers[0] != "" and gold_answers[0] in pred) or (pred != "" and pred in gold_answers[0])):


                count_err += 1

                print(annotated_data[pred_id]['context'])
                print()
                print(annotated_data[pred_id]['question'])
                print()
                print(gold_answers, "  ---  ","'"+pred+"'")
                print(f1_score)
                print()
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

