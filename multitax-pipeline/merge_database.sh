#!/bin/bash
usearch=/data/baozw/software/usearch11.0.667_i86linux64

cat ./*_nop.fasta >tmp_merge.fasta
$usearch -fastx_uniques tmp_merge.fasta -fastaout merge_uniques.relabel.fasta -uc merge_uniques.relabel.uc -strand plus -threads 75 -relabel Uniq
cut -f9 merge_uniques.relabel.uc | sed 's/\+.*//g' >tmp1.txt
cut -f10 merge_uniques.relabel.uc | sed 's/\+.*//g' >tmp2.txt
cut -f1-8 merge_uniques.relabel.uc >tmp3.txt
mv merge_uniques.relabel.uc merge_uniques.relabel.raw.uc
paste tmp3.txt tmp1.txt tmp2.txt > merge_uniques.relabel.uc
python gen_relabel_uc_list.py

mkdir -p temp
mv tmp* ./temp/