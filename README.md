# Challenge RE (CRE) 
This work is a companion repository to the EMNLP 2020 paper:

[EMNLP 2020] [Exposing Shallow Heuristics of Relation Extraction Models with Challenge Data](https://www.aclweb.org/anthology/2020.emnlp-main.302/).

## Data:

The file ``challenge_set.txt`` contains the CRE evaluation set introduced in our paper, [Exposing Shallow Heuristics of Relation Extraction Models with Challenge Data](https://www.aclweb.org/anthology/2020.emnlp-main.302/). This file is formatted similarly to the TACRED release, so if your system is trained on TACRED (such as [this](https://github.com/allenai/kb)) you should be able to feed this file directly into your system. Otherwise, you may need to reformat the data to fit your system's input format. 

The fields are the same as the fields of TACRED, with the following additions:

- ``relation``:   alweys 'no_relation', this field exists to fit the format that models accept.
- ``id_relation``:   A relation in which the example is binary labeled for this given relation. 
- ``gold_relation``:   The correct label for this sentence pair (either ``[id_relation]`` or ``no_relation``)
- ``sentence_id``:  A unique identifier for the sentence in which this example is a part of.


## Evaluation:

We provide a script for evaluating a model's predictions. These predictions must be formatted in a text file with the following structure:
The file format is one example per line, in the format: ``id<TAB>prediction``
 - This file should have 10,844 lines: as the number of CRE examples.
 
There is an example file provided here: ``knowbert_preds.txt``.

To evaluate a file formatted in this way, simply run: ``python evaluate_challenge_set_output.py FILENAME``

This will give you results broken down at three levels of granularity. 
- First, it will give scors of the total accuracy, positive accuracy and negative accuracy.
- Second, it will give the true positive, false positive, true negative and false negative.
- Finally, it will give the scores of precision, recall and F1.


## Additional files

- ``extra_files``: These are scripts and additional files which were used during the creation of the dataset, and for performing the various experiments in the paper. This is pretty much a "raw dump" of the files, without any attempt to make them friendly to external use. Use at your own risk.



