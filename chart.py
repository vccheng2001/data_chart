import csv
import sys
import os
#This program selects the most informative subjects from Chart_Events based on data size, warning flags, etc.
#The purpose is to associate subjects with ICD9 Codes (disease codes) and figure out which
#vitals need to be monitored for specific diseases.

#Each row of Chart_Events is structured as follows:

#|    0   |      1     |    2    |    3    |     4    |    5      |    6      |
#| ROW_ID | SUBJECT_ID | HADM_ID | ICU_STAY| ITEMID   | CHARTTIME | STORETIME |

#|    7   |     8     |   9      |   10     |    11     |      12   |    13     |     14    |
#|  CGID  |    VALUE  | VALUENUM | VALUEUOM | WARNING   |   ERROR   |   RESULT  |   STOPPED |

NUM_ROWS_MIN = 500
NUM_ROWS_MAX = 2500

#Item ids corresponding to 4 vitals
temp_id = ["223762","676","678","223761"]
resp_id = ["618", "615", "220210", "224690"]
heart_id = ["211", "220045","220046","220047"]
bp_id = ["51","442","455","6701","220179","220050","8368","8440","8441","8555","220180","220051"]
spO2_id = ["646", "220277"]

#Dictionaries
dict = {}
dict_vitals = {}
#Add all patient files in folder to in_files list
path = "chart_files/"
dirListing = os.listdir(path)
in_files = []
for item in dirListing:
    if ".csv" in item:
        in_files.append(item)

for i in range(len(in_files)):
    filename = in_files[i]
    subject_id = (filename.split("_"))[1]
    dict_vitals[subject_id] = set()
    raw_csv = open(path + filename)
    chart_events = csv.reader(raw_csv, delimiter='\t')

    num_rows = 0
    #Dictionary to keep track of patient vitals measurements
    for row in chart_events:
        num_rows += 1
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
    # Filter subjects by number of rows (data size)
    # Filters out subjects who have no vitals measurements
    if (num_rows < NUM_ROWS_MIN or num_rows > NUM_ROWS_MAX or len(dict_vitals[subject_id]) == 0):
        del dict_vitals[subject_id]
    else:
        dict[subject_id] = num_rows

print("Selected " + str(len(dict)) + " patients" + " from " + str(len(dirListing)))
outfile = open('vitals.txt', 'w')
sys.stdout = outfile
sorted_dict_vitals = sorted(dict_vitals.items(), key = lambda key: len(key[1]), reverse = True)
for d in sorted_dict_vitals:
    print("Subject " + str(d[0]) + " Vitals : " + str(d[1]))
outfile.close()



outfile = open('size.txt', 'w')
sys.stdout = outfile
sorted_dict= sorted(dict.items(), key=lambda x: x[1], reverse=True)
for d in sorted_dict:
    print("Subject " + str(d[0]) + ": " + str(d[1]) + " rows" )
outfile.close()


