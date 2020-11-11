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

for RELS in ALL_RELS:

    print(RELS)
    things_to_plot[RELS] = {}


    REL_TO_WRITE = "_".join(RELS.split(':'))


    if IS_CHALLENGE_SET:
        real_samples = {ts['id']:ts for num in challenge_samples[RELS] for batch in challenge_samples[RELS][num] for ts in batch}
        REL_TO_WRITE = REL_TO_WRITE.replace('/', '_')
        # REL_TO_WRITE += "_CHALLENGE"
        REL_TO_WRITE += "_CHALLENGE_2"
        # REL_TO_WRITE += "_CHALLENGE_best_threshold"
        # REL_TO_WRITE += "_CHALLENGE_best_threshold_2"



    else:
        real_samples = tacred_real_samples
        REL_TO_WRITE = REL_TO_WRITE.replace('/', '_')
        # REL_TO_WRITE += "_tacred_REAL"
        # REL_TO_WRITE += "_tacred_Amir_2"
        REL_TO_WRITE += "_tacred_REAL_2"


    with open("../span_bert/SpanBERT/SpanBERT/qa_rels/"+REL_TO_WRITE+".json") as json_file:
        gold_data = json.load(json_file)


    with open("../span_bert/SpanBERT/SpanBERT/model_squad2/squad2/predictions_"+REL_TO_WRITE+".json") as json_file:
        preds_data = json.load(json_file)

    # with open("../span_bert/SpanBERT/SpanBERT/model_squad2/squad2_tac/predictions_"+REL_TO_WRITE+".json") as json_file:
    #     preds_data = json.load(json_file)






    annotated_data = {}

    for paragraph in gold_data['data'][0]['paragraphs']:
        context = paragraph['context']
        for qa in paragraph['qas']:

            new_qa = qa.copy()
            new_qa['context'] = context
            annotated_data[qa['id']] = new_qa




    marged_preds_in_ans = {}


    for pred_id, pred in preds_data.items():


        gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
        if not gold_answers:
            # For unanswerable questions, only correct answer is empty string
            gold_answers = ['']


        # slice_pred_id = pred_id.split('_')[0]

        k = pred_id.rfind("_")
        slice_pred_id = pred_id[:k]


        if slice_pred_id not in marged_preds_in_ans:
            marged_preds_in_ans[slice_pred_id] = "no_relation"


        subj, obj = get_span_of_subj_obj(real_samples[slice_pred_id])

        # for idxxx, (q, question_about) in enumerate(questions_dic[RELS]):
        for idx, q in enumerate(rel_qs[RELS]):
            # curr_question = q(subj, obj)
            if idx == 0:
                question_about = 'subj'
                curr_question = q.format(subj)

            elif idx == 1:
                question_about = 'obj'
                curr_question = q.format(obj)

            # curr_question = q(subj, obj)

            if annotated_data[pred_id]['question'] == curr_question and question_about == 'subj':
                if obj in pred or (pred != '' and pred in obj):
                    marged_preds_in_ans[slice_pred_id] = RELS
                    # print("TTTTTTTT_22222_22222")
                    # print(curr_question)
                    # print(obj, "  --  ", pred)
                    # print("--------------------")



            elif annotated_data[pred_id]['question'] == curr_question and question_about == 'obj':
                if subj in pred or (pred != '' and pred in subj):
                    marged_preds_in_ans[slice_pred_id] = RELS
                    # print("TTTTTTTT_11111_11111")
                    # print(curr_question)
                    # print(subj, "  --  ", pred)
                    # print(print("--------------------"))



    y_true_in_ans = []
    y_pred_in_ans = []

    for pred_id in marged_preds_in_ans:

        if IS_CHALLENGE_SET:
            gold_relation = real_samples[pred_id]['gold']

        else:
            gold_relation = real_samples[pred_id]['relation']



        if gold_relation != RELS:
            y_true_in_ans.append('no_relation')
        else:
            y_true_in_ans.append(gold_relation)

        y_pred_in_ans.append(marged_preds_in_ans[pred_id])

    print(RELS)

    print()

    print("Tacred results:  ", tacred_results[RELS])

    print()

    print("QA Tacred results:  ", qa_tacred_results[RELS])

    print()

    print(classification_report(y_true_in_ans, y_pred_in_ans))

    dic_classification_report = classification_report(y_true_in_ans, y_pred_in_ans, output_dict=True)
    micro_avg_f1.append(dic_classification_report[RELS]['f1-score'] * dic_classification_report[RELS]['support'])
    total_weight += dic_classification_report[RELS]['support']


    true_positive = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_p == RELS and y_t == RELS])
    false_positive = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_p == RELS and y_t != RELS])
    true_negative = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_p != RELS and y_t != RELS])
    false_negative = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_p != RELS and y_t == RELS])

    print("TRUE POSITIVE:  ", round(true_positive / len(y_true_in_ans), 4), "\t\tNUMBER: ", true_positive)
    print()
    print("FALSE POSITIVE:  ", round(false_positive / len(y_true_in_ans), 4), "\t\tNUMBER: ", false_positive)
    print()
    print("TRUE NEGATIVE:  ", round(true_negative / len(y_true_in_ans), 4), "\t\tNUMBER: ", true_negative)
    print()
    print("FALSE NEGATIVE:  ", round(false_negative / len(y_true_in_ans), 4), "\t\tNUMBER: ", false_negative)

    things_to_plot[RELS]["true_positive"] = round(true_positive / len(y_true_in_ans), 4)
    things_to_plot[RELS]["false_positive"] = round(false_positive / len(y_true_in_ans), 4)

    # qa_tacred_results[RELS] = dic_classification_report[RELS]
    # qa_tacred_results[RELS]["true_positive"] = round(true_positive / len(y_true_in_ans), 4)
    # qa_tacred_results[RELS]["false_positive"] = round(false_positive / len(y_true_in_ans), 4)
    # qa_tacred_results[RELS]["true_negative"] = round(true_negative / len(y_true_in_ans), 4)
    # qa_tacred_results[RELS]["false_negative"] = round(false_negative / len(y_true_in_ans), 4)


    print()

    print("num of TRUE POSITIVE:  ", sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_p == RELS and y_t == RELS]))

    print()

    print("num of SYSTEM POSITIVE:  ", sum([1 for y in y_pred_in_ans if y == RELS]))

    print()

    print("num of REAL POSITIVE:  ", sum([1 for y in y_true_in_ans if y == RELS]))

    print()

    assert len(y_true_in_ans) == len(y_pred_in_ans)

    num_of_positive_examples = sum([1 for y_t in y_true_in_ans if y_t == RELS])
    num_of_negative_examples = sum([1 for y_t in y_true_in_ans if y_t != RELS])

    total_positive_examples += num_of_positive_examples
    total_negative_examples += num_of_negative_examples

    print("number of POSITIVE examples:", num_of_positive_examples, "({})".format(round(num_of_positive_examples / (num_of_positive_examples + num_of_negative_examples), 2)))
    print("number of NEGATIVE examples:", num_of_negative_examples, "({})".format(round(num_of_negative_examples / (num_of_positive_examples + num_of_negative_examples), 2)))

    print()

    accuracy_score_positive = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_t != 'no_relation' and y_p == y_t]) / num_of_positive_examples
    accuracy_score_negative = sum([1 for y_p, y_t in zip(y_pred_in_ans, y_true_in_ans) if y_t == 'no_relation' and y_p == y_t]) / num_of_negative_examples


    print("accuracy score positive: ", accuracy_score_positive)
    print()
    print("accuracy negative score: ", accuracy_score_negative)


    things_to_plot[RELS]["accuracy_score_positive"] = accuracy_score_positive
    things_to_plot[RELS]["accuracy_score_negative"] = accuracy_score_negative

    total_all_rel_y_true += y_true_in_ans
    total_all_rel_y_pred += y_pred_in_ans

    print("-----------------------------------------------------------")




    #                   #DEBUG !!!!
    #
    # for pred_id, pred in preds_data.items():
    #
    #     k = pred_id.rfind("_")
    #     slice_pred_id = pred_id[:k]
    #
    #     gold_answers = [a['text'] for a in annotated_data[pred_id]['answers'] if normalize_answer(a['text'])]
    #
    #     if marged_preds_in_ans[slice_pred_id] != RELS and len(gold_answers) > 0:# and gold_relation == RELS:
    #         print("-------------------")
    #         print(len(gold_answers))
    #         print("dadasgd")
    #         print(slice_pred_id)
    #         print(annotated_data[pred_id]['context'])
    #         print()
    #         print(annotated_data[pred_id]['question'])
    #         print()
    #         print(gold_answers, "  ---  ", "'" + pred + "'")






print("total_positive_examples:", total_positive_examples, "({})".format(round(total_positive_examples / (total_positive_examples + total_negative_examples),2)))
print("total_negative_examples:", total_negative_examples, "({})".format(round(total_negative_examples / (total_positive_examples + total_negative_examples),2)))

print()


print("total_positive_examples:", total_positive_examples)
print("total_negative_examples:", total_negative_examples)

print()
print()

total_accuracy_score_positive = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_t != 'no_relation' and y_p == y_t]) / total_positive_examples
total_accuracy_score_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_t == 'no_relation' and y_p == y_t]) / total_negative_examples

print()
print()

print("total accuracy_score: ", accuracy_score(total_all_rel_y_true, total_all_rel_y_pred))

print()
print("total accuracy score positive: ", total_accuracy_score_positive)
print()
print("total accuracy negative score: ", total_accuracy_score_negative)

print()
print()

print("f1 (accuracy) without 'no_relation':  ", sum([f1 for f1 in micro_avg_f1])/total_weight)
print()
print("f1 (accuracy) QA Tacred results without 'no_relation':  ", 0.5863011442419781)

print()





total_true_positive = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p != 'no_relation' and y_t != 'no_relation'])
total_false_positive = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p != 'no_relation' and y_t == 'no_relation'])
total_true_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p == 'no_relation' and y_t == 'no_relation'])
total_false_negative = sum([1 for y_p, y_t in zip(total_all_rel_y_pred, total_all_rel_y_true) if y_p == 'no_relation' and y_t != 'no_relation'])

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


print(classification_report(total_all_rel_y_true, total_all_rel_y_pred))


name_of_file_things_to_plot = 'things_to_plot_QA'

if IS_CHALLENGE_SET:
    name_of_file_things_to_plot += "_CHALLENGE.json"
else:
    name_of_file_things_to_plot += "_TACRED.json"


with open(name_of_file_things_to_plot, 'w') as outfile:
    json.dump(things_to_plot, outfile)


# if not IS_CHALLENGE_SET:
#     with open('qa_tacred_results.json', 'w') as outfile:
#         json.dump(qa_tacred_results, outfile)

print("pred true (there is a relation) : " , sum([1 for y_p in total_all_rel_y_pred if y_p != 'no_relation']), sum([1 for y_p in total_all_rel_y_pred if y_p != 'no_relation'])/len(total_all_rel_y_pred))


print()
print(compute_f1(total_all_rel_y_pred, total_all_rel_y_true))
print()
print(len(total_all_rel_y_pred))