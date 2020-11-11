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

def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return [subj_span, obj_span]


def get_indx_and_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end']+1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end']+1])
    return [(subj_span, sample['subj_start'], sample['subj_end']), (obj_span, sample['obj_start'], sample['obj_end'])]



def find_span(ent_aggregate, tokens):
    # print("AAAA")
    # print(ent_aggregate)
    start_index = min([start for span, start, end in ent_aggregate])
    end_index = max([end for span, start, end in ent_aggregate])
    return " ".join(tokens[start_index:end_index+1])


def traverse(sent, ):

    global FINDED_SPAN
    global ALL_NP

    for child in sent._.children:

        str_child = str(child).rstrip(',')
        str_child = str_child.rstrip('.')
        str_child = str_child.rstrip(' ')
        if child._.labels == ('NP',):
            ALL_NP.append(str_child)
        # if str_child == span and child._.labels == ('NP',):
        #     FINDED_SPAN = True
        #     return

        traverse(child)


def is_np(span, doc_sent):
    global FINDED_SPAN
    FINDED_SPAN = False

    for sentt in list(doc_sent.sents):
        traverse(sentt)

    return FINDED_SPAN


def get_smallest_span(doc_sent, ents):
    global ALL_NP

    for sentt in list(doc_sent.sents):
        traverse(sentt)

    ans = ""
    for span in ALL_NP:
        if all([e in span for e in ents]):
            if ans == "" or len(span) < len(ans):
                ans = span

    return ans



with open("../span_bert/SpanBERT/2squad/dev-v2.0.json") as json_file:
    squad_dev = json.load(json_file)

# newDict = squad_dev.copy()
# newDict['data'] = squad_dev['data'][0:1]
# newDict['data'][0]['paragraphs'] = squad_dev['data'][0]['paragraphs'][0:2]
#
# newDict['data'][0]['paragraphs'][0]['qas'] = squad_dev['data'][0]['paragraphs'][0]['qas'][0:2]
# newDict['data'][0]['paragraphs'][1]['qas'] = squad_dev['data'][0]['paragraphs'][1]['qas'][0:2]
#
#
# newDict['data'][0]['paragraphs'] = []

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






# batch = [{'id': '63c2f42e-028e-4fcb-9746-fb27f1a07a21_ORGANIZATION_DATE_1497721', 'docid': 2, 'token': ['In', '1982', ',', 'AB', 'Etiproducts', 'Oy', 'was', 'established', 'by', 'Finnish', 'mining', 'multimetal', 'Outokumpu', 'group', 'and', 'Etibank', '.'], 'relation': 'no_relation', 'subj_start': 3, 'subj_end': 5, 'obj_start': 1, 'obj_end': 1, 'stanford_ner': ['O', 'DATE', 'O', 'ORGANIZATION', 'ORGANIZATION', 'ORGANIZATION', 'O', 'O', 'O', 'MISC', 'O', 'O', 'ORGANIZATION', 'O', 'O', 'ORGANIZATION', 'O'], 'subj_type': 'ORGANIZATION', 'obj_type': 'DATE', 'pred': 'org:founded'}, {'id': '63c2f42e-028e-4fcb-9746-fb27f1a07a21_ORGANIZATION_DATE_1497722', 'docid': 2, 'token': ['In', '1982', ',', 'AB', 'Etiproducts', 'Oy', 'was', 'established', 'by', 'Finnish', 'mining', 'multimetal', 'Outokumpu', 'group', 'and', 'Etibank', '.'], 'relation': 'no_relation', 'subj_start': 12, 'subj_end': 12, 'obj_start': 1, 'obj_end': 1, 'stanford_ner': ['O', 'DATE', 'O', 'ORGANIZATION', 'ORGANIZATION', 'ORGANIZATION', 'O', 'O', 'O', 'MISC', 'O', 'O', 'ORGANIZATION', 'O', 'O', 'ORGANIZATION', 'O'], 'subj_type': 'ORGANIZATION', 'obj_type': 'DATE', 'pred': 'org:founded'}, {'id': '63c2f42e-028e-4fcb-9746-fb27f1a07a21_ORGANIZATION_DATE_1497723', 'docid': 2, 'token': ['In', '1982', ',', 'AB', 'Etiproducts', 'Oy', 'was', 'established', 'by', 'Finnish', 'mining', 'multimetal', 'Outokumpu', 'group', 'and', 'Etibank', '.'], 'relation': 'no_relation', 'subj_start': 15, 'subj_end': 15, 'obj_start': 1, 'obj_end': 1, 'stanford_ner': ['O', 'DATE', 'O', 'ORGANIZATION', 'ORGANIZATION', 'ORGANIZATION', 'O', 'O', 'O', 'MISC', 'O', 'O', 'ORGANIZATION', 'O', 'O', 'ORGANIZATION', 'O'], 'subj_type': 'ORGANIZATION', 'obj_type': 'DATE', 'pred': 'org:founded'}]
# RELS_TO_ANNOTATE = ['per:age']
# RELS_TO_ANNOTATE = ['org:founded']
# RELS_TO_ANNOTATE = ['per:date_of_birth']
# RELS_TO_ANNOTATE = ['org:founded_by']
# RELS_TO_ANNOTATE = ['per:schools_attended']
# RELS_TO_ANNOTATE = ['per:employee_of']

# RELS_TO_ANNOTATE = ['org:founded_by','per:age','per:date_of_birth','org:founded_by','per:schools_attended','per:employee_of']


# RELS = 'per:age'
# RELS = 'org:founded_by'
# RELS = 'per:employee_of'
# RELS = 'org:founded'
# RELS = 'per:date_of_birth'
# RELS = 'per:schools_attended'

# ALL_RELS = ['per:age', 'org:founded_by', 'per:employee_of', 'org:founded', 'per:date_of_birth', 'per:schools_attended']

# ALL_RELS = rel_qs


# with open('wiki_13_34_35_not_fixed.pkl', 'rb') as f:
#     dic_to_annotate = pickle.load(f)
#
# with open("ANNOTATED_org_alternate_names_SAME_ENT.txt", 'r') as f:
#     marge_annotated_org_alternate_names = f.readlines()
#
# with open("ANNOTATED_data_alon_4_relations.txt", 'r') as f:
#     marge_annotated_alon = f.readlines()
#
# with open("ANNOTATED_age_3.txt", 'r') as f:
#     marge_annotated_age_3 = f.readlines()
#
# with open("ANNOTATED_employee_of.txt", 'r') as f:
#     marge_annotated_employee_of = f.readlines()
#
# with open("ANNOTATED_date_of_birth.txt", 'r') as f:
#     marge_annotated_date_of_birth = f.readlines()
#
# marge_annotated = marge_annotated_alon + marge_annotated_age_3 + marge_annotated_employee_of + marge_annotated_date_of_birth + marge_annotated_org_alternate_names
#
# annotated_data = {}
# for l in marge_annotated:
#     line_split = l.split()
#     if line_split[1] != 'invalid':
#         annotated_data[line_split[0]] = 'no_relation' if line_split[1] == 'NA' else line_split[1]




with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples = json.load(tacred_test_file)


with open('gold_annotations.json') as json_file:
    challenge_samples = json.load(json_file)


ALL_RELS = challenge_samples

# ALL_RELS = rel_qs

# ALL_RELS = ['org:alternate_names']

# ALL_RELS = ["per:countries_of_residence"]



IS_CHALLENGE_SET = True # False True



cccc = 0



count_with_rels = 0

for RELS in ALL_RELS:


    RELS_TO_ANNOTATE = [RELS]
    REL_TO_WRITE = "_".join(RELS.split(':'))
    REL_TO_WRITE = REL_TO_WRITE.replace('/', '_')


    if IS_CHALLENGE_SET:
        real_samples = [ts for num in challenge_samples[RELS] for batch in challenge_samples[RELS][num] for ts in batch]
        REL_TO_WRITE += "_CHALLENGE_2"
        # REL_TO_WRITE += "_CHALLENGE_22222"

    else:
        real_samples = tacred_real_samples
        REL_TO_WRITE += "_tacred_REAL_2"
        # REL_TO_WRITE += "_tacred_Amir"
        # REL_TO_WRITE += "_tacred_Amir_2"






    newDict = squad_dev.copy()
    newDict['data'] = squad_dev['data'][0:1]
    newDict['data'][0]['paragraphs'] = squad_dev['data'][0]['paragraphs'][0:2]

    newDict['data'][0]['paragraphs'][0]['qas'] = squad_dev['data'][0]['paragraphs'][0]['qas'][0:2]
    newDict['data'][0]['paragraphs'][1]['qas'] = squad_dev['data'][0]['paragraphs'][1]['qas'][0:2]

    newDict['data'][0]['paragraphs'] = []

    print("ASDFGHJ")
    print(RELS)




    for samp in real_samples:


        if IS_CHALLENGE_SET:
            gold_relation = samp['gold']

        else:
            gold_relation = samp['relation']

        curr_context = ' '.join(samp['token'])
        curr_paragraph = {'context': curr_context, 'qas': []}

        subj, obj = get_span_of_subj_obj(samp)

        if RELS == "per:countries_of_residence":
            cccc += 1

        for idx, q  in enumerate(rel_qs[RELS]):
            # curr_question = q(subj, obj)
            if idx == 0:
                question_about = 'subj'
                curr_question = q.format(subj)

            elif idx == 1:
                question_about = 'obj'
                curr_question = q.format(obj)



                        #      MUST be the same ner type !!!!!!!

            if (samp['subj_type'] != ALL_RELATIONS_TYPES[RELS][0] or samp['obj_type'] != ALL_RELATIONS_TYPES[RELS][1]) and not IS_CHALLENGE_SET:
                continue

            if gold_relation != RELS and gold_relation != "no_relation":
                continue



            # print(samp['subj_type'],samp['obj_type'])
            # print()

            if question_about == 'subj':
                if gold_relation == RELS:
                    # count_with_rels += 1
                    answers = [{'answer_start': curr_context.find(obj), 'text': obj}]
                # elif samp['subj_type'] != 'PERSON':
                # elif samp['subj_type'] != ALL_RELATIONS_TYPES[RELS][0] and not IS_CHALLENGE_SET:
                #     continue
                elif gold_relation != RELS:
                    answers = []
                    count_with_rels += 1


            elif question_about == 'obj':
                if gold_relation == RELS:
                    # count_with_rels += 1
                    answers = [{'answer_start': curr_context.find(subj), 'text': subj}]
                # elif samp['obj_type'] != 'NUMBER' and samp['obj_type'] != 'DURATION':
                # elif samp['obj_type'] != ALL_RELATIONS_TYPES[RELS][1] and not IS_CHALLENGE_SET:
                #     continue
                elif gold_relation != RELS:
                    answers = []
                    count_with_rels += 1


            is_impossible = True if len(answers) == 0 else False

            curr_qa = {'id': samp['id'] + '_' + str(idx), 'is_impossible': is_impossible, 'question': curr_question,
                       'answers': answers}
            curr_paragraph['qas'].append(curr_qa)

        # if curr_paragraph['qas'] == []:
        #     print(curr_paragraph['qas'][32143242])
        if curr_paragraph['qas'] != []:
            newDict['data'][0]['paragraphs'].append(curr_paragraph)

    # print(json.dumps(newDict, indent=4, sort_keys=True))

    print(len(newDict['data'][0]['paragraphs']), len(newDict['data'][0]['paragraphs'])*2)

    with open('../span_bert/SpanBERT/SpanBERT/qa_rels/'+REL_TO_WRITE+'.json', 'w') as outfile:
        json.dump(newDict, outfile)





#
#
#
# for rel in dic_to_annotate:
#     if rel not in RELS_TO_ANNOTATE:
#         continue
#     for num in dic_to_annotate[rel]:
#         for idx_sents, batch in enumerate(dic_to_annotate[rel][num]):
#             if batch[0]['id'] not in annotated_data:
#                 continue
#             curr_context = ' '.join(batch[0]['token'])
#             curr_paragraph = {'context': curr_context, 'qas': []}
#
#             gold_pairs = [get_span_of_subj_obj(ts) for ts in batch if ts['id'] in annotated_data and annotated_data[ts['id']] == rel]
#             gold_index_pairs = [get_indx_and_span_of_subj_obj(ts) for ts in batch if ts['id'] in annotated_data and annotated_data[ts['id']] == rel]
#
#             doc = nlp(curr_context)
#
#             set_of_aggregated_gold = set()
#
#
#
#             aggregated_gold = []
#             for i, [index_gold_subj, index_gold_obj] in enumerate(gold_index_pairs):
#
#                 gold_subj_span, gold_subj_start, gold_subj_end = index_gold_subj[0], index_gold_subj[1], index_gold_subj[2]
#                 gold_obj_span, gold_obj_start, gold_obj_end = index_gold_obj[0], index_gold_obj[1], index_gold_obj[2]
#
#                 subj_aggregate = {index_gold_subj}
#                 obj_aggregate = {index_gold_obj}
#
#                 for j, [index_gold_subj_else, index_gold_obj_else] in enumerate(gold_index_pairs):
#
#                     gold_subj_span_else, gold_subj_start_else, gold_subj_end_else = index_gold_subj_else[0], index_gold_subj_else[1], index_gold_subj_else[2]
#                     gold_obj_span_else, gold_obj_start_else, gold_obj_end_else = index_gold_obj_else[0], index_gold_obj_else[1], index_gold_obj_else[2]
#
#                     if i != j:
#                         if gold_subj_span_else == gold_subj_span:
#                             obj_aggregate.add(index_gold_obj_else)
#
#                         if gold_obj_span_else == gold_obj_span:
#                             subj_aggregate.add(index_gold_subj_else)
#
#                 if len(subj_aggregate) > 1:
#                     # target_span = find_span(subj_aggregate, batch[0]['token'])
#                     target_ents = [e[0] for e in subj_aggregate]
#                     smallest_span = get_smallest_span(doc, target_ents)
#
#
#                     # is_target_span_np = is_np(target_span, doc)
#                     if smallest_span != "" and tuple([smallest_span, gold_obj_span]) not in set_of_aggregated_gold:
#                         set_of_aggregated_gold.add(tuple([smallest_span, gold_obj_span]))
#                         aggregated_gold.append([smallest_span, gold_obj_span])
#                     FINDED_SPAN = False
#                     ALL_NP = []
#
#                 if len(obj_aggregate) > 1:
#                     # target_span = find_span(obj_aggregate, batch[0]['token'])
#                     target_ents = [e[0] for e in obj_aggregate]
#                     smallest_span = get_smallest_span(doc, target_ents)
#
#
#                     # is_target_span_np = is_np(target_span, doc)
#                     if smallest_span != ""  and tuple([gold_subj_span, smallest_span]) not in set_of_aggregated_gold:
#                         set_of_aggregated_gold.add(tuple([gold_subj_span, smallest_span]))
#                         aggregated_gold.append([gold_subj_span, smallest_span])
#                     FINDED_SPAN = False
#                     ALL_NP = []
#
#
#             print(curr_context)
#             print()
#             print(gold_pairs)
#             print()
#             print(aggregated_gold)
#             print("_____________________________________________________________________________")
#             print()
#
#             gold_pairs = gold_pairs + aggregated_gold
#
#
#             question_set = set()
#
#             for ts in batch:
#                 if ts['id'] not in annotated_data:
#                     continue
#                 subj, obj = get_span_of_subj_obj(ts)
#                 # print(subj, "  ----  ",obj)
#                 # print()
#                 # print(ts['token'])
#                 # print()
#
#
#                 for idx, (q, question_about) in enumerate(questions_dic[rel]):
#                     curr_question = q(subj, obj)
#                     if curr_question in question_set:
#                         continue
#                     question_set.add(curr_question)
#
#                     if question_about == 'subj':
#                         answers = [{'answer_start': curr_context.find(gold_obj), 'text': gold_obj} for gold_subj, gold_obj in gold_pairs if subj == gold_subj]
#
#                     elif question_about == 'obj':
#                         answers = [{'answer_start': curr_context.find(gold_subj), 'text': gold_subj} for gold_subj, gold_obj in gold_pairs if obj == gold_obj]
#
#                     is_impossible = True if len(answers) == 0 else False
#                     curr_qa = {'id': ts['id'] + '_' + str(idx), 'is_impossible': is_impossible, 'question': q(subj, obj),
#                                'answers': answers}
#                     curr_paragraph['qas'].append(curr_qa)
#
#             if curr_paragraph['qas'] == []:
#                 print(curr_paragraph['qas'][32143242])
#
#             newDict['data'][0]['paragraphs'].append(curr_paragraph)
#
# print(json.dumps(newDict, indent=4, sort_keys=True))
#
#
# with open('../span_bert/SpanBERT/SpanBERT/qa_rels_all_span/'+REL_TO_WRITE+'.json', 'w') as outfile:
#     json.dump(newDict, outfile)
#
# # with open('../span_bert/SpanBERT/7squad_trans_new_load_model/transformers/per_age.json', 'w') as outfile:
# #     json.dump(newDict, outfile)
#
#

print("count_with_rels", count_with_rels)

print()
print(cccc)
