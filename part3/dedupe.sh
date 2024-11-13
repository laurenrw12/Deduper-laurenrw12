#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 1
#SBATCH --mem=8G
#SBATCH --time=0-3
#SBATCH --output=LOG/dedupe_%j.out
#SBATCH --error=LOG/dedupe_%j.err

/usr/bin/time -v /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/Williams_deduper.py \
    -f /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/sorted_C1_SE_uniqAlign.sam \
    -o /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/output_C1_SE_uniqAlign.sam \
    -u /home/lwil/bgmp/bioinfo/Bi624/Deduper-laurenrw12/STL96.txt 
