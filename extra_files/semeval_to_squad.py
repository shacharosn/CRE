import json
import random

ent_rel = {
"ORGANIZATION ORGANIZATION": ['org:alternate_names', 'org:parents', 'org:subsidiaries', 'org:member_of', 'org:members', 'org:shareholders'],
"PERSON CITY": ['per:cities_of_residence', 'per:city_of_death', 'per:city_of_birth'],
"PERSON COUNTRY": ['per:countries_of_residence', 'per:origin', 'per:country_of_death', 'per:country_of_birth'],
"PERSON MISC": ['per:alternate_names'],
"ORGANIZATION MISC": ['org:alternate_names'],
"ORGANIZATION LOCATION": ['org:country_of_headquarters', 'org:parents', 'org:stateorprovince_of_headquarters', 'org:city_of_headquarters', 'org:subsidiaries', 'org:member_of'],
"PERSON PERSON": ['per:parents', 'per:children', 'per:siblings', 'per:alternate_names', 'per:other_family', 'per:spouse'],
"PERSON TITLE": ['per:title'],
"PERSON ORGANIZATION": ['per:employee_of', 'per:schools_attended'],
"PERSON LOCATION": ['per:cities_of_residence', 'per:stateorprovinces_of_residence', 'per:stateorprovince_of_death', 'per:employee_of', 'per:city_of_death', 'per:countries_of_residence'],
"ORGANIZATION PERSON": ['org:top_members/employees', 'org:founded_by', 'org:shareholders'],
"ORGANIZATION URL": ['org:website'],
"ORGANIZATION COUNTRY": ['org:country_of_headquarters', 'org:members', 'org:parents', 'org:member_of'],
"PERSON DURATION": ['per:age'],
"PERSON NUMBER": ['per:age'],
"ORGANIZATION DATE": ['org:founded', 'org:dissolved'],
"ORGANIZATION NUMBER": ['org:number_of_employees/members'],
"PERSON NATIONALITY": ['per:origin', 'per:country_of_birth', 'per:countries_of_residence'],
"PERSON DATE": ['per:date_of_birth', 'per:date_of_death'],
"PERSON CAUSE_OF_DEATH": ['per:cause_of_death'],
"PERSON RELIGION": ['per:religion'],
"PERSON CRIMINAL_CHARGE": ['per:charges'],
"PERSON STATE_OR_PROVINCE": ['per:stateorprovince_of_death', 'per:stateorprovinces_of_residence', 'per:stateorprovince_of_birth'],
"ORGANIZATION RELIGION": ['org:political/religious_affiliation'],
"ORGANIZATION CITY": ['org:city_of_headquarters'],
"ORGANIZATION STATE_OR_PROVINCE": ['org:stateorprovince_of_headquarters'],
"ORGANIZATION IDEOLOGY": [],
}

ALL_RELS = {'Content-Container', 'Component-Whole', 'Product-Producer', 'Instrument-Agency', 'Member-Collection', 'Entity-Origin', 'Entity-Destination', 'Message-Topic', 'Cause-Effect'}

# rel_qs={}
# rel_qs['Content-Container'] = ("Where is the {} stored?", 'What is stored in the {}?')
# rel_qs['Component-Whole'] = ("What whole is the {} component of?", 'What is the component of the {}?')
# rel_qs['Product-Producer'] = ("Who produces {}?", 'What does {} produce?')
# rel_qs['Instrument-Agency'] = ("Who uses a {}?", 'What does {} use?')
# rel_qs['Member-Collection'] = ("What collection {} is part of?", 'What is a fraction of {}?')
# rel_qs['Entity-Origin'] = ("Where does {} come from?", 'What comes from {}?')
# rel_qs['Entity-Destination'] = ("What is the {}'s destination?", 'Who does {} serve as a destination?')
# rel_qs['Message-Topic'] = ("What is the topic of the {}?", 'Who does {} serve as a topic?')
# rel_qs['Cause-Effect'] = ("What caused the {}?", 'From what {} caused')



# rel_qs={}
# rel_qs['Content-Container'] = ("Content-Container h {}", 'Content-Container t {}')
# rel_qs['Component-Whole'] = ("Component-Whole h {}", 'Component-Whole t {}')
# rel_qs['Product-Producer'] = ("Product-Producer h {}", 'Product-Producer t {}')
# rel_qs['Instrument-Agency'] = ("Instrument-Agency h {}", 'Instrument-Agency t {}')
# rel_qs['Member-Collection'] = ("Member-Collection h {}", 'Member-Collection t {}')
# rel_qs['Entity-Origin'] = ("Entity-Origin h {}", 'Entity-Origin t {}')
# rel_qs['Entity-Destination'] = ("Entity-Destination h {}", 'Entity-Destination t {}')
# rel_qs['Message-Topic'] = ("Message-Topic h {}", 'Message-Topic t {}')
# rel_qs['Cause-Effect'] = ("Cause-Effect h {}", 'Cause-Effect t {}')



rel_qs={}
rel_qs['Content-Container'] = ("r1 h {}", 'r1 t {}')
rel_qs['Component-Whole'] = ("r2 h {}", 'r2 t {}')
rel_qs['Product-Producer'] = ("r3 h {}", 'r3 t {}')
rel_qs['Instrument-Agency'] = ("r4 h {}", 'r4 t {}')
rel_qs['Member-Collection'] = ("r5 h {}", 'r5 t {}')
rel_qs['Entity-Origin'] = ("r6 h {}", 'r6 t {}')
rel_qs['Entity-Destination'] = ("r7 h {}", 'r7 t {}')
rel_qs['Message-Topic'] = ("r8 h {}", 'r8 t {}')
rel_qs['Cause-Effect'] = ("r9 h {}", 'r9 t {}')





# rel_qs['per:date_of_birth'] = ("When was {} born?", 'Who was born in {}?')
# rel_qs['per:title'] = ("What is {}'s title?", "Who has the title {}")
# rel_qs['org:top_members/employees'] = ('Who are the top members of the organization {}?', 'What organization is {} a top member of?')
# rel_qs['org:country_of_headquarters'] = ('In what country the headquarters of {} is?', "What organization have it's headquarters in {}?")
# rel_qs['per:parents'] = ('Who are the parents of {}?', "Who are the children of {}?")
# rel_qs['per:age'] = ("What is {}'s age?", "Whose age is {}?")
# rel_qs['per:countries_of_residence'] = ("What country does {} resides in?", "Who resides in country {}?")
# rel_qs['per:children'] = ("Who are the children of {}?", "Who are the parents of {}?") #  singular or plural?
# rel_qs['org:alternate_names'] = ("{} is another name for which organization?", "What are other names for {}?")
# rel_qs['org:alternate_names'] = ("What is the alternative name of the organization {}?", "What is the alternative name of the organization {}?")  #simetrical?
# rel_qs['per:charges'] = ("What are the charges of {}?", "Who was charged in {}?")
# rel_qs['per:cities_of_residence'] = ("What city does {} resides in?", "Who resides in city {}?")
# rel_qs['per:origin'] = ("What is {} origin?", "Who originates from {}?")
# rel_qs['org:founded_by'] = ("Who founded {}?", "What did {} found?")
# rel_qs['per:employee_of'] = ('Where does {} work?', 'Who is an employee of {}?')
# rel_qs['per:siblings'] = ("Who is the sibling of {}?", "Who is the sibling of {}?") #  singular or plural? simetrical?
# rel_qs['per:alternate_names'] = ("What is the alternative name of {}?", "What is the alternative name of {}?")  #simetrical?
# rel_qs['org:website'] = ("What is the URL of {}?", "What organization have the URL {}?")
# rel_qs['per:religion'] = ("What is the religion of {}", "Who believe in {}")  #?
# rel_qs['per:stateorprovince_of_death'] = ("Where did {} died?", "Who died in {}?")
# rel_qs['org:parents'] = ("What organization is the parent organization of {}?", "What organization is the child organization of {}?")
# rel_qs['org:subsidiaries'] = ("What organization is the child organization of {}?", "What organization is the parent organization of {}?")
# rel_qs['per:other_family'] = ('Who are family of {}?', "Who are family of {}?")  #Todo Too general, but it will do for now.
# rel_qs['per:stateorprovinces_of_residence'] = ("What is the state of residence of {}?", "Who lives in the state of {}?") #Todo check
# rel_qs['org:members'] = ('Who is a member of the organization {}?', 'What organization {} is member of?')
# rel_qs['per:cause_of_death'] = ('How did {} died?', "How died by {}?")  # verify
# rel_qs['org:member_of'] = ("What is the group the organization {} is member of?", "What organization is a member of {}?")  #Todo check
# rel_qs['org:number_of_employees/members'] = ("How many members does {} have?", "What organization have {} members?")
# rel_qs['per:country_of_birth'] = ("In what city was {} born", "Who was born in the city {}?")
# rel_qs['org:shareholders'] = ("Who hold shares of {}?", "What organization does {} have shares of?")
# rel_qs['org:stateorprovince_of_headquarters'] = ("What is the state or province of the headquarters of {}?", "What organization's headquarters are in the state or province {}?")  # good?
# rel_qs['per:city_of_death'] = ("In what city did {} died?", "Who died in the city {}?")
# rel_qs['per:city_of_birth'] = ("In what city was {} born?", "Who was born in the city {}?")
# rel_qs['per:spouse'] = ("Who is the spouse of {}?", "Who is the spouse of {}?")
# rel_qs['org:city_of_headquarters'] = ("Where are the headquarters of {}?", "Which organization has its headquarters in {}?")  # in what city?
# rel_qs['per:date_of_death'] = ("When did {} die?", "Who died on {}")  #if it’s a date - on, if it’s a year - in
# rel_qs['per:schools_attended'] = ("Which schools did {} attend?", "Who attended {}?")
# rel_qs['org:political/religious_affiliation'] = ("What is {} political or religious affiliation?", "Which organization has is political or religious affiliation with {}?")
# rel_qs['per:country_of_death'] = ("Where did {} die?", "Who dies in {}?")
# rel_qs['org:founded'] = ("When was {} founded?", "What organization was founded on {}?") #same issue mentioned before about the date, this time I used “in” since it will more likely be a year than a specific date
# rel_qs['per:stateorprovince_of_birth'] = ('In what state was {} born?', 'Who was born in state {}?')  # this will be the same as country/city of birth. Maybe consider all “places” together and separate them later on according to list or other words in their vicinity?
# # rel_qs['per:city_of_birth'] = ("Where was {} born?", "Who was born in {}?")
# rel_qs['org:dissolved'] = ("When was {} dissolved?", "Which organization was dissolved in {}?")

new_questions_id = -2
def extruct_ent(tokens, start, end):
    return ' '.join(tokens[start: end + 1])

def generate_qas(r, relation = None, is_impossible = False):
    global new_questions_id
    if not relation:
        relation = r['relation']
    raw = rel_qs[relation]
    context = ' '.join(r['token'])
    subj = extruct_ent(r['token'], r['subj_start'], r['subj_end'])
    obj = extruct_ent(r['token'], r['obj_start'], r['obj_end'])

    if is_impossible:
        answer_obj = []
        answer_subj = []
    else:
        answer_obj = [{'text': obj, 'answer_start': context.find(obj)}]
        answer_subj = [{'text': subj, 'answer_start': context.find(subj)}]
    new_questions_id += 2
    print("adfds")
    return [{'is_impossible': is_impossible, 'question': raw[0].format(subj), 'id_rel': r['id'], 'answers': answer_obj, 'id': str(new_questions_id), 'rel': relation},
            {'is_impossible': is_impossible, 'question': raw[1].format(obj),'answers': answer_subj,  'id_rel': r['id'], 'id': str(new_questions_id +1), 'rel': relation }]


def create_qa(r):
    item = {'title': r['relation']}
    context = ' '.join(r['token'])
    qas = []
    if r['relation'] != 'no_relation':
        qas.extend(generate_qas(r))
    for other_r in ALL_RELS: #ent_rel['{} {}'.format(r['subj_type'], r['obj_type'])]:
        if other_r == r['relation']:
            continue
        qas.extend(generate_qas(r, other_r, True))
        random.shuffle(qas)
    par = [{'context': context, 'qas': qas, 'subj':extruct_ent(r['token'], r['subj_start'], r['subj_end']), 'obj': extruct_ent(r['token'], r['obj_start'], r['obj_end'])}]
    item['paragraphs'] = par
    return item


def merge_squad(s1, s2):
    s1['data'].extend(s2['data'])
    random.shuffle(s1['data'])
    return s1

if '__main__' ==__name__:
    filetype = "test"
    if filetype == "train":
        new_questions_id = 1000000
    if filetype == "test":
        new_questions_id = 2000000
    # with open("/home/nlp/amirdnc/data/squad2/{}-v2.0.json".format(filetype)) as f:
    #     s1 = json.load(f)
    # with open("/home/nlp/amirdnc/data/squad2/tac_{}.json".format(filetype)) as f:
    #     s2 = json.load(f)
    # out = merge_squad(s1, s2)
    # with open("/home/nlp/amirdnc/data/squad2/tac_unified_{}.json".format(filetype), 'w') as f:
    #     json.dump(out, f)
    # print("Done - {}".format(filetype))
    # exit()
    with open("/home/nlp/sharos/TRE/datasets/test_semeval_as_tacred.json") as f:
        d = json.load(f)
    res = {'version': 'v2.1'}
    res['data'] = []
    for r in d:
        res['data'].append(create_qa(r))
    with open("/home/nlp/sharos/TRE/datasets/semeval_markers/sem_{}.json".format(filetype), 'w') as f:
        json.dump(res, f)

    print("Done - {}".format(filetype))
