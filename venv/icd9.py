import os
import pandas as pd

icd_file = "DIAGNOSES_ICD.csv"

#sort by disease
def main():
    icd = open(icd_file)
    reader = csv.reader(icd, delimiter='\t')
    f = list(reader)
    print(f)


if __name__ == "__main__":
    main()