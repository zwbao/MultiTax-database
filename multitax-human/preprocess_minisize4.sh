#!/bin/bash

input_file=$1
file_name=$(basename $input_file)  # 提取文件名部分
file_name="${file_name%.*}"          # 去除文件扩展名部分
output_file=${file_name}_zotus.fa  # 加上前缀和后缀

# Find unique read sequences and abundances
usearch11.0.667_i86linux64 -fastx_uniques ./clean/${file_name}_clean.fastq -sizeout -relabel Uniq -fastaout ./uniq/${file_name}_uniq.fa

usearch11.0.667_i86linux64 -unoise3 ./uniq/${file_name}_uniq.fa -tabbedout ./zotus_minsize4/${file_name}_unoise3.txt -minsize 4 -zotus ./zotus_minsize4/$output_file

