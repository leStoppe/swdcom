#!/usr/bin/python3
import argparse
import re
import os

#r_constants = re.compile(r"equ\s+([a-zA-Z0-9_]+)\s+(a-zA-Z0-9_\$\#)")
# extract constants data. The format is value equ name 
r_constants = re.compile(r"([a-zA-Z0-9_\$\#]+)\s+equ\s+([a-zA-Z0-9_]+)")
kDictionary = {}
# line skips. If the parser sees a line starting with this, the line will be removed
r_skips = re.compile(r"^\\|\/|\(")
# matches for comments and parentheses mixed with code
r_strip_parn = re.compile (r"\(\s+[a-zA-Z0-9_\-\(\s]*\s+\)")
r_strip_slash= re.compile (r"\/\s+.*\n")
# matches for comments and parentheses on their own line
r_strip_parn_full = re.compile (r"\s*\(.*\)(\r|\n)")
r_strip_slash_full= re.compile (r"\s*\/\s+.*(\r|\n)")

def extract_constants (filename):
    kDictionary = {}
    fh = open (filename, 'r')
    for line in fh:
        match = r_constants.findall(line)
        if (match):
            label = match[0][1]
            value = match[0][0]
            kDictionary[label] = value
    fh.close()
    return kDictionary

def process_forth_source (sourcefile, constants):
    outputfile = sourcefile + ".swp"
    fh_in = open(sourcefile, 'r')
    fh_out = open(outputfile, 'w')
    for line in fh_in:
        #line = r_strip_slash_full.sub('', line)
        #line = r_strip_parn_full.sub('', line)
        line = r_strip_parn.sub('', line)
        line = r_strip_slash.sub('', line)
        if ( len(line) <= 1 ):
            continue
        print (line)
        print (len(line) )

        split_line = re.split("\s+", line)
        processed_line = ''
        for word in split_line:
            if (word in constants.keys() ):
                word = constants[word]
            processed_line = processed_line + word + " "
        fh_out.write(processed_line + "\n")
    fh_in.close()
    fh_out.close()
    originalbackup = sourcefile + ".bak"
    if (os.path.exists(originalbackup) ):
        os.remove (originalbackup)
    os.rename(sourcefile, originalbackup)
    os.rename(outputfile, sourcefile)

def process_forth_source_org (sourcefile, constants):
    outputfile = sourcefile + ".swp"
    fh_in = open(sourcefile, 'r')
    fh_out = open(outputfile, 'w')
    for line in fh_in:
        if ( r_skips.findall(line) ):
            continue
        else:
            split_line = re.split("\s+", line)
            processed_line = ''
            for word in split_line:
                if (word in constants.keys() ):
                    word = constants[word]
                processed_line = processed_line + word + " "
        fh_out.write(processed_line + "\n")
    fh_in.close()
    fh_out.close()
    originalbackup = sourcefile + ".bak"
    if (os.path.exists(originalbackup) ):
        os.remove (originalbackup)
    os.rename(sourcefile, originalbackup)
    os.rename(outputfile, sourcefile)

parser = argparse.ArgumentParser(
                    prog="SWDCOMM (swd2) forth preprocessor",
                    description="Takes a list of equ constants and replaces references int the forth code to avoid using constants",
                    epilog="----------------------------------")

parser.add_argument('-k', '--constants', dest='constantsfile', action='store', required=True, help='file with list of constants')
parser.add_argument('-fs', '--forth-file', dest='forthfile', action='store', required=True, help='forth source code')

args = parser.parse_args()
print (args.constantsfile)
print (args.forthfile)

kDictionary = extract_constants(args.constantsfile)
process_forth_source(args.forthfile, kDictionary)

