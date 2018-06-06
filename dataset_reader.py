import pandas as pd
import sys
import argparse

"""
Dataset reader script

Reads methylation, rnaseq and datasets.
"""


# functions
def getargs():
    """
    Get input arguments.
    """
    parser = argparse.ArgumentParser()
    # input data files
    parser.add_argument("datafiles", nargs="+", type="str")
    # delimiter. Default is TAB
    parser.add_argument("delimiter", const="\t")
    # file that maps patient names across files
    parser.add_argument("patient_alignment", type="str")
    # methylation aggregation method
    avail_aggregation = ["avg", "quartile"]
    parser.add_argument("aggregation", type="str", choices=avail_aggregation)
    return parser.parse()


def apply_common_patient_name(alignment_file, data):
    pass

def aggregate(dat):
    # check for uniqueness of row identifiers
    pass
# --------------------------------------------------------
# main

args = getargs()
# read all data
data = []
for infile in args.datafiles:
    dat = pd.read_csv(infile, args.delimiter)
    print("Read {} data instances from {}.".format(len(dat), infile))
    data.append(dat)

# align
apply_common_patient_name()

# write
