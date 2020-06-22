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

Interesting ICD9 codes 
320-389  Diseases Of The Nervous System And Sense Organs (109)
460-519  Diseases Of The Respiratory System (166)
520-579  Diseases Of The Digestive System  (111)
580-629  Diseases Of The Genitourinary System (30)
710-739  Diseases Of The Musculoskeletal System And Connective Tissue (24)
E8859 Fall from other slipping, tripping, or stumbling  (3)
'''

SCORE_THRESHOLD = 75 #minimum score to consider
DISEASE_THRESHOLD = 3
icd9_dict = {}
scores_dict = {}
subj_disease_dict = {}
disease_count_dict = {}

codes_dict = {1:[140,240],2:[240,280],3:[280,290],4:[290,320],5:[320,390],6:[390,460],7:[460,520],8:[520,580],9:[580,630]
              ,10:[630,680],11:[680,710],12:[710,740],13:[740,760],14:[760,780],15:[780,800],16:[800,1000],17:["E000","E999"]}
#Codes to filter by"
prefixes = [(580,630)] #Respiration

#Files to read/write to
icd9_file = "icd9/DIAGNOSES_ICD.csv"
icd9_names_file = "icd9/D_ICD_DIAGNOSES.csv"
score_file = "updated_rankings.txt"




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
    print("Total patients extracted: " + str(sum_total(filtered_dict)))
    output(filtered_dict, "filtered_output_580_629.txt")
    output(subj_disease_dict, "disease_count_580_629.txt")

#Returns total number of patients extracted after filtering
def sum_total(dict):
    cnt = 0
    for key, value in dict.items():
        for v in value:
            cnt +=1
    return cnt

#Helper function to fill out a dictionary based on ICD9_codes files
def fill_dict (dict, key, value):
    if key not in dict:
        dict[key] = set()
        dict[key].add(value)
    else:
        dict[key].add(value)



#1. Puts all scores above SCORE_THRESHOLD from updated_rankings.txt into a file
# Eliminates subject files with inadequate scores
def filter_by_scores():
    scores = open(score_file)
    for line in scores:
        if line.strip() == "":
            continue
        line = line.split("|")
        score = line[-1][-6:]
        subject_id = line[0].strip()
        if float(score) >= SCORE_THRESHOLD:
            scores_dict[subject_id] = score


#2. Filter out items in dictionary by ICD9 code prefix (first three characters)
def filter_by_code(prefixes, dict):
    filtered_dict = {}
    for key, value in dict.items():
        if check_prefix(prefixes, key) == True:
             filtered_dict[key] = value
    return filtered_dict


#check if subject has specified diseases by checking against ICD9 code prefix
def check_prefix(prefixes, k):
    for prefix in prefixes:
        if type(prefix[0]) == str:
            for pre in range(int(prefix[0][1:]), int(prefix[1][1:])):
                pre = "E" + str(pre)
                if k.startswith(str(pre)):
                    return True
        else:
            for pre in range(prefix[0], prefix[1]):
                if k.startswith(str(pre)):
                    return True
    return False




def get__prefix_category():
    cats = set()
    for prefix in prefixes:
        if type(prefix[0]) == str:
            for pre in range(int(prefix[0][1:]),int(prefix[1][1:])):
                pre = "E" + str(pre)
                for k,v in codes_dict.items():
                    if type(v[0]) == str:
                        for i in range(int(v[0][1:]),int(v[1][1:])):
                            i = "E" + str(i)
                            if str(pre).startswith(str(i)):
                                cats.add(k) #k is index

                    else:
                        for i in range(v[0],v[1]):
                            if str(pre).startswith(str(i)):
                                cats.add(k) #k is index

        else:
            for pre in range(prefix[0], prefix[1]):
                for k,v in codes_dict.items():
                    if type(v[0]) == str:
                        for i in range(int(v[0][1:]),int(v[1][1:])):
                            i = "E" + str(i)
                            if str(pre).startswith(str(i)):
                                cats.add(k) #k is index
                    else:
                        for i in range(v[0],v[1]):
                            if str(pre).startswith(str(i)):
                                cats.add(k) #k is index

    print(cats)
    return cats


def get_disease_category(disease):
    for k,v in codes_dict.items():
        if type(v[0]) != str:
            for i in range(v[0], v[1]):
                if disease.startswith(str(i)):
                    return k #key
        else:
            for i in range(int(v[0][1:]),int(v[1][1:])):
                i = "E" + str(i)
                if disease.startswith(str(i)):
                    return k


#Filters out subjects who have a large amount of different diseases/conditions
#Purpose is to minimize the number of independent variables
def filter_by_subjects(dict):
    cats = get__prefix_category()
    # print("cats is ")
    # print(cats)
    for key, value in dict.items():
        subjects = value
        #check each subject for associated diseases
        for subj in subjects:
            disease_count_dict[subj] = 0
            diseases = subj_disease_dict[subj]
            for disease in diseases:

                if get_disease_category(str(disease)) not in cats:

                    disease_count_dict[subj] = disease_count_dict.get(subj, 0) + 1
            try:
                dict[key] = [subj for subj in subjects if disease_count_dict[subj] < DISEASE_THRESHOLD]
            except KeyError:
                continue




#Outputs filtered disease/patients data to text file
def output(dict, txtfile):
    outfile = open(txtfile, 'w')
    sys.stdout = outfile
    for key, value in dict.items():
        if value == []:
            continue
        else:
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