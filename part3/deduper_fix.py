#!/usr/bin/env python
import argparse
import re
def get_arg():
   parser = argparse.ArgumentParser(description="")
   parser.add_argument("-f", help="designates absolute file path to sorted sam file", required=True, type=str)
   parser.add_argument("-o", help="designates absolute file path to deduplicated sam file", required=True, type=str)
   parser.add_argument("-u", help="designates file containing the list of UMIs", required=True, type=str)
   #parser.add_argument("-h", help="Deduper works to remove PCR duplicates added to SAM files. For kautz_deduper to work, be sure to include a -f (input file), -o (output file), and -u(UMI file). These arguments are all required for kautz_deduper to run.", required=False, type=str)
   return parser.parse_args()
args = get_arg()
f=args.f
o=args.o
u=args.u
#h=args.h
def load_umis(umi_file: str) -> set: #using a set because it is unordered and doesn't allow duplicates - UMI set doesn't need order and each element should be unique
    '''Will take a file of known UMIs (unique molecular index, indicated by -u flag) and create a set (stores multiple items in single variable) to check UMIs in each line, making sure that they're known.'''
    umi_set = set() #initializing set to add known umis to
    with open(umi_file, 'r') as infile: #will open file of known umis for reading
        for umi_line in infile:
            umi_set.add(umi_line.strip()) #for each line in the known umi infile, strip the newline character from the end of each line and add the line to the set (each line is one umi)
    return umi_set #return the set of known umis
def find_strand(bit_flag: int) -> str: #turning number of bitwise flag into string of either "plus" or "minus"
    '''Will look at the bitwise flag in element 2 of a samline and determine whether the read for that samline is on the plus or minus strand.'''
    if ((bit_flag & 16)==16): #looking at bitwise flag to determine if read is from forward or reverse strand, if bitwise flag is set to 16 read is from reverse strand
        return "-" #minus indicates reverse
    else:
        return "+" #plus indicates forward
def adjusted_pos(strand: str, cigar: list, pos: int) -> int:
    '''Will take the CIGAR string and position from samline and adjust samline starting position for softclipping, matching, alginment gaps, deletions, and insertions.'''
    if strand == "+" and cigar[0][1] == 'S': #if forward strand
        clipping_adjust = cigar[0][0] #if there is nS in the cigar string, this will take the FIRST group from the regex match. the first group will be the number associated with the soft clipping ie how many bases are soft clipped
        pos -= int(clipping_adjust) #adjusted position for forwards strand will have the soft clipping subratcted from the original start position to give the true left most 5' starting position
    elif strand == "-":
        for i in range(len(cigar)):
             if cigar[i][1] == 'S' or cigar[i][1] == 'M' or cigar[i][1] == 'N' or cigar[i][1] == 'D':
                 clipping_adjust = cigar[i][0]
                 pos += int(clipping_adjust)
    return pos
def parse_sam_line(line: str) -> tuple: #using tuple to store multiple items in a single variable, in an immutable storage method
    '''Will take one line from a SAM file and pull all necessary information for checking uniqueness: UMI, chromosome, plus/minus strand, position, CIGAR string. Stored in a tuple.'''
    elements = line.strip().split('\t') #each element in the sam read is split by a tab, and the newline is removed from the end of the line
    nec_info = () #initializing a tuple of necessary info needed from the samline
    #DELETED THIS
    col1 = elements[0]
    umi = col1[len(col1) - 8:] #splitting first element by ":" and pulling last element from new split line. this will be the last 8 characters/UMI
    chrom = elements[2] #grabbing third element of samline, chromosome
    strand = find_strand(int(elements[1])) #using function find_strand to determine if the read os on the + or - strand, turning the result into an integer and grabbing it from the second samline element
    pos = int(elements[3]) #using function adjusted_pos to adjust 5' start position for clipping according to CIGAR string, grabbing true start position from fourth element in samline
    cigar = elements[5]
    cigar_tuples = re.findall('([0-9+])([A-Z])', cigar)
    nec_info = (umi, chrom, strand, pos, cigar_tuples) #storing umi, chromosome, strand, and true start position in a tuple
    return(nec_info) #return tuple
with open(f, 'r') as input_file, open(o, 'w') as output_file: #opening input sam file for reading and output sam file for writing
    umi_set = load_umis(u) #initializing set of known umis with load_umis function and -u argparse flag
    current_chrom = "" #initializing chromosome as none to loop through each chromosome at a time
    chrom_dict = {}
    unique_dict = {} #initializing set to hold all unique samfile reads
    unknown_umi = 0 #counter to add up any instances of unknown umis
    removed_dups = 0 #counter to add up all removed duplicates
    while True:
        line = input_file.readline()
        if line == "": #if the while True loop reaches an empty line, break the loop because the file is empty
            for samline_ID in chrom_dict:
                unique_dict[samline_ID] = chrom_dict[samline_ID]
            break
        if line.startswith('@'): #if a line starts with @, it is a header line and should be written out to the output
            output_file.write(line)
            continue
        umi, chrom, strand, pos, cigar = parse_sam_line(line)
        if umi not in umi_set:
            unknown_umi += 1
            continue
        #fix postion of all minus strands and all soft clipped strands
        if strand == '-' or (strand == '+' and cigar[0][1] == 'S'):
            pos = adjusted_pos(strand, cigar, pos)
        samline_ID = (umi, strand, pos, chrom)
        if chrom == current_chrom:
            if samline_ID not in chrom_dict:
                chrom_dict[samline_ID] = line
            else:
                removed_dups += 1
        else:
            for samline_ID in chrom_dict:
                unique_dict[samline_ID] = chrom_dict[samline_ID]
            chrom_dict = {}
            current_chrom = chrom
            chrom_dict[samline_ID] = line
    for key in unique_dict:
        output_file.write(unique_dict[key])
print(f"Number of Reads With Invalid UMIs: {unknown_umi}")
print(f"Number of Duplicates Removed: {removed_dups}")