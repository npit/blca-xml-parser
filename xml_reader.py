import xml.etree.ElementTree as ET

import re
import argparse

"""
XML reader script for clinical data

"""


# functions
def getargs():
    """
    Get input arguments.
    """
    parser = argparse.ArgumentParser()
    # input data files
    parser.add_argument("datafiles", nargs="+", type=str)
    # tag to keep. Keep all if blank
    parser.add_argument("-tags", nargs="+",  type=str)
    return parser.parse_args()

def parse_xml(infile, tags):
    feature_vector = {}
    tree = ET.parse(infile)
    root = tree.getroot()

    patient_info = None
    for c in root:
        print(c.tag)
        if c.tag.endswith('patient'):
            patient_info = c
            break
    if not patient_info:
        print("No patient info found on file [{}]".format(infile))
        exit(1)

    for x in patient_info.getchildren():
        if not x.text: continue
        attributes = x.attrib
        use_entry = (tags and x.tag in tags) or not tags
        if use_entry:
            key = re.sub("\{.*\}", "", x.tag)
            print(key, x.text)
            assert key not in feature_vector, "Key [{}] already in feature vector"
            feature_vector[key] = x.text
    return feature_vector

    
# --------------------------------------------------------
# main

args = getargs()
# read all data
data = []
for infile in args.datafiles:
    dat = parse_xml(infile, args.tags)
    print("Read {} data instances from {}.".format(len(dat), infile))
    data.append(dat)
