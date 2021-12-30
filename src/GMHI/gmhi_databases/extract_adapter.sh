#!/bin/bash
for f in repaired1_fastqc/fastqc_data.txt; do
    echo $f `grep -A100 ">>Overrepresented sequences" $f | \
    grep -m1 -B100 ">>END_MODULE" | \
    grep -P "Adapter|PCR" | awk '{print ">overrepresented_sequences" "_" ++c "/1" $1}'` | \
    awk '{gsub(/\/1/,"/1\n")}1' | \
    awk '{gsub(/>/,"\n>")}1' | \
    awk '{gsub(/fastqc_data.txt/,"")}1' | \
    awk 'NF > 0';
done > adapter1.txt

for f in repaired2_fastqc/fastqc_data.txt; do
    echo $f `grep -A100 ">>Overrepresented sequences" $f | \
    grep -m1 -B100 ">>END_MODULE" | \
    grep -P "Adapter|PCR" | awk '{print ">overrepresented_sequences" "_" ++c "/1" $1}'` | \
    awk '{gsub(/\/1/,"/1\n")}1' | \
    awk '{gsub(/>/,"\n>")}1' | \
    awk '{gsub(/fastqc_data.txt/,"")}1' | \
    awk 'NF > 0';
done > adapter2.txt
