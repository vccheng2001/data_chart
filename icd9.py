import os
import pandas as pd
import csv
import matplotlib.pyplot as plt

SCORE_THRESHOLD = 75
icd9_file = "icd9/DIAGNOSES_ICD.csv"
icd9_dict = {}
def main():
    scores()
    raw_csv = open(icd9_file)
    reader = csv.reader(raw_csv, delimiter=',')
    f = list(reader)
    for line in f:
        icd9_code = line[4]
        subject_id = line[1]
        if subject_id == "SUBJECT_ID":
            continue
        try:
            score = get_score(subject_id)
        except KeyError:
            continue
        if score < SCORE_THRESHOLD:
            continue
        if icd9_code not in icd9_dict:
            icd9_dict[icd9_code] = set()
            icd9_dict[icd9_code].add(subject_id)
        else:
            icd9_dict[icd9_code].add(subject_id)

    #graph out

    x = list(icd9_dict.keys())
    length_dict = {key: len(value) for key, value in icd9_dict.items()}
    y = list(length_dict.values())
    plt.bar(x,y, color='purple',width = 0.5)
    plt.xticks(x, rotation='vertical')
    plt.ylim(top=2500)
    plt.show()
    print(icd9_dict)

scores_dict = {}
score_file = "detailed_rankings.txt"
def scores():
    scores = open(score_file)
    for line in scores:
        if line.strip() == "":
            continue
        line = line.split(":")
        score = line[-1].strip()
        subject_id = line[0][8:]
        scores_dict[subject_id] = score


def get_score(subject_id):
   return float(scores_dict[subject_id])



if __name__ == "__main__":
    main()