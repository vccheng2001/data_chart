import os
import pandas as pd

#Each row of Chart_Events is structured as follows
names = ["ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME1", "CHARTTIME2","STORETIME1","STORETIME2","CGID","VALUE","VALUENUM","VALUEUOM","WARNING","ERROR"]


def sortByChartTime(dirListing, path):
    # Add all patient files in folder to in_files list
    for filename in dirListing:
        fullpath = path + filename
        try:
            df = pd.read_csv(fullpath, sep='\t',header=None,names=names)
            df = df.sort_values("CHARTTIME1", ascending=True, inplace=False)
            #df["CHARTTIME1"] = pd.to_datetime(df["CHARTTIME1"], format='%Y-%m-%d %H:%M:%S')
            df.to_csv(fullpath, sep="\t",index=False, header=None)
        except pd.io.common.EmptyDataError:
            df = pd.DataFrame()


