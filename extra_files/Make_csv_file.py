import json
from collections import Counter
from collections import defaultdict
# from IPython.display import display, Markdown
from tabulate import tabulate
from termcolor import colored
import csv
import pickle
from termcolor import colored, cprint
import spacy
import xlwt
from xlwt import Workbook

NUMBER_OF_EXAMPLES_PER_LINE = [1,2,3,4,5]
NUM_OF_COLUMNS = 7

a = "34-11e728d6-5743-4bad-9bd3-f64d8d9fd24c_PERSON_NUMBER_1662965"
print("_".join(a.split("_")[:-1]))

RELS_TO_ANNOTATE = 'per:age'

q1_per_age = lambda per,age: "Is " + per + "'s age " + age + "?"

questions_dic = {}

questions_dic['per:age'] = q1_per_age

with open('wiki_13_34_35_not_fixed.pkl', 'rb') as f:
    dic_to_annotate = pickle.load(f)

with open("ANNOTATED_age_3.txt", 'r') as f:
    marge_annotated_age_3 = f.readlines()


def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<span style="color:  #0000ff; ">' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</span>'

    s[samp['obj_start']] = '<span style="color: #FF0000; ">' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</span>'

    s_detokenize = " ".join(s)

    # print(s_detokenize)
    # print()
    # print(" ".join(s[samp['subj_start']:samp['subj_end']+1]))
    # print(" ".join(s[samp['obj_start']:samp['obj_end']+1]))
    # print("---------------")
    # print()

    return dict(id=samp['id'], pred=samp['pred'], token=s_detokenize,
                mark_subj=" ".join(s[samp['subj_start']:samp['subj_end'] + 1]),
                mark_obj=" ".join(s[samp['obj_start']:samp['obj_end'] + 1]))

annotated_data = {}
for l in marge_annotated_age_3:
    line_split = l.split()
    if line_split[1] != 'invalid':
        annotated_data[line_split[0]] = 'no_relation' if line_split[1]=='NA' else line_split[1]


wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

for example_num in NUMBER_OF_EXAMPLES_PER_LINE:
    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 0, 'ID_'+str(example_num))
    # sheet1.write(0, 1, 'SENTENCE_ID')
    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 1, 'SENTENCE_'+str(example_num))

    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 2, 'SUBJ_' + str(example_num))
    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 3, 'OBJ_' + str(example_num))

    sheet1.write(0, (example_num - 1) * NUM_OF_COLUMNS + 4, 'QUESTION_' + str(example_num))

    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 5, 'IS_RELATION_'+str(example_num))
    sheet1.write(0, (example_num-1) * NUM_OF_COLUMNS + 6, 'GOLD_ANSWER_'+str(example_num))

col = 0
row = 1
curr_num_of_examples_in_line = 0
nnn = 0

for rel in dic_to_annotate:
    if rel not in RELS_TO_ANNOTATE:
        continue
    for num in dic_to_annotate[rel]:
        for idx_sents, batch in enumerate(dic_to_annotate[rel][num]):
            if batch[0]['id'] not in annotated_data:
                continue

            for ts in batch:
                nnn += 1

                readable_sampl = make_readable_sampl(ts)

                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 0, ts['id'])
                # sheet1.write(row, 1, "_".join(ts['id'].split("_")[:-1]))
                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 1, readable_sampl['token'])

                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 2, readable_sampl['mark_subj'])
                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 3, readable_sampl['mark_obj'])

                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 4, questions_dic[rel](readable_sampl['mark_subj'], readable_sampl['mark_obj']))

                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 5, rel)
                curr_gold_answer = 'NA'
                if ts['id'] in annotated_data:
                    curr_gold_answer = True if annotated_data[ts['id']] == rel else False

                sheet1.write(row, curr_num_of_examples_in_line * NUM_OF_COLUMNS + 6, curr_gold_answer)

                curr_num_of_examples_in_line += 1

                if curr_num_of_examples_in_line == len(NUMBER_OF_EXAMPLES_PER_LINE):
                    curr_num_of_examples_in_line = 0
                    row += 1



                print(ts['id'])
                print("_".join(ts['id'].split("_")[:-1]))
                print(make_readable_sampl(ts)['token'])
                print(rel)
                if ts['id'] in annotated_data:
                    print(annotated_data[ts['id']])
                else:
                    print("NNNNNNNNNNNNNAAAAAAAAAAAAA")

                if ts['id'] in annotated_data:
                    print(annotated_data[ts['id']])


                print()
            print("-----------------------------------------")






wb.save('age_example.xls')
print(row)
print("ddddddd")
print(nnn)