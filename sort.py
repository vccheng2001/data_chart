import csv
import sys
import os
from timesort import *
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from scipy import stats
import math
import statistics as st

'''
This is a sorting algorithm to determine the most informative subject files to generate ADDs chart/graphs
of vitals trends for medical professionals to effectively monitor patient deterioration over time.
'''

#Each row of Chart_Events is structured as follows:
#|    0   |      1     |    2    |    3    |     4    |    5      |    6      |
#| ROW_ID | SUBJECT_ID | HADM_ID | ICU_STAY| ITEMID   | CHARTTIME | STORETIME |
#|    7   |     8     |   9      |   10     |    11     |      12   |    13     |     14    |
#|  CGID  |    VALUE  | VALUENUM | VALUEUOM | WARNING   |   ERROR   |   RESULT  |   STOPPED |


DURATION = 4320 #Measure continuity over 4320 minutes (3 days)

#Item ids corresponding to 5 vitals
temp_id = ["223762","676","678","223761"]
resp_id = ["618", "615", "220210", "224690"]
heart_id = ["211", "220045","220046","220047"]
#bp_id = ["51","442","455","6701","220179", "220050","8368","8440","8441","8555","220180","220051"]

#BAD: 51,6701, 8368,8555,220050,220051
bp_id = ["455","220179","8441","220180"]
spO2_id = ["646", "220277"]

path = "chart_files2/"


dict_vitals = {}
rankings = {}

class Subject:
    pass

def main():
    count=0
    # Add all patient files in folder to in_files list
    dirListing = os.listdir(path)
    sortByChartTime(dirListing,path)
    in_files = []

    for item in dirListing:
        if ".txt" in item:
            in_files.append(item)
    for i in range(len(in_files)):
        subj = Subject() #empty Subject class, with attributes id, vitals, score
        filename = in_files[i]
        subject_id = (filename.split("_"))[1]

        #----------reading text file-------------#
        raw_csv = open(path + filename)
        reader = csv.reader(raw_csv, delimiter='\t')
        chart_events = list(reader)
        # ----------reading text file-------------#
        num_rows = get_num_rows(chart_events)
        subj.id = subject_id
        if num_rows == 0:
            subj.vscore = 0
            subj.cscore = 0
        else:
            subj.vscore = get_vitals_score(chart_events, subject_id, num_rows) #VITALS SCORE
            subj.cscore =get_continuity_score(chart_events,count,subject_id) #CONTINUITY SCORE
            subj.cscore = float('%.2f' % (subj.cscore))
            avg_score = '%.2f' % ((subj.vscore + subj.cscore )/2)  # AVERAGE
            rankings[subj] = avg_score  # put into a dictionary of all subjects
        count+=1
    detailed_output(rankings)
    plt.show()


filter_bp = ["51","6701","8368","8555","220050","220051"]
#Returns vitals score out of 100 based on number of vitals measurements present in patient data
def get_vitals_score(chart_events, subject_id, num_rows):
    filter_bp_flag = 0
    dict_vitals[subject_id] = set()
    for row in chart_events:
        if row[4] in filter_bp:
            filter_bp_flag = 1
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
    vitals = dict_vitals.get(subject_id)
    if vitals == 0:
        return 0
    return ((len(vitals) - filter_bp_flag)* 20)


#Returns continuity score out of 100 based on continuity of measurements taken.
#A ks-test is conducted to test how closely the patient sample distribution function matches
#with a reference uniform distribution.
def get_continuity_score(chart_events,count,subject_id):
    times = []
    starttime = chart_events[0][5][5:]
    for row in chart_events:
        raw_charttime = row[5][5:]
        datetimeFormat = '%m-%d %H:%M:%S'
        try:
            elapsed = datetime.strptime(raw_charttime, datetimeFormat) - datetime.strptime(starttime, datetimeFormat)
        except ValueError:
            continue
        elapsed = int(elapsed.total_seconds() / 60)
        if (elapsed <= DURATION):
            times.append(elapsed)
    if times == []:
        return 0
    zeros = [subject_id]*len(times)
    plt.scatter(times,zeros, s=2) #plot all measurement timestamps over <DURATION>
    res = stats.kstest(times,'uniform',args=(0,DURATION),N=len(times))
    return (1-res[0])*100

#Returns number of rows in subject file
def get_num_rows(chart_events):
    num_rows = 0
    for row in chart_events:
        num_rows += 1
    return num_rows



#Outputs rankings to updated_rankings.txt
#Prints out Subject id, V/C scores, and overall score
def detailed_output(rankings):
    outfile = open('detailed_rankings2.txt', 'w')
    sys.stdout = outfile

    # sort subjects by score (highest to lowest out of 100)
    sorted_rankings = sorted(rankings.items(), key=lambda x: float(x[1]), reverse=True)
    for subj, score in sorted_rankings:
        c = subj.cscore
        v = subj.vscore
        print(str(subj.id) + " | V: " + str(subj.vscore) + " | C: " + str(subj.cscore) + " = " + str(rankings[subj]))
    outfile.close()


if __name__ == "__main__":
    main()