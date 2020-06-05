import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
import sys

'''
This is an algorithm to categorize subject files into specified diseases. Subject files are filtered by
1. Scores (based on vitals completeness and continuity of data)
2. Type of disease (based on ICD9 Code)
3. Subject's other diseases 
'''

SCORE_THRESHOLD = 75 #minimum score to consider
DISEASE_THRESHOLD = 4
icd9_dict = {}
scores_dict = {}
subj_disease_dict = {}
disease_count_dict = {}

#Codes to filter by

RESPIRATORY = [(460,519)]
prefixes = [(460,519)]#[(460,466),(470,478),(480,488),(511,512)] #["466","480","487","511"]

#Files to read/write to
icd9_file = "icd9/DIAGNOSES_ICD.csv"
icd9_names_file = "icd9/D_ICD_DIAGNOSES.csv"
score_file = "detailed_rankings.txt"

def main():
    filter_by_scores()
    #######reading diagnoses ICD9 csv file#######
    raw_csv = open(icd9_file)
    reader = csv.reader(raw_csv, delimiter=',')
    f = list(reader)
    ############################################
    for line in f:
        icd9_code = line[4]
        subject_id = line[1]
        if icd9_code == "" or subject_id == "SUBJECT_ID" or subject_id not in scores_dict:
            continue
        fill_dict(subj_disease_dict,subject_id, icd9_code)
        fill_dict(icd9_dict, icd9_code, subject_id)


    #Sort and filter icd9 codes dictionary
    icd9_dict_sorted= {k: icd9_dict[k] for k in sorted(icd9_dict)}
    filtered_dict = filter_by_code(prefixes, icd9_dict_sorted)
    filter_by_subjects(filtered_dict)
    print(disease_count_dict)
    output(filtered_dict, "filtered_output.txt")
    output(subj_disease_dict, "disease_count.txt")


#Helper function to fill out a dictionary based on ICD9_codes files
def fill_dict (dict, key, value):
    if key not in dict:
        dict[key] = set()
        dict[key].add(value)
    else:
        dict[key].add(value)



#1. Puts all scores above SCORE_THRESHOLD from detailed_rankings.txt into a file
# Eliminates subject files with inadequate scores
def filter_by_scores():
    scores = open(score_file)
    for line in scores:
        if line.strip() == "":
            continue
        line = line.split(":")
        score = line[-1].strip()
        subject_id = line[0][8:]
        if float(score) >= SCORE_THRESHOLD:
            scores_dict[subject_id] = score


#2. Filter out items in dictionary by ICD9 code prefix (first three characters)
def filter_by_code(prefixes, dict):
    filtered_dict = {}
    for key, value in dict.items():
        if check_prefix(prefixes, key) == True:
             filtered_dict[key] = value
    return filtered_dict



def check_prefix(prefixes, s):
    for prefix in prefixes:
        for i in range(prefix[0], prefix[1]):
            if s.startswith(str(i)):
                return True
    return False



#Filters out subjects who have
def filter_by_subjects(dict):
    for key, value in dict.items():
        subjects = value
        #check each subject for associated diseases
        for subj in subjects:
            diseases = subj_disease_dict[subj]
            #check diseases of subject s
            for d in diseases:
                if check_prefix(prefixes, d) == False:
                    disease_count_dict[subj] = disease_count_dict.get(subj, 0) + 1
            try:
                dict[key] = [subj for subj in subjects if disease_count_dict[subj] < DISEASE_THRESHOLD]
            except KeyError:
                continue







#Outputs filtered icd9code:{subjectIDs} to text file
def output(dict, txtfile):
    outfile = open(txtfile, 'w')
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


if __name__ == "__main__":
    main()