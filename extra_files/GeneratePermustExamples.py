import json
from collections import Counter

ALL_RELATIONS_TYPES = {'per:title': ['PERSON', 'TITLE'], 'org:top_members/employees': ['ORGANIZATION', 'PERSON'], 'org:country_of_headquarters': ['ORGANIZATION', 'COUNTRY'], 'per:parents': ['PERSON', 'PERSON'], 'per:age': ['PERSON', 'DURATION'], 'per:countries_of_residence': ['PERSON', 'COUNTRY'], 'per:children': ['PERSON', 'PERSON'], 'org:alternate_names': ['ORGANIZATION', 'ORGANIZATION'], 'per:charges': ['PERSON', 'CRIMINAL_CHARGE'], 'per:cities_of_residence': ['PERSON', 'CITY'], 'per:origin': ['PERSON', 'NATIONALITY'], 'org:founded_by': ['ORGANIZATION', 'PERSON'], 'per:employee_of': ['PERSON', 'ORGANIZATION'], 'per:siblings': ['PERSON', 'PERSON'], 'per:alternate_names': ['PERSON', 'PERSON'], 'org:website': ['ORGANIZATION', 'URL'], 'per:religion': ['PERSON', 'RELIGION'], 'per:stateorprovince_of_death': ['PERSON', 'LOCATION'], 'org:parents': ['ORGANIZATION', 'ORGANIZATION'], 'org:subsidiaries': ['ORGANIZATION', 'ORGANIZATION'], 'per:other_family': ['PERSON', 'PERSON'], 'per:stateorprovinces_of_residence': ['PERSON', 'STATE_OR_PROVINCE'], 'org:members': ['ORGANIZATION', 'ORGANIZATION'], 'per:cause_of_death': ['PERSON', 'CAUSE_OF_DEATH'], 'org:member_of': ['ORGANIZATION', 'LOCATION'], 'org:number_of_employees/members': ['ORGANIZATION', 'NUMBER'], 'per:country_of_birth': ['PERSON', 'COUNTRY'], 'org:shareholders': ['ORGANIZATION', 'ORGANIZATION'], 'org:stateorprovince_of_headquarters': ['ORGANIZATION', 'STATE_OR_PROVINCE'], 'per:city_of_death': ['PERSON', 'CITY'], 'per:date_of_birth': ['PERSON', 'DATE'], 'per:spouse': ['PERSON', 'PERSON'], 'org:city_of_headquarters': ['ORGANIZATION', 'CITY'], 'per:date_of_death': ['PERSON', 'DATE'], 'per:schools_attended': ['PERSON', 'ORGANIZATION'], 'org:political/religious_affiliation': ['ORGANIZATION', 'RELIGION'], 'per:country_of_death': ['PERSON', 'COUNTRY'], 'org:founded': ['ORGANIZATION', 'DATE'], 'per:stateorprovince_of_birth': ['PERSON', 'STATE_OR_PROVINCE'], 'per:city_of_birth': ['PERSON', 'CITY'], 'org:dissolved': ['ORGANIZATION', 'DATE']}
SET_OF_ALL_TYPES = {('PERSON', 'STATE_OR_PROVINCE'), ('ORGANIZATION', 'ORGANIZATION'), ('ORGANIZATION', 'DATE'), ('PERSON', 'DATE'), ('ORGANIZATION', 'LOCATION'), ('PERSON', 'LOCATION'), ('PERSON', 'NATIONALITY'), ('ORGANIZATION', 'URL'), ('PERSON', 'ORGANIZATION'), ('ORGANIZATION', 'COUNTRY'), ('PERSON', 'CITY'), ('PERSON', 'TITLE'), ('ORGANIZATION', 'CITY'), ('PERSON', 'RELIGION'), ('PERSON', 'CRIMINAL_CHARGE'), ('ORGANIZATION', 'RELIGION'), ('PERSON', 'COUNTRY'), ('ORGANIZATION', 'NUMBER'), ('PERSON', 'PERSON'), ('PERSON', 'DURATION'), ('PERSON', 'CAUSE_OF_DEATH'), ('ORGANIZATION', 'PERSON'), ('ORGANIZATION', 'STATE_OR_PROVINCE')}

ID_COUNTER = 0

def generator_model_input(indxs_subject, indxs_object, wiki_ner_list_all, toks, tacred_id, et_of_subj, et_of_obj, rel):
    global ID_COUNTER
    ID_COUNTER += 1


    new_sample = {'id': tacred_id+"_"+et_of_subj+"_"+et_of_obj+"_"+str(ID_COUNTER), 'docid': 2, 'relation': rel, 'token': toks,
                  'subj_start': indxs_subject[0], 'subj_end': indxs_subject[1], 'obj_start': indxs_object[0],
                  'obj_end': indxs_object[1], 'stanford_ner': wiki_ner_list_all, 'subj_type': et_of_subj,
                  'obj_type': et_of_obj}

    return new_sample


def merge_ents_2(ner_list):
    text_stack = []
    span_stack = []
    type_stack = []

    ents_types_list = []
    ents_text_list = []
    ents_spans_list = []

    for i, ent in enumerate(ner_list):
        #         print(type_stack, span_stack, text_stack)

        if ent[1] not in type_stack:
            if type_stack != [] and type_stack[0] != 'O':
                assert len(set(type_stack)) == 1, type_stack
                ents_types_list.append(type_stack[0])
                ents_spans_list.append((span_stack[0], span_stack[-1]))
                ents_text_list.append(' '.join(text_stack))

            type_stack = [ent[1]]
            text_stack = [ent[0]]
            span_stack = [i]
        elif ent[1] in type_stack and ent[1] != 'O':
            type_stack.append(ent[1])
            text_stack.append(ent[0])
            span_stack.append(i)

    if text_stack is not [] and type_stack[0] != 'O':
        assert len(set(type_stack)) == 1, type_stack
        ents_types_list.append(type_stack[0])
        ents_spans_list.append((span_stack[0], span_stack[-1]))
        ents_text_list.append(' '.join(text_stack))

    return ents_types_list, ents_text_list, ents_spans_list


with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples = json.load(tacred_test_file)

print(("cccccccc"))
print((tacred_real_samples[0]))
count = []
count_ORGANIZATION_PERSON = [] #['ORGANIZATION', 'PERSON']

count_all = 0

data_examples = []

SENTENCES_SET = set()

for samp_idx, samp in enumerate(tacred_real_samples):

    if tuple(samp['token']) in SENTENCES_SET:
        continue

    SENTENCES_SET.add(tuple(samp['token']))

    ner_list_word_and_type = [[tok, ner] for tok, ner in zip(samp['token'], samp['stanford_ner'])]

    ents_types_list, ents_text_list, entity_spans = merge_ents_2(ner_list_word_and_type)  # TODO


    for curr_ents in SET_OF_ALL_TYPES:
        if samp['subj_type'] == "PERSON" and samp['obj_type'] == "COUNTRY":
            print("FFFFFFFFF")


        curr_num_of_permutations = 0
        curr_num_of_permutations_ORGANIZATION_PERSON = 0
        curr_tup = []

        for i, et_subj in enumerate(ents_types_list):
            if et_subj == curr_ents[0]:

                indxs_subject = entity_spans[i]

                for j, et_obj in enumerate(ents_types_list):
                    if et_obj == curr_ents[1] and i != j:
                        if et_subj == "PERSON"  and et_obj == "COUNTRY":
                            print("FFFFFFFFF")
                            print(et_obj[52435])

                        indxs_object = entity_spans[j]

                        curr_num_of_permutations += 1
                        if et_subj == 'ORGANIZATION' and et_obj == 'PERSON':
                            curr_num_of_permutations_ORGANIZATION_PERSON += 1

                        count_all += 1
                        curr_tup.append([str(i)+ "_"+et_subj, str(j)+ "_"+et_obj])

                        the_new_model_inputs = generator_model_input(indxs_subject, indxs_object, samp['stanford_ner'],
                                                                     samp['token'],samp['id'], et_subj, et_obj, samp['relation'])

                        data_examples.append(the_new_model_inputs)


        if curr_num_of_permutations != 0:
            count.append(curr_num_of_permutations)

        if curr_num_of_permutations_ORGANIZATION_PERSON != 0:
            count_ORGANIZATION_PERSON.append(curr_num_of_permutations_ORGANIZATION_PERSON)

        # if curr_num_of_permutations > 1:
        #     count.append(curr_num_of_permutations)
        #
        #     print(data_examples)
        #     print(data_examples[32523])



    print(ents_types_list)
    print()
    print("----------------------------------------------------------------------")

with open("../span_bert/SpanBERT/permut_pred_tacred/data/json/test.json", "w") as f:
    json.dump(data_examples, f)

print("DDDDDDDDDDDDD")
print()
print(len(data_examples))
print(count_all)

for cc in count:
    print(cc)

print(len(count))

print(count)

c = Counter(count_ORGANIZATION_PERSON)

print(c)
summ = 0
for c1, c2 in c.items():
       print(c1, c2)
       summ += c1*c2
print(summ)
print(len(data_examples))

print("SENTENCES_SET len:  ", SENTENCES_SET)