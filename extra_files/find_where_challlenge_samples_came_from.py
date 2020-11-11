import json
# from collections import Counter
# from collections import defaultdict
# from IPython.display import display, Markdown
# from tabulate import tabulate
# from termcolor import colored
# import pickle
import time

def timer(start,end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

start_time = time.time()

with open('gold_annotations.json') as json_file:
    the_challenge_set = json.load(json_file)

dic_of_all_challenge_ids = {}

for rel in the_challenge_set:
    for num in the_challenge_set[rel]:
        for idx_sents, batch in enumerate(the_challenge_set[rel][num]):
            for index, ts in enumerate(batch, 1):
                dic_of_all_challenge_ids[ts['id']] = []




count_id_found = 0

COUNT_ID = 0

id2num = {}

# for fname in ['13', '34', '35','14-23', '24-33','36-45', '46', '47-51', '52-56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72']:
for fname in ['13', '14-23', '34', '35', '36-45', '47-51', '52-56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72']:
    print("fname: ", fname)
    timer(start_time, time.time())

    with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_"+fname+".json") as json_file:
        data_examples = json.load(json_file)

    # curr_set_data_examples = {samp['id'] for samp in data_examples}

    for samp in data_examples:
        id2num[samp["id"]] = COUNT_ID

        COUNT_ID += 1


        # if samp["id"] in dic_of_all_challenge_ids:
        #     # print("SDGSDFFSDF")
        #
        #     dic_of_all_challenge_ids[samp["id"]].append(fname)
        #
        #     count_id_found += 1
        #     if count_id_found % 100 == 0:
        #         print("count_id_found: ", count_id_found)

    del data_examples


# print("DDDDDDD")
# print(dic_of_all_challenge_ids)

#
# with open('all_challenge_id_file_came_from.json', 'w') as outfile:
#     json.dump(dic_of_all_challenge_ids, outfile)


num2id = {id2num[iddd] : iddd for iddd in id2num}

with open('wiki_id2num.json', 'w') as outfile:
    json.dump(id2num, outfile)

with open('wiki_num2id.json', 'w') as outfile:
    json.dump(id2num, outfile)

















# with open('all_challenge_id_file_came_from.json') as json_file:
#     dic_of_all_challenge_ids = json.load(json_file)
#
#
# set_of_all_fname = set()
#
# print(type(dic_of_all_challenge_ids))
#
#
# for iidd in dic_of_all_challenge_ids:
#
#     # print(iidd, dic_of_all_challenge_ids[iidd])
#
#     if len(dic_of_all_challenge_ids[iidd]) > 1:
#         print("AAAA")
#
#     if len(dic_of_all_challenge_ids[iidd]) == 0:
#         print(iidd)
#         print("BBBB")
#
#     set_of_all_fname.add(dic_of_all_challenge_ids[iidd][0])
#
# print()
# print(len(set_of_all_fname))
# print()
# print(set_of_all_fname)
# print()
# s = [i for i in set_of_all_fname]
# s.sort()
# print(s)
# # print(dic_of_all_challenge_ids)












