import os
import pandas as pd


#This is a helper program to sort all txt files in chronological order by timestamp of when each observation
#made, starting from the beginning of the patient's stay in the ICU.

#Each row of Chart_Events is structured as follows
names = ["ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME1", "CHARTTIME2","STORETIME1","STORETIME2","CGID","VALUE","VALUENUM","VALUEUOM","WARNING","ERROR"]


def sortByChartTime(dirListing, path):
    # Add all patient files in folder to in_files list
    for filename in dirListing:
        fullpath = path + filename
        try:
            df = pd.read_csv(fullpath,  sep='\t',header=None,names=names,engine = "python")
            #Sort pandas dataframe in-place by CHART_EVENTS timestamp
            df = pd.DataFrame(sorted(df.values, key=lambda x: (x[5][5:].split('-')[0], x[5][5:].split('-')[1])), columns=df.columns)
            df.to_csv(fullpath, sep="\t",index=False, header=None)
        except:
            df = pd.DataFrame()


