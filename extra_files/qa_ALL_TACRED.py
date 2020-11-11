import json
from collections import Counter
from collections import defaultdict
# from IPython.display import display, Markdown
from tabulate import tabulate
from termcolor import colored
import csv
import pickle
import cloudpickle
from termcolor import colored, cprint
import spacy
from benepar.spacy_plugin import BeneparComponent
import base64
import numpy as np
import dill
from The_Questions import rel_qs
# FINDED_SPAN = False
# ALL_NP = []
# nlp = spacy.load('en')
# nlp.add_pipe(BeneparComponent('benepar_en'))

ALL_RELATIONS_TYPES = {'per:title': ['PERSON', 'TITLE'], 'org:top_members/employees': ['ORGANIZATION', 'PERSON'],
                       'org:country_of_headquarters': ['ORGANIZATION', 'COUNTRY'], 'per:parents': ['PERSON', 'PERSON'],
                       'per:age': ['PERSON', 'DURATION'], 'per:countries_of_residence': ['PERSON', 'COUNTRY'],
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

def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return [subj_span, obj_span]









with open("../span_bert/SpanBERT/2squad/dev-v2.0.json") as json_file:
    squad_dev = json.load(json_file)







with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples = json.load(tacred_test_file)


with open('gold_annotations.json') as json_file:
    challenge_samples = json.load(json_file)


# ALL_RELS = challenge_samples

ALL_RELS = rel_qs

# ALL_RELS = ['org:alternate_names']

# ALL_RELS = ["per:countries_of_residence"]



IS_CHALLENGE_SET = False # False True



cccc = 0



count_with_rels = 0
count_total_qas = 0







newDict = squad_dev.copy()
newDict['data'] = squad_dev['data'][0:1]
newDict['data'][0]['paragraphs'] = squad_dev['data'][0]['paragraphs'][0:2]

newDict['data'][0]['paragraphs'][0]['qas'] = squad_dev['data'][0]['paragraphs'][0]['qas'][0:2]
newDict['data'][0]['paragraphs'][1]['qas'] = squad_dev['data'][0]['paragraphs'][1]['qas'][0:2]

newDict['data'][0]['paragraphs'] = []



FILE_TO_WRITE = "ALL_RELS_QA_5"

iiiddd = set()
size_of_iiiddd = 0

for samp in tacred_real_samples:

    if samp['id'] == "098f665fb9b0249c0bfb":
        print()


    for rel in ALL_RELATIONS_TYPES:

        #      MUST be the same ner type !!!!!!!

        if (samp['subj_type'] != ALL_RELATIONS_TYPES[rel][0] or samp['obj_type'] != ALL_RELATIONS_TYPES[rel][1]):
            continue

        gold_relation = samp['relation']


        curr_context = ' '.join(samp['token'])
        curr_paragraph = {'context': curr_context, 'qas': []}

        subj, obj = get_span_of_subj_obj(samp)


        for idx, q  in enumerate(rel_qs[rel]):
            # curr_question = q(subj, obj)
            if idx == 0:
                question_about = 'subj'
                curr_question = q.format(subj)

            elif idx == 1:
                question_about = 'obj'
                curr_question = q.format(obj)


            if question_about == 'subj':
                if gold_relation == rel:
                    answers = [{'answer_start': curr_context.find(obj), 'text': obj}]

                elif gold_relation != rel:
                    answers = []
                    count_with_rels += 1


            elif question_about == 'obj':
                if gold_relation == rel:
                    answers = [{'answer_start': curr_context.find(subj), 'text': subj}]

                elif gold_relation != rel:
                    answers = []
                    count_with_rels += 1


            is_impossible = True if len(answers) == 0 else False

            curr_qa = {'id': samp['id'] + '_' + rel + '_' + str(idx), 'is_impossible': is_impossible, 'question': curr_question,
                       'answers': answers, 'gold_rel': gold_relation, 'q_rel': rel, 'original_id': samp['id']}
            curr_paragraph['qas'].append(curr_qa)

            count_total_qas += 1

            iiiddd.add(samp['id'] )

        # if curr_paragraph['qas'] == []:
        #     print(curr_paragraph['qas'][32143242])
        if curr_paragraph['qas'] != []:
            newDict['data'][0]['paragraphs'].append(curr_paragraph)

    # print(json.dumps(newDict, indent=4, sort_keys=True))

    print(len(newDict['data'][0]['paragraphs']), len(newDict['data'][0]['paragraphs'])*2)

    if len(iiiddd) == size_of_iiiddd:
        print("ssssss")
        print(samp['subj_type'], samp['obj_type'])

    size_of_iiiddd += 1





with open('../span_bert/SpanBERT/SpanBERT/qa_rels/'+FILE_TO_WRITE+'.json', 'w') as outfile:
    json.dump(newDict, outfile)




print("count_with_rels", count_with_rels)

print()
print(cccc)
print(count_total_qas)
print()
print("len(iiiddd)", len(iiiddd))
print()
print("len(tacred_real_samples): ", len(tacred_real_samples))