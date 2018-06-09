import xml.etree.ElementTree as ET
import os
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
    # skip empty xml values or not
    parser.add_argument("--skipempties", action="store_true")
    return parser.parse_args()

def parse_xml(infile, tags, skip_empties=False, verbose=False):
    """
    Function that keeps all occurences of the input tags in the patient information portion of the input xml file
    """
    # output feature vector in map form
    feature_vector = {}
    # get the xml root
    tree = ET.parse(infile)
    root = tree.getroot()

    # get the patient information node in the xml
    patient_info = None
    for c in root:
        print(c.tag)
        if c.tag.endswith('patient'):
            patient_info = c
            break

    if not patient_info:
        print("No patient info found on file [{}]".format(infile))
        exit(1)

    for x in patient_info.iter():
        key = re.sub("\{.*\}", "", x.tag.strip())
        if x.text == None:
            x.text = ""
        value = x.text.strip()
        # skip empties
        if skip_empties:
            if not value: continue
        # use the entry if it's in the input tagset or no such set is defined
        if (tags and key not in tags):
            continue
        if key in feature_vector:
            i = 0
            while "{}_{}".format(key,i) in feature_vector: i+=1
            newkey = "{}_{}".format(key,i)
            print("Key {} already in vector, renaming new instance to {}".format(key, newkey))
            key = newkey
        feature_vector[key] = value
    if verbose:
        for i, (key, value) in enumerate(feature_vector.items()):
            print("{}/{} : [{}] : [{}]".format(i, len(feature_vector), key, value))
    return feature_vector

    
# --------------------------------------------------------
# main

args = getargs()
# read all data
data = []
for infile in args.datafiles:
    dat = parse_xml(infile, args.tags, verbose=True, skip_empties=args.skipempties)
    print("Read {} data instances from {}.".format(len(dat), infile))
    data.append(dat)

# write
for infile, dat in zip(args.datafiles, data):
    outfilename = os.path.basename(infile) + ".parsed-xml"
    with open(outfilename, "w") as f:
        for key,value in dat.items():
            f.write(key + " " + value + "\n")
