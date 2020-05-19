import csv
import sys
import os
import pandas as pd
from datetime import datetime

#Each row of Chart_Events is structured as follows
path = "chart_files2/"
names = ["ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME1", "CHARTTIME2","STORETIME1","STORETIME2","CGID","VALUE","VALUENUM","VALUEUOM","WARNING","ERROR"]

class Subject:
    pass

def main():
    # Add all patient files in folder to in_files list
    dirListing = os.listdir(path)
    for filename in dirListing:
        fullpath = path + filename
        try:
            df = pd.read_csv(fullpath, sep='\t',header=None,names=names)
            df = df.sort_values("CHARTTIME1", ascending=True, inplace=False)
            df.to_csv(fullpath, sep="\t",index=False, header=None)
        except pd.io.common.EmptyDataError:
            df = pd.DataFrame()


if __name__ == "__main__":
    main()