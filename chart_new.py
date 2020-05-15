import csv
import sys
import os
import random

#Each row of Chart_Events is structured as follows:

#|    0   |      1     |    2    |    3    |     4    |    5      |    6      |
#| ROW_ID | SUBJECT_ID | HADM_ID | ICU_STAY| ITEMID   | CHARTTIME | STORETIME |
#|    7   |     8     |   9      |   10     |    11     |      12   |    13     |     14    |
#|  CGID  |    VALUE  | VALUENUM | VALUEUOM | WARNING   |   ERROR   |   RESULT  |   STOPPED |

#Item ids corresponding to 4 vitals

vitalcount = 0
DATA_SIZES = [50, 250, 500, 1000, 5000]

temp_id = ["223762","676","678","223761"]
resp_id = ["618", "615", "220210", "224690"]
heart_id = ["211", "220045","220046","220047"]
bp_id = ["51","442","455","6701","220179","220050","8368","8440","8441","8555","220180","220051"]
spO2_id = ["646", "220277"]

all_vitals = temp_id + resp_id + heart_id + bp_id + spO2_id
path = "chart_files/"
dict_vitals = {}
rankings = {}
class Subject:
    pass

def sortBy(s):
    return

def main():
    # Add all patient files in folder to in_files list
    dirListing = os.listdir(path)
    in_files = []
    for item in dirListing:
        if ".csv" in item:
            in_files.append(item)

    for i in range(len(in_files)):
        subj = Subject()
        filename = in_files[i]
        subject_id = (filename.split("_"))[1]
        raw_csv = open(path + filename)
        reader = csv.reader(raw_csv, delimiter='\t')
        chart_events = list(reader)
        #get scores
        subj.id = subject_id
        subj.sscore = get_size_score(chart_events)
        #print("SIZE:" + str(subj.sscore))
        subj.vitals = get_vitals(chart_events, subject_id)
        subj.vscore = get_vitals_score(subj.vitals)
        #print("VITALS:" + str(subj.vscore))
        subj.cscore =get_continuity_score(chart_events)
        avg_score = '%.2f'%((subj.vscore + subj.sscore + subj.cscore)/3)
        rankings[subj]=avg_score


    output(rankings, in_files)

def output(rankings, in_files):
    print("Selected " + str(len(rankings)) + " patients" + " from " + str(len(in_files)))
    outfile = open('rankings.txt', 'w')
    sys.stdout = outfile
    sorted_rankings = sorted(rankings.items(), key=lambda x: float(x[1]), reverse=True)
    for subj, score in sorted_rankings:
        print("Subject No " + str(subj.id) + " Score: " + str(score))
    outfile.close()


def get_num_rows(chart_events):
    num_rows = 0
    for row in chart_events:
        num_rows += 1
    return num_rows

def get_size_score(chart_events):
    DATA_SIZES = [50, 250, 500, 1000, 2500]
    num_rows = get_num_rows(chart_events)
    for i in range(len(DATA_SIZES)):
        if num_rows < DATA_SIZES[i]:
            return (25*i)
    return 100



def get_vitals(chart_events, subject_id):
    dict_vitals[subject_id] = set()
    for row in chart_events:
        if row[4] in temp_id:
            dict_vitals[subject_id].add("temp")
        if row[4] in resp_id:
            dict_vitals[subject_id].add("resp")
        if row[4] in heart_id:
            dict_vitals[subject_id].add("heart")
        if row[4] in bp_id:
            dict_vitals[subject_id].add("bp")
        if row[4] in spO2_id:
            dict_vitals[subject_id].add("spO2")

    return dict_vitals.get(subject_id) #None if key not in dictionary

def get_vitals_score(vitals):
    if vitals == None:
        return 0
    return len(vitals) * 20



def get_continuity_score(chart_events):
    count = 0
    for row in chart_events:
        if row[4] in all_vitals:
            count += 1
    num_rows = get_num_rows(chart_events)
    if (num_rows == 0 or count == 0):
        return 0
    return (count/num_rows)*100



if __name__ == "__main__":
    main()