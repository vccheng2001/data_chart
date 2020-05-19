import csv
import sys
import os
import random
from timesort import *
from datetime import datetime

#Each row of Chart_Events is structured as follows:

#|    0   |      1     |    2    |    3    |     4    |    5      |    6      |
#| ROW_ID | SUBJECT_ID | HADM_ID | ICU_STAY| ITEMID   | CHARTTIME | STORETIME |
#|    7   |     8     |   9      |   10     |    11     |      12   |    13     |     14    |
#|  CGID  |    VALUE  | VALUENUM | VALUEUOM | WARNING   |   ERROR   |   RESULT  |   STOPPED |

#Item ids corresponding to 4 vitals

DATA_SIZES = [50, 250, 500, 1000, 5000]

temp_id = ["223762","676","678","223761"]
resp_id = ["618", "615", "220210", "224690"]
heart_id = ["211", "220045","220046","220047"]
bp_id = ["51","442","455","6701","220179","220050","8368","8440","8441","8555","220180","220051"]
spO2_id = ["646", "220277"]
#contains all vitals ITEM_IDs
all_vitals = temp_id + resp_id + heart_id + bp_id + spO2_id
path = "chart_files2/"

dict_vitals = {}
rankings = {}

class Subject:
    pass

def main():
    # Add all patient files in folder to in_files list
    dirListing = os.listdir(path)
    sortByChartTime(dirListing,path)
    in_files = []
    for item in dirListing:
        if ".csv" in item:
            in_files.append(item)

    for i in range(len(in_files)):
        subj = Subject() #empty Subject class, with attributes id, vitals, score
        #Opening and reading the csv file
        filename = in_files[i]
        subject_id = (filename.split("_"))[1]
        raw_csv = open(path + filename)
        reader = csv.reader(raw_csv, delimiter='\t')
        chart_events = list(reader)

        subj.id = subject_id
        subj.sscore = get_size_score(chart_events) #SIZE SCORE
        subj.vitals = get_vitals(chart_events, subject_id)
        subj.vscore = get_vitals_score(subj.vitals) #VITALS SCORE
        subj.cscore =get_continuity_score(chart_events) #CONTINUITY SCORE
        subj.cscore = float('%.2f'%(subj.cscore))
        subj.dscore = get_duration_score(chart_events)
        #calculates average of all three scores
        avg_score = '%.2f'%((subj.vscore + subj.sscore + subj.cscore)/3) #AVERAGE OUT ALL THREE SCORES
        rankings[subj]=avg_score #put into a dictionary of all subjects

    #output(rankings)
    detailed_output(rankings)

#Print output of rankings to a text file, rankings.txt
def output(rankings):
    outfile = open('rankings.txt', 'w')
    sys.stdout = outfile

    #sort subjects by score (highest to lowest out of 100)
    sorted_rankings = sorted(rankings.items(), key=lambda x: float(x[1]), reverse=True)
    for subj, score in sorted_rankings:
        print("Subject No " + str(subj.id) + " Score: " + str(score))
    outfile.close()


def detailed_output(rankings):
    outfile = open('detailed_rankings.txt', 'w')
    sys.stdout = outfile

    # sort subjects by score (highest to lowest out of 100)
    sorted_rankings = sorted(rankings.items(), key=lambda x: float(x[1]), reverse=True)
    for subj, score in sorted_rankings:
        s = subj.sscore
        v = subj.vscore
        c = subj.cscore
        print('Subject No ' + str(subj.id))
        print(f'Individual Scores: S {s} | V {v} | C {c}: ')
        print('Overall score: ' + str(score))
        print("\n")
    outfile.close()


#returns number of rows in subject file
def get_num_rows(chart_events):
    num_rows = 0
    for row in chart_events:
        num_rows += 1
    return num_rows

#returns size score based on number of rows
def get_size_score(chart_events):
    DATA_SIZES = [50, 250, 500, 1000, 2500]
    num_rows = get_num_rows(chart_events)
    for i in range(len(DATA_SIZES)):
        if num_rows < DATA_SIZES[i]:
            return (25*i)
    return 100


#returns list of all measured vitals for a given subject
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

#calculates vitals score based on how many vitals measured
def get_vitals_score(vitals):
    if vitals == None:
        return 0
    return len(vitals) * 20


#returns continuity score based on frequency at which vitals are measured
def get_continuity_score(chart_events):
    count = 0
    for row in chart_events:
        if row[4] in all_vitals:
            count += 1
    num_rows = get_num_rows(chart_events)
    if (num_rows == 0 or count == 0):
        return 0
    return (count/num_rows)*100

def get_duration_score(chart_events):
    start_time = chart_events[0][5]
    num_rows = get_num_rows(chart_events)
    last_row = num_rows - 1
    end_time = chart_events[last_row][5]
    print(start_time)
    print(end_time)
    print('\n')



if __name__ == "__main__":
    main()