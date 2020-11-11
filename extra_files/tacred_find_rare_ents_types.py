import json
from collections import Counter
import math
from termcolor import colored



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



NEW_ALL_RELATIONS_TYPES = {'org:founded_by': {('ORGANIZATION', 'PERSON')}, 'per:employee_of': {('PERSON', 'ORGANIZATION'), ('PERSON', 'LOCATION')},
        'org:alternate_names': {('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:cities_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')},
        'per:children': {('PERSON', 'PERSON')}, 'per:title': {('PERSON', 'TITLE')}, 'per:siblings': {('PERSON', 'PERSON')}, 'per:religion': {('PERSON', 'RELIGION')},
        'per:age': {('PERSON', 'NUMBER'), ('PERSON', 'DURATION')}, 'org:website': {('ORGANIZATION', 'URL')}, 'per:stateorprovinces_of_residence': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:member_of': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'org:top_members/employees': {('ORGANIZATION', 'PERSON')}, 'per:countries_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')},
        'org:city_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'CITY')}, 'org:members': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:country_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'COUNTRY')}, 'per:spouse': {('PERSON', 'PERSON')},
        'org:stateorprovince_of_headquarters': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION')}, 'org:number_of_employees/members': {('ORGANIZATION', 'NUMBER')},
        'org:parents': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:subsidiaries': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'per:origin': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'org:political/religious_affiliation': {('ORGANIZATION', 'RELIGION'), ('ORGANIZATION', 'IDEOLOGY')},
        'per:other_family': {('PERSON', 'PERSON')}, 'per:stateorprovince_of_birth': {('PERSON', 'STATE_OR_PROVINCE')}, 'org:dissolved': {('ORGANIZATION', 'DATE')},
        'per:date_of_death': {('PERSON', 'DATE')}, 'org:shareholders': {('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:alternate_names': {('PERSON', 'MISC'), ('PERSON', 'PERSON')},
        'per:parents': {('PERSON', 'PERSON')}, 'per:schools_attended': {('PERSON', 'ORGANIZATION')}, 'per:cause_of_death': {('PERSON', 'CAUSE_OF_DEATH')},
        'per:city_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:stateorprovince_of_death': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:founded': {('ORGANIZATION', 'DATE')}, 'per:country_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'per:date_of_birth': {('PERSON', 'DATE')},
        'per:city_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:charges': {('PERSON', 'CRIMINAL_CHARGE')},
        'per:country_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}}


NEW_SHORT_ALL_RELATIONS_TYPES = {'org:founded_by': {('ORGANIZATION', 'PERSON')}, 'per:employee_of': {('PERSON', 'ORGANIZATION'), ('PERSON', 'LOCATION')},
        'org:alternate_names': {('ORGANIZATION', 'MISC'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:cities_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')},
        'per:children': {('PERSON', 'PERSON')}, 'per:title': {('PERSON', 'TITLE')}, 'per:siblings': {('PERSON', 'PERSON')}, 'per:religion': {('PERSON', 'RELIGION')},
        'per:age': {('PERSON', 'NUMBER'), ('PERSON', 'DURATION')}, 'org:website': {('ORGANIZATION', 'URL')}, 'per:stateorprovinces_of_residence': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:member_of': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'org:top_members/employees': {('ORGANIZATION', 'PERSON')}, 'per:countries_of_residence': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')},
        'org:city_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'CITY')}, 'org:members': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:country_of_headquarters': {('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'COUNTRY')}, 'per:spouse': {('PERSON', 'PERSON')},
        'org:stateorprovince_of_headquarters': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION')}, 'org:number_of_employees/members': {('ORGANIZATION', 'NUMBER')},
        'org:parents': {('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'LOCATION'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY')},
        'org:subsidiaries': {('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'LOCATION')},
        'per:origin': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'org:political/religious_affiliation': {('ORGANIZATION', 'RELIGION'), ('ORGANIZATION', 'IDEOLOGY')},
        'per:other_family': {('PERSON', 'PERSON')}, 'per:stateorprovince_of_birth': {('PERSON', 'STATE_OR_PROVINCE')}, 'org:dissolved': {('ORGANIZATION', 'DATE')},
        'per:date_of_death': {('PERSON', 'DATE')}, 'org:shareholders': {('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'ORGANIZATION')}, 'per:alternate_names': {('PERSON', 'MISC'), ('PERSON', 'PERSON')},
        'per:parents': {('PERSON', 'PERSON')}, 'per:schools_attended': {('PERSON', 'ORGANIZATION')}, 'per:cause_of_death': {('PERSON', 'CAUSE_OF_DEATH')},
        'per:city_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:stateorprovince_of_death': {('PERSON', 'STATE_OR_PROVINCE'), ('PERSON', 'LOCATION')},
        'org:founded': {('ORGANIZATION', 'DATE')}, 'per:country_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}, 'per:date_of_birth': {('PERSON', 'DATE')},
        'per:city_of_birth': {('PERSON', 'LOCATION'), ('PERSON', 'CITY')}, 'per:charges': {('PERSON', 'CRIMINAL_CHARGE')},
        'per:country_of_death': {('PERSON', 'LOCATION'), ('PERSON', 'COUNTRY'), ('PERSON', 'NATIONALITY')}}


SET_OF_UNIQUE_TYPES = {('PERSON', 'DURATION'), ('ORGANIZATION', 'MISC'), ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'LOCATION'), ('PERSON', 'RELIGION'), ('PERSON', 'ORGANIZATION'),
                      ('PERSON', 'NUMBER'), ('PERSON', 'LOCATION'), ('ORGANIZATION', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'DATE'), ('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'ORGANIZATION'),
                      ('PERSON', 'MISC'), ('PERSON', 'CRIMINAL_CHARGE'), ('ORGANIZATION', 'RELIGION'), ('ORGANIZATION', 'CITY'), ('ORGANIZATION', 'COUNTRY'), ('ORGANIZATION', 'NUMBER'),
                      ('PERSON', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'IDEOLOGY'), ('PERSON', 'TITLE'), ('PERSON', 'PERSON'), ('PERSON', 'COUNTRY'), ('ORGANIZATION', 'URL'),
                      ('PERSON', 'NATIONALITY'), ('PERSON', 'DATE'), ('PERSON', 'CITY')}

regex2type = {}

for regexfilename in ['regexner_caseless.tab', 'regexner_cased.tab']:
    with open(regexfilename, encoding="utf-8") as f:
        for line in f:
            l = line.rstrip('\n')
            l_split = l.split('\t')
            regex = l_split[0].lower()
            if '/' in regex:
                for sp in regex.split('/'):
                    regex2type[sp] = l_split[1]
            else:
                regex2type[regex] = l_split[1]

regex2type['poland'] = 'STATE_OR_PROVINCE'
regex2type['china'] = 'STATE_OR_PROVINCE'
regex2type['canada'] = 'STATE_OR_PROVINCE'
regex2type['mexico'] = 'STATE_OR_PROVINCE'



def make_readable_sampl(samp):
    s = samp['token'].copy()

    s[samp['subj_start']] = '<e1>' + s[samp['subj_start']]
    s[samp['subj_end']] = s[samp['subj_end']] + '</e1>'

    s[samp['obj_start']] = '<e2>' + s[samp['obj_start']]
    s[samp['obj_end']] = s[samp['obj_end']] + '</e2>'

    s_detokenize = " ".join(s)

    return {'id': samp['id'], 'token': s_detokenize}



def get_clor_entitis(sent):
    subject_str = sent[sent.find('<e1>') + 4: sent.find('</e1>')]
    object_str = sent[sent.find('<e2>') + 4: sent.find('</e2>')]
    sent = sent.replace("-LRB-", "(")
    sent = sent.replace("-RRB-", ")")
    color_sent = sent.replace(subject_str, colored(subject_str, 'blue', attrs=['bold']))
    color_sent = color_sent.replace(object_str, colored(object_str, 'green', attrs=['bold']))

    return color_sent


def merge_ents_2(ner_list, regex2type):
    text_stack = []
    span_stack = []
    type_stack = []

    ents_types_list = []
    ents_text_list = []
    ents_spans_list = []


    for i, ent in enumerate(ner_list):

        if ent[1] not in type_stack:
            if type_stack != [] and type_stack[0] != 'O':
                assert len(set(type_stack)) == 1, type_stack
                ents_spans_list.append((span_stack[0], span_stack[-1]))
                ents_text_list.append(' '.join(text_stack))
                if ' '.join(text_stack).lower() in regex2type:
                    ents_types_list.append(regex2type[' '.join(text_stack).lower()])
                    # print(regex2type[' '.join(text_stack)])
                else:
                    ents_types_list.append(type_stack[0])

            type_stack = [ent[1]]
            text_stack = [ent[0]]
            span_stack = [i]
        elif ent[1] in type_stack and ent[1] != 'O':
            type_stack.append(ent[1])
            text_stack.append(ent[0])
            span_stack.append(i)

    if text_stack is not [] and type_stack[0] != 'O':
        assert len(set(type_stack)) == 1, type_stack
        ents_spans_list.append((span_stack[0], span_stack[-1]))
        ents_text_list.append(' '.join(text_stack))
        if ' '.join(text_stack).lower() in regex2type:
            ents_types_list.append(regex2type[' '.join(text_stack).lower()])
            # print(regex2type[' '.join(text_stack)])

        else:
            ents_types_list.append(type_stack[0])

    return ents_types_list, ents_text_list, ents_spans_list


def get_number_of_combinations_per_types(ents_list, subj_t, obj_t):
    counter_ents = Counter(ents_list)
    num_of_subj_t = counter_ents[subj_t]
    num_of_obj_t = counter_ents[obj_t]

    if subj_t == obj_t:
        if num_of_subj_t < 2:
            return 0
        else:
            return math.factorial(num_of_subj_t)/math.factorial(num_of_subj_t-2)

    return num_of_subj_t * num_of_obj_t


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end'] + 1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end'] + 1])
    return subj_span, obj_span



with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/train.json") as tacred_test_file:
    tacred_real_samples_train = json.load(tacred_test_file)

with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/dev.json") as tacred_test_file:
    tacred_real_samples_dev = json.load(tacred_test_file)

with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples_test = json.load(tacred_test_file)


tacred_real_samples =  tacred_real_samples_train + tacred_real_samples_dev + tacred_real_samples_test

for r in ALL_RELATIONS_TYPES:
    print(ALL_RELATIONS_TYPES[r])


new_rels_types = {}

# for rel in NEW_ALL_RELATIONS_TYPES:
#     print("---------------------------------------------------------")
#     print(rel)
#
#     for (subj_type, obj_type) in NEW_ALL_RELATIONS_TYPES[rel]:
#
#         curr_pair_the_list_of_relation = []
#         curr_pair_the_number_of_combinations = 0
#
#
#         for samp in tacred_real_samples:
#
#             if samp['subj_type'] == subj_type and samp['obj_type'] == obj_type:
#
#                 curr_pair_the_list_of_relation.append(samp['relation'])
#
#             ner_list_word_and_type = [[tok, e_type] for tok, e_type in zip(samp['token'], samp['stanford_ner'])]
#             ents_types_list, ents_text_list, entity_spans = merge_ents_2(ner_list_word_and_type, regex2type)  # TODO
#
#             curr_number_of_combinations_per_types = get_number_of_combinations_per_types(ents_types_list, subj_type, obj_type)
#             curr_pair_the_number_of_combinations += curr_number_of_combinations_per_types
#
#         print("------------")
#         print(subj_type, obj_type)
#         print(Counter(curr_pair_the_list_of_relation))
#         print("Tagged:",len(curr_pair_the_list_of_relation),"Not tagged",curr_pair_the_number_of_combinations)








# set_of_paird_types = set()
#
# for samp in tacred_real_samples:
#     if samp['relation'] != 'no_relation':
#
#         if samp['relation'] not in new_rels_types:
#             new_rels_types[samp['relation']] = set()
#
#         new_rels_types[samp['relation']].add(tuple([samp['subj_type'], samp['obj_type']]))
#
#         set_of_paird_types.add(tuple([samp['subj_type'], samp['obj_type']]))
#
#         if samp['relation'] == 'per:employee_of' and samp['obj_type'] == 'LOCATION':
#             print("DFDSF")
#             print(get_clor_entitis(make_readable_sampl(samp)['token']))
#             print()
#
#
#
#
# print(set_of_paird_types)
# print(len(set_of_paird_types))


# list_of_types_with_one_rel = []
#
#
# for (subj_type, obj_type) in SET_OF_UNIQUE_TYPES:
#
#     curr_pair_the_list_of_relation = []
#     curr_pair_the_number_of_combinations = 0
#
#
#     for samp in tacred_real_samples:
#
#         if samp['subj_type'] == subj_type and samp['obj_type'] == obj_type:
#
#             curr_pair_the_list_of_relation.append(samp['relation'])
#
#         ner_list_word_and_type = [[tok, e_type] for tok, e_type in zip(samp['token'], samp['stanford_ner'])]
#         ents_types_list, ents_text_list, entity_spans = merge_ents_2(ner_list_word_and_type, regex2type)  # TODO
#
#         curr_number_of_combinations_per_types = get_number_of_combinations_per_types(ents_types_list, subj_type, obj_type)
#         curr_pair_the_number_of_combinations += curr_number_of_combinations_per_types
#
#     print("------------")
#     print(subj_type, obj_type)
#     print(Counter(curr_pair_the_list_of_relation))
#     print("Tagged:",len(curr_pair_the_list_of_relation),"Not tagged",curr_pair_the_number_of_combinations)
#     print("Number of different relations: ", len(Counter(curr_pair_the_list_of_relation)) - 1)
#
#     if len(Counter(curr_pair_the_list_of_relation)) - 1 == 1:
#         list_of_types_with_one_rel.append((subj_type, obj_type))
#
#
# print(list_of_types_with_one_rel)




# ('PERSON', 'CRIMINAL_CHARGE')


aaaa = Counter({'no_relation': 70, 'per:charges': 11, 'per:alternate_names': 1, 'per:origin': 1, 'per:children': 1})
print(aaaa.most_common(1))
print(aaaa.most_common(1)[0])
print(aaaa.most_common(1)[0][0])

ccc = 83.3333333333

print(round(ccc,2))

