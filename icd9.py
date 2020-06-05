import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
import sys


SCORE_THRESHOLD = 80 #minimum score to consider
icd9_dict = {}
scores_dict = {}

#Codes to filter by
prefixes = ["466","480","487","511"]

#Files to read/write to
icd9_file = "icd9/DIAGNOSES_ICD.csv"
icd9_names_file = "icd9/D_ICD_DIAGNOSES.csv"
score_file = "detailed_rankings.txt"

def main():
    scores()
    #######reading diagoses ICD9 csv file#######
    raw_csv = open(icd9_file)
    reader = csv.reader(raw_csv, delimiter=',')
    f = list(reader)
    ############################################
    for line in f:
        icd9_code = line[4]
        subject_id = line[1]
        if icd9_code == "" or subject_id == "SUBJECT_ID" or subject_id not in scores_dict:
            continue
        if icd9_code not in icd9_dict:
            icd9_dict[icd9_code] = set()
            icd9_dict[icd9_code].add(subject_id)
        else:
            icd9_dict[icd9_code].add(subject_id)

    #Sort and filter icd9 codes dictionary
    icd9_dict_sorted= {k: icd9_dict[k] for k in sorted(icd9_dict)}
    filtered_dict = filter_by(prefixes, icd9_dict_sorted)
    icd9_output(filtered_dict)

#Filter out items in dictionary by ICD9 code
def filter_by(prefixes, dict):
    filtered_dict = {}
    for key, value in dict.items():
        for prefix in prefixes:
            if key.startswith(prefix) == True:
                filtered_dict[key] = value
    return filtered_dict


#Outputs filtered icd9code:{subjectIDs} to text file
def icd9_output(dict):
    outfile = open('icd9_output.txt', 'w')
    sys.stdout = outfile
    for key, value in dict.items():
        print(f"{key}: {(value)}")
    outfile.close()


#Get disease name based on ICD9 code from D_ICD_DIAGNOSES.csv
def get_disease_name(dict):
    raw_csv = open(icd9_names_file)
    reader = csv.reader(raw_csv, delimiter=',')
    for line in reader:
        icd9_code = line[1]
        name = line[2]
        try:
            dict[name] = dict.pop(icd9_code)
        except:
            continue


#Puts all scores above SCORE_THRESHOLD from detailed_rankings.txt into a file
def scores():
    scores = open(score_file)
    for line in scores:
        if line.strip() == "":
            continue
        line = line.split(":")
        score = line[-1].strip()
        subject_id = line[0][8:]
        if float(score) >= SCORE_THRESHOLD:
            scores_dict[subject_id] = score


if __name__ == "__main__":
    main()