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

# ['13', '14-23', '34', '35', '36-45', '47-51', '52-56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72']
#     print("fname: ", fname)

N = 5
fname = "52-56"




with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_"+fname+".json") as json_file:
    data_examples = json.load(json_file)

print("FINISH READING FILE")
timer(start_time, time.time())


for i in range(0, N):
    curr_chunk = data_examples[i::N]

    with open("../span_bert/SpanBERT/permut_ALL_wiki_pure_exlusive_pred/data/json/test_" + fname + "_" + str(i) + ".json", 'w') as outfile:
        json.dump(curr_chunk, outfile)

    print("fname: ", fname + "_" + str(i))
    timer(start_time, time.time())
    print()

