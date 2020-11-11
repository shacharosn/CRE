import json
from termcolor import colored



REL = "per:age"

IS_ERROR = False   # false positive   False    True



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


def get_span_of_subj_obj(sample):
    subj_span = " ".join(sample['token'][sample['subj_start']:sample['subj_end'] + 1])
    obj_span = " ".join(sample['token'][sample['obj_start']:sample['obj_end'] + 1])
    return subj_span, obj_span


def is_valid_type(ts, rel, ALL_RELATIONS_TYPES):
    if ts['subj_type'] == ALL_RELATIONS_TYPES[rel][0] and ts['obj_type'] == ALL_RELATIONS_TYPES[rel][1]:
        return True
    return False


with open("../span_bert/SpanBERT/LDC2018T24/tacred/data/json/test.json") as tacred_test_file:
    tacred_real_samples = json.load(tacred_test_file)


with open("../span_bert/SpanBERT/SpanBERT/out_tacred/tacred/predictions.txt", 'r') as f:
    annotated_date_tacred = f.readlines()



dic_annotated_date_tacred = {}

for l in annotated_date_tacred:
    line_split = l.split()
    dic_annotated_date_tacred[line_split[0]] = line_split[1]


set_of_objs = set()






for samp in tacred_real_samples:

    if IS_ERROR:
        if dic_annotated_date_tacred[samp['id']] == REL and samp['relation'] != REL:
            print()
            print(get_clor_entitis(make_readable_sampl(samp)['token']))
            print(samp['relation'])



    else:
        if samp['relation'] == REL: # and samp['id'] == "098f665fb96a07b2cc18":
            print()
            print(get_clor_entitis(make_readable_sampl(samp)['token']))
            print(samp['relation'])


        set_of_objs.add(get_span_of_subj_obj(samp)[1])



# print(set_of_objs)