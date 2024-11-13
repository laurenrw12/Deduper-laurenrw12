Part 1: [Pseudocode](part1_puedocode.md)

Part 2: Peer Reviews

Part 3: Write your deduper function!

    ```bash
    $ conda create --name deduper
    $ conda activate deduper
    $ conda install samtools -c bioconda
    $ samtools --version                    ### should be 1.20
    ```

**samtools sort:**
samtools sort C1_SE_uniqAlign.sam -o sorted_C1_SE_uniqAlign.sam

REPORTED NUMBERS!

Original File:
- number of header lines: 64 
```grep "^@" -c /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam```

- number of reads: 18186410
```grep -v "^@" -c /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam```

Deduped File:
- number of header lines: 64
```grep "^@" -c output_C1_SE_uniqAlign.sam```

- number of unique reads: 13719048
```grep -v "^@" -c output_C1_SE_uniqAlign.sam```

- number of wrong umis: 0 

- number of duplicates removed: 4467362


Report the number of reads per chromosome in the format <chrom_name><tab><count> with one chromosome per line (suggest copy/paste)
```grep -v "^@" output_C1_SE_uniqAlign.sam | cut -f 3 | sort -g | uniq -c ```

1   697508
2   2787018
3   547615
4   589839
5   562160
6   510818
7   1113183
8   576463
9   627488
10  564903
11  1220389
12  359951
13  467659
14  387239
15  437465
16  360923
17  517566
18  290506
19  571665
GL456210.1  5
GL456211.1  6
GL456212.1  4
GL456221.1  4
GL456233.2  656
GL456239.1  1
GL456354.1  1
GL456367.1  3
GL456368.1  3
GL456370.1  21
GL456379.1  2
GL456382.1  1
GL456383.1  1
GL456389.1  1
GL456390.1  1
GL456396.1  17
JH584295.1  111
JH584299.1  3
JH584304.1  294
MT  202002
MU069434.1  3
MU069435.1  5450
X   317853
Y   2247

How much memory did your script use to deduplicate the file? (in GB)
8GB

How long did your script run? (H:mm:ss)
0:01:09.72
