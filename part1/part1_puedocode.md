**Define the problem:**

During PCR, the orginal DNA is duplicated MANY times. But, we want the numbers we analyze to be based on original numbers in the sample, not duplications. So, our goal is to remove all PCR duplicates and retain only a single copy of each read. 

**Write examples:**

[test_output.sam](test_output.sam)

[test_input.sam](test_input.sam)

**Develop your algorithm using pseudocode:**
```python
'''
set arguments (file, outfile, umi, help)

initialize an empty list (KNOWN_UMI)

open known UMI file (using 'r')
  while True:
    read 1 line from file (LINE)

    if end of file (LINE == ""):
      break

    add line to list of known UMIs (KNOWN_UMI = KNOWN_UMI+LIST)

initialize an empty dictionary (UNIQUE_DICT)

open input file (using 'r') & output file (using 'w') 
  while True:
    read 1 line from file (LINE)

    if end of file (LINE == ""):
      break

    if LINE starts with @:
      write to output file
      continue & move to next line

    split line by tab to get a list of each column in the line (LINE_AS_LIST)

    UMI = last 8 characters of column 1 (LINE_AS_LIST[0])
    if UMI is not in known list of UMI:
        continue & move to next line

    RNAME = column 3 (LINE_AS_LIST[2])

    FLAG = column 2 (LINE_AS_LIST[1])
    if FLAG has 16-bit:
      STRAND = "minus"
    else:
      STRAND = "plus"

    POSITION = column 4 (LINE_AS_LIST[3])
    CIGAR_STRING = column 6 (LINE_AS_LIST[4])
    if CIGAR_STRING start with nS:
      POSITION += n
    
    set KEY_LIST to list of (UMI, RNAME, STRAND, POS)

    if KEY_LIST is not a key in UNIQUE_DICT:
      add KEY_LIST to the dictionary as the key & LINE as the value

  iterate through dictionary & output all values of dictionary to output file 
'''
```

**Determine high level functions:**

This may sound crazy, but I will not have any functions. 😲

