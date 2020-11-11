import json
import re
import string
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

# from The_Questions import questions_dic
from The_Questions import rel_qs


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




# RELS = 'per:age'
# RELS = 'org:founded_by'
# RELS = 'per:employee_of'
# RELS = 'org:founded'
# RELS = 'per:date_of_birth'
# RELS = 'per:schools_attended'

# ALL_RELS = ['per:age', 'org:founded_by', 'per:employee_of', 'org:founded', 'per:date_of_birth', 'per:schools_attended']

aaa = ['org:top_members/employees', 'per:parents', 'org:parents', 'org:subsidiaries', 'per:children']

# ALL_RELS = rel_qs

# ALL_RELS = aaa




with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples_list = json.load(tacred_test_file)


with open('gold_annotations.json') as json_file:
    challenge_samples = json.load(json_file)


with open('tacred_results.json') as json_file:
    tacred_results = json.load(json_file)



with open('qa_tacred_results.json') as json_file:
    qa_tacred_results = json.load(json_file)


tacred_real_samples = {samp['id']: samp for samp in tacred_real_samples_list}


micro_avg_f1 = []
total_weight = 0


IS_CHALLENGE_SET = False # False # True



# qa_tacred_results = {}

ALL_RELS = challenge_samples
# ALL_RELS = rel_qs

# ALL_RELS = ["org:number_of_employees/members"]
# ALL_RELS = ['org:alternate_names']

# ALL_RELS = ["per:countries_of_residence"]

total_positive_examples = 0
total_negative_examples = 0

total_all_rel_y_true = []
total_all_rel_y_pred = []


things_to_plot = {}





# for RELS in ALL_RELS:




FILE_TO_WRITE = "ALL_RELS_QA_4"




with open("../span_bert/SpanBERT/SpanBERT/qa_rels/"+FILE_TO_WRITE+".json") as json_file:
    gold_data = json.load(json_file)


# with open("../span_bert/SpanBERT/SpanBERT/model_squad2/squad2/predictions_"+FILE_TO_WRITE+".json") as json_file:
#     preds_data = json.load(json_file)

with open("/home/nlp/sharos/span_bert/SpanBERT/7squad_trans_new_load_model/transformers/out_bert/predictions_"+FILE_TO_WRITE+".json") as json_file:
        preds_data = json.load(json_file)

# with open("../span_bert/SpanBERT/SpanBERT/model_squad2/squad2_tac/predictions_"+REL_TO_WRITE+".json") as json_file:
#     preds_data = json.load(json_file)




iiiddd = set()

annotated_data = {}

for paragraph in gold_data['data'][0]['paragraphs']:
    context = paragraph['context']
    for qa in paragraph['qas']:

        new_qa = qa.copy()
        new_qa['context'] = context
        annotated_data[qa['id']] = new_qa

        iiiddd.add(qa['original_id'])
        # if "098f665fb9d13cf39372" in qa['original_id']:
        #     print(qa['original_id'])
        #     print("fds"[4323])




marged_preds_in_ans = {}


for pred_id, pred in preds_data.items():

    real_samples = tacred_real_samples

    gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
    if not gold_answers:
        # For unanswerable questions, only correct answer is empty string
        gold_answers = ['']



    split_pred_id = pred_id.split("_")


    slice_pred_id = split_pred_id[0]
    rel_q = annotated_data[pred_id]['q_rel']
    q_num = split_pred_id[-1]
    gold_rel = annotated_data[pred_id]['gold_rel']


    if slice_pred_id not in marged_preds_in_ans:
        marged_preds_in_ans[slice_pred_id] = []   # "no_relation"


    subj, obj = get_span_of_subj_obj(real_samples[slice_pred_id])

    if int(q_num) == 0:
        if obj in pred or (pred != '' and pred in obj):
            marged_preds_in_ans[slice_pred_id].append(rel_q)

    if int(q_num) == 1:
        if subj in pred or (pred != '' and pred in subj):
            marged_preds_in_ans[slice_pred_id].append(rel_q)



count_more_than_one_pred = 0

y_true = []
y_pred = []

no_rel = 0

for samp_id in marged_preds_in_ans:
    set_of_preds = set(marged_preds_in_ans[samp_id])

    y_true.append(tacred_real_samples[samp_id]['relation'])

    if len(marged_preds_in_ans[samp_id]) == 0:
        y_pred.append('no_relation')

    else:
        y_pred.append(marged_preds_in_ans[samp_id][0])


    # else:
    #     if tacred_real_samples[samp_id]['relation'] in marged_preds_in_ans[samp_id]:
    #         y_pred.append(tacred_real_samples[samp_id]['relation'])
    #
    #     else:
    #
    #         y_pred.append(marged_preds_in_ans[samp_id][0])

    if y_true[-1] != 'no_relation' and y_pred[-1] == 'no_relation':
        y_tt = y_true[-1]
        y_pp = marged_preds_in_ans[samp_id]
        y_pppp = y_pred[-1]
        print("gfgdg")

    if len(marged_preds_in_ans[samp_id]):
        no_rel += 1

    if len(set_of_preds) > 1:
        count_more_than_one_pred += 1
        print(set_of_preds)
        print(samp_id)
        print()

print("count_more_than_one_pred: ", count_more_than_one_pred)
print(no_rel)

print(len(marged_preds_in_ans))




total_true_positive = sum([1 for y_p, y_t in zip(y_pred, y_true) if y_p == y_t and y_t != 'no_relation' ])
total_false_positive = sum([1 for y_p, y_t in zip(y_pred, y_true) if y_p != 'no_relation' and y_t != y_p])
total_true_negative = sum([1 for y_p, y_t in zip(y_pred, y_true) if y_p == y_t and y_t == 'no_relation' ])
total_false_negative = sum([1 for y_p, y_t in zip(y_pred, y_true) if y_p == 'no_relation' and y_t != y_p])




print("TOTAL TRUE POSITIVE:  ",round(total_true_positive / len(y_true), 4), "\t\tNUMBER: ", total_true_positive)
print()
print("TOTAL FALSE POSITIVE:  ",round(total_false_positive / len(y_true),4), "\t\tNUMBER: ", total_false_positive)
print()
print("TOTAL TRUE NEGATIVE:  ", round(total_true_negative / len(y_true), 4), "\t\tNUMBER: ", total_true_negative)
print()
print("TOTAL FALSE NEGATIVE:  ", round(total_false_negative / len(y_true), 4), "\t\tNUMBER: ", total_false_negative)




pos = sum([1 for y_t in y_true if y_t != 'no_relation'])
neg = sum([1 for y_t in y_true if y_t == 'no_relation'])
print()
print("pos: ", pos, pos / len(y_true))
print("neg: ", neg, neg / len(y_true))

print()
print(sum([1 for y_p in y_pred if y_p != 'no_relation']))
print()

print(compute_f1(y_pred, y_true))
