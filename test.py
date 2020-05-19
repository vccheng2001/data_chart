import csv
import sys
import os
import pandas as pd
from datetime import datetime

#Each row of Chart_Events is structured as follows
path = "chart_files2/"


class Subject:
    pass

def main():
    # Add all patient files in folder to in_files list
    dirListing = os.listdir(path)
    for filename in dirListing:
        fullpath = path + filename
        #df = pd.read_csv(fullpath, delim_whitespace=True)
        df = pd.read_csv(fullpath,
                         names=['0', '1', '2', '3', '4', '5', 'Date', 'Time', '8', '9', '10', '11', '12', '13', '14'],
                         delim_whitespace=True)  # read in csv with header assignment to columns

        if df.empty:
            continue
        df = df.sort_values(['Date','Time'], ascending=[False,False], inplace=True)


        #df = df.sort_values(by=[6], ascending=True)
       # df.to_csv(fullpath, sep = "\t")



if __name__ == "__main__":
    main()