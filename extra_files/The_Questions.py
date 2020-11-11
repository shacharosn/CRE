


# q1_org_founded = lambda org,date: 'When was ' + org + ' founded?'
# q2_org_founded = lambda org,date: 'What was founded on ' + date + '?'
# q3_org_founded = lambda org,date: f'On what date was {org} founded?'
#
# qg1_org_founded = lambda org,date: f'What organization was founded on some date ?'  #  TODO: ask yoav
# qg4_org_founded = lambda org,date: f"What organization's founding date is mentioned ?"  #  TODO: ask yoav
# qg2_org_founded = lambda org,date: 'On what date was an organization founded?'
# qg3_org_founded = lambda org,date: 'When was any organization founded?'
#
# q1_per_age = lambda per,age: "What is " + per + "'s age?"
# q2_per_age = lambda per,age: "Whose age is "+ age + "?"
#
# qg1_per_age = lambda per,age: f"Which number in the test is an age?"
# qg2_per_age = lambda per,age: f"Whose age is mentioned in the text?" #GOOD
#
# q1_per_date_of_birth = lambda per,date_of_birth: "What is " + per + "'s date of birth?"
# q2_per_date_of_birth = lambda per,date_of_birth: "Who was born on " + date_of_birth + "?"
#
# qg1_per_date_of_birth = lambda per,date_of_birth: f"Whose date of birth is mentioned?"
# qg2_per_date_of_birth = lambda per,date_of_birth: f"When was anyone born?"
#
# q1_org_founded_by = lambda org,per: "Who founded " + org + "?"
# q2_org_founded_by = lambda org,per: "What did " + per + " found?"
# # q2_org_founded_by = lambda org,per: "What was founded by " + per + "?"
#
# qg1_org_founded_by = lambda org,date: 'Who founded an organization?'
# qg2_org_founded_by = lambda org,date: f"What organization someone found?"
# qg3_org_founded_by = lambda org,date: f"Which organization's founder is mentioned?"
#
# q1_per_schools_attended = lambda per,org: "Which school did " + per + " attend?"
# q2_per_schools_attended = lambda per,org: "Who attended " + org + "?"
#
# qg1_per_schools_attended = lambda per,org: "Which school did someone attend?"
# qg2_per_schools_attended = lambda per,org: "Who attended a school?"
#
# q1_per_employee_of = lambda per,org: "Who employs " + per + "?"
# q2_per_employee_of = lambda per,org: "Who is employee of " + org + "?"
#
# qgg1_per_employee_of = lambda per,org: "Who employs someone?"
# qgg2_per_employee_of = lambda per,org: "Who was employed by an organization?"
#
# qg1_per_employee_of = lambda per,org: "Which organization's employee is mentioned?"
# qg2_per_employee_of = lambda per,org: "Whose employing organization is mentioned?"
#
# # q1_per_employee_of = lambda per,org: "What company does " + per + " work for?"
# # q2_per_employee_of = lambda per,org: "Who works for " + org + "?"
#
#
#
#
#
# questions_dic = {}
#
# questions_dic['org:founded'] = [[q1_org_founded, 'subj'], [q2_org_founded, 'obj']]
# questions_dic['per:age'] = [[q1_per_age, 'subj'], [q2_per_age, 'obj']]
# questions_dic['per:date_of_birth'] = [[q1_per_date_of_birth, 'subj'], [q2_per_date_of_birth, 'obj']]
# questions_dic['org:founded_by'] = [[q1_org_founded_by, 'subj'], [q2_org_founded_by, 'obj']]
# questions_dic['per:schools_attended'] = [[q1_per_schools_attended, 'subj'], [q2_per_schools_attended, 'obj']]
# questions_dic['per:employee_of'] = [[q1_per_employee_of, 'subj'], [q2_per_employee_of, 'obj']]


aaa = ['org:top_members/employees', 'per:parents', 'org:parents', 'org:subsidiaries', 'per:children']

import json

rel_qs={}

rel_qs['per:date_of_birth'] = ("What is {}'s date of birth?", 'Who was born on {}?')
rel_qs['per:title'] = ("What is {}'s title?", "Who has the title {}")
rel_qs['org:top_members/employees'] = ('Who are the top members of {}?', 'What organization is {} a top member of?')
rel_qs['org:country_of_headquarters'] = ('In what country the headquarters of {} is?', 'What organization have it\'s headquarters in {}')
rel_qs['per:parents'] = ('Who are the parents of {}?', "Who are the children of {}?")
rel_qs['per:age'] = ("What is {}'s age?", "Whose age is {}?")
rel_qs['per:countries_of_residence'] = ("What is {}'s countries of residence?", "Who resides in {}?")
rel_qs['per:children'] = ("Who are the children of {}?", "Who are the parent of {}?") #  singular or plural?
# rel_qs['org:alternate_names'] = ("{} is another name for which organization?", "What are other names for {}?")
rel_qs['org:alternate_names'] = ("What is the alternative name of  {}?", "What is the alternative name of {}?")  #simetrical?
rel_qs['per:charges'] = ("What are the charges of {}?", "Who was charged in {}?")
rel_qs['per:cities_of_residence'] = ("What city does {} resides in?", "Who resides in city {}?")
rel_qs['per:origin'] = ("What is {} origin?", "Who originates from {}?")
rel_qs['org:founded_by'] = ("Who founded {}?", "What did {} found?")
rel_qs['per:employee_of'] = ('Who employs {}?', 'Who is employee of {}?')

rel_qs['per:siblings'] = ("Who are the siblings of {}?", "Who are the siblings of {}?") #  singular or plural? simetrical?
rel_qs['per:alternate_names'] = ("What is the alternative name of  {}?", "What is the alternative name of {}?")  #simetrical?

rel_qs['org:website'] = ("What is the URL of {}?", "What organization have the URL {}?")
rel_qs['per:religion'] = ("What is the religion of {}", "Who belongs to the {} religion?")  #?
rel_qs['per:stateorprovince_of_death'] = ("Where did {} died?", "Who died in {}?")
rel_qs['org:parents'] = ("What organization is the parent organization of {}?", "What organization is the child organization of {}?")
# rel_qs['org:subsidiaries'] = ("Who is a subsidiary of {}?", "Who is the holding company of {}?")
rel_qs['org:subsidiaries'] = ("What organization is the child organization of {}?", "What organization is the parent organization of {}?")
rel_qs['per:other_family'] =  ('Who are family of {}?', "Who are family of {}?")  #Todo check
rel_qs['per:stateorprovinces_of_residence'] = ("What is {}'s state of residence?", "Who lives in the state of {}?") #Todo check
rel_qs['org:members'] = ('Who is a ,member of the organization {}?', 'What organization {} is member of?')
rel_qs['per:cause_of_death'] = ('How did {} died?', "How died by {}?")  # verify
rel_qs['org:member_of'] = ("What is the group {} is member of?", "Who is a member of {}?")  #Todo check
rel_qs['org:number_of_employees/members'] = ("How many employees {} have?", "What organization have {} number of employees?")
rel_qs['per:country_of_birth'] = ("In what city was {} born", "Who was born in the city {}?")
rel_qs['org:shareholders'] = ("Who hold shares of {}?", "What organization does {} have shares of?")
rel_qs['org:stateorprovince_of_headquarters'] = ("What is the state or province of the headquarters of {}?", "What organization's headquarters are in the state or province {}?")  # good?
rel_qs['per:city_of_death'] = ("What {}'s city of death?", "Who died in the city {}?")
rel_qs['per:city_of_birth'] = ("What {}'s city of birth?", "Who was born in the city {}?")
# rel_qs['per:spouse'] = ("Who is the spouse of {}?", "Who is the spouse of {}?")
rel_qs['per:spouse'] = ("Who is spouse of {}?", "Who is spouse of {}?")
rel_qs['org:city_of_headquarters'] = ("Where are the headquarters of {}?", "Which organization has its headquarters in {}?")  # in what city?
rel_qs['per:date_of_death'] = ("When is {}'s date of death?", "Who was died on {}?")  #if it’s a date - on, if it’s a year - in
rel_qs['per:schools_attended'] = ("Which schools did {} attend?", "Who attended {}?")
rel_qs['org:political/religious_affiliation'] = ("What is {} political or religious affiliation?", "Which organization has is political or religious affiliation with {}?")
rel_qs['per:country_of_death'] = ("Where did {} die?", "Who dies in {}?")
rel_qs['org:founded'] = ("When was {} founded?", "What organization was founded on {}?") #same issue mentioned before about the date, this time I used “in” since it will more likely be a year than a specific date
rel_qs['per:stateorprovince_of_birth'] = ('Where was {} born?', 'Who was born in {}?')  # this will be the same as country/city of birth. Maybe consider all “places” together and separate them later on according to list or other words in their vicinity?
# rel_qs['per:city_of_birth'] = ("Where was {} born?", "Who was born in {}?")
rel_qs['org:dissolved'] = ("When was {} dissolved?", "Which organization was dissolved in {}?")



# rel_qs['per:cities_of_residence:'] = ("Who resided in {}?", "What cities did {} reside in?")
# rel_qs['per:city_of_death:'] = ("Who died in {}?", "Where did {} die?")
# rel_qs['per:city_of_birth:'] = ("Who was born in {}?", "Where was {} born?")
# rel_qs['per:countries_of_residence:'] = ("Who resided in {}?", "What countries did {} reside in?")
# rel_qs['per:country_of_death:'] = ("Who died in {}?", "Where did {} die?")

# qg1_org_founded = lambda org,date: f'What organization was founded on some date ?'  #  TODO: ask yoav
# qg4_org_founded = lambda org,date: f"What organization's founding date is mentioned ?"  #  TODO: ask yoav
# qg2_org_founded = lambda org,date: 'On what date was an organization founded?'
# qg3_org_founded = lambda org,date: 'When was any organization founded?'
#
#
# qg1_per_age = lambda per,age: f"Which number in the test is an age?"
# qg2_per_age = lambda per,age: f"Whose age is mentioned in the text?" #GOOD
#
# q1_per_schools_attended = lambda per,org: "Which school did " + per + " attend?"
# q2_per_schools_attended = lambda per,org: "Who attended " + org + "?"
#
# qg1_per_schools_attended = lambda per,org: "Which school did someone attend?"
# qg2_per_schools_attended = lambda per,org: "Who attended a school?"
#
# q1_per_employee_of = lambda per,org: "Who employs " + per + "?"
# q2_per_employee_of = lambda per,org: "Who is employee of " + org + "?"
#
# qgg1_per_employee_of = lambda per,org: "Who employs someone?"
# qgg2_per_employee_of = lambda per,org: "Who was employed by an organization?"
#
# qg1_per_employee_of = lambda per,org: "Which organization's employee is mentioned?"
# qg2_per_employee_of = lambda per,org: "Whose employing organization is mentioned?"



# def generate_qas(r):



# def create_qa(r):
#     item = {'title': r['relation']}
#     context = ' '.join(r['token'])
#     qas = generate_qas(r)


# if '__main__' ==__name__:
    # with open("/home/nlp/amirdnc/data/tacred/data/json/train.json") as tacred_test_file:
    #     d = json.load(tacred_test_file)
    # res = {'version': 'v2.1'}
    # res['data'] = []
    # for r in d:
    #     res['data'].append(create_qa(r))


sss = ('In what country the headquarters of {} is?', 'What organization have it\'s headquarters in {}')
name = "shachar"


print(sss[1].format(name))
print('Hello, {}'.format(name))


old_string = "22ea0c33-5eb4-4017-8975-d38f9ef303bd_ORGANIZATION_PERSON_661067_0"
k = old_string.rfind("_")
new_string = old_string[:k]

print(new_string)

dsadaaa = True

l = not dsadaaa

print(l)

if not l:
    print("AAAA")

