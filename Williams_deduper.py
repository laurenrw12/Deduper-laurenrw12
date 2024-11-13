#!/usr/bin/env python
import argparse
import re

# ./deduper.py -f /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/test_input.sam -o /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/test_output.sam -u STL96.txt 

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", required=True, type=str)
    parser.add_argument("-o", "--outfile", help="designates absolute file path to deduplicated sam file", required=True, type=str)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", required=True, type=str)
    #MAKE SURE TO ADD HELP BACK IN
    return parser.parse_args() 

args = get_args()
f = args.file
o = args.outfile
u = args.umi
#MAKE SURE TO ADD HELP BACK IN

def retrieve_identifiers(line: str) -> tuple:
    ''' doc string here'''
    # split line into columns
    line_as_list = line.strip().split("\t")
    
    #UMI = last 8 characters of column 1 
    column1 = line_as_list[0]
    umi = column1[len(column1) - 8:]

    #RNAME = column 3 
    rname = line_as_list[2]

    #FLAG = column 2 
    flag = int(line_as_list[1])
    #calculate strandedness
    if ((flag & 16) == 16):
      strand = "minus"
    else:
      strand = "plus"

    #POSITION = column 4 
    position = int(line_as_list[3])

    #CIGAR_STRING = column 6 
    cigar = line_as_list[5]
    #split up the cigar string into a list of tuples
    cigar_tuples = re.findall("([0-9]+)([A-Z])", cigar)

    return umi, rname, strand, position, cigar_tuples 
#Input: "TRUE_DUPLICATE_CASE:TTCGCCTA    0       2       130171653       36      71M     *       0       0       GTCTCTTAGTTTATTATAAACCAGCTTCATAGGCCACAGAGGAAAAAGGACTATATACATACAGCCTTTTG 6AEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEE MD:Z:53G16      NH:i:1  HI:i:1  NM:i:2  SM:i:36 XQ:i:40 X2:i:0  XO:Z:UU"
#Expected Output: ('TTCGCCTA', 2, 'plus', 130171653, [('71', 'M')])

def fix_minus_position(position: int, cigar_tuples: list) -> int:
    ''' doc string here'''
    for i in range(len(cigar_tuples)):
            if cigar_tuples[i][1] == "M" or cigar_tuples[i][1]  == "D" or cigar_tuples[i][1] == "N" or (i>0 and cigar_tuples[i][1]  == "S"):
                position += int(cigar_tuples[i][0])
    return position
#Input: 
#Expected 

# initialize
known_umis = []
unique_dict = {}
chrom_dict = {}
current_chrom = "1"
wrong_umi_counter = 0 
duplicates_removed_counter = 0 

# covert known umis textfile to list
with open(u, "r") as umis:
    for line in umis:
        umi = line.strip("\n")
        known_umis.append(umi)

with open(f, "r") as input, open(o, "w") as output:
  while True:
    line = input.readline()

    if line == "":
      #at the end of the file, save the last chrom_dict to unique_dict
      print(f'{current_chrom}\t{len(chrom_dict)}')
      for key in chrom_dict:
        unique_dict[key] = chrom_dict[key]
      break
    
    # write header lines to output file
    if line.startswith("@") == True:
      output.write(line)
      continue

    #retrieve identifers
    umi, rname, strand, position, cigar_tuples = retrieve_identifiers(line)

    if umi not in known_umis:
      wrong_umi_counter += 1
      continue

    #fix the position of plus strands with soft clipping
    if strand == "plus" and cigar_tuples[0][1] == "S":
       position -= int(cigar_tuples[0][0])
    #fix the position of all minus strands
    elif strand == "minus":
        position = fix_minus_position(position, cigar_tuples)

    #set key for dictionary
    key = (umi, rname, strand, position)

    if rname == current_chrom:
      #add to chrom dictionary if not already there
      if key not in chrom_dict:
        chrom_dict[key] = line 
      else:
        duplicates_removed_counter += 1

    else: 
      #add ALL of chrom_dict to unique dict
      print(f'{current_chrom}\t{len(chrom_dict)}')
      for dict_key in chrom_dict:
        unique_dict[dict_key] = chrom_dict[dict_key] 

      #clear chrom_dict
      chrom_dict = {}

      #set current chrom
      current_chrom = rname

      #add first line with new chrom to chrom dictionary
      chrom_dict[key] = line

  for key in unique_dict:
    output.write(unique_dict[key])

print("Number of Wrong UMIs:", wrong_umi_counter)
print("Number of Duplicates Removed:", duplicates_removed_counter)