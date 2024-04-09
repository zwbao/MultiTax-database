#!/bin/bash
usearch=/data/baozw/software/usearch11.0.667_i86linux64

if [ ! -f merge_uniques.relabel.udb ]
then
$usearch -makeudb_usearch merge_uniques.relabel.fasta -output merge_uniques.relabel.udb
fi

if [ ! -f zotus.fa ]
then
    echo "########################################"
    echo "Start: Denoising sequences using UNOISE3..."
    echo "########################################"
    cat $1/*fastq >tmp_full_length.fastq
    $usearch -orient tmp_full_length.fastq -db merge_uniques.relabel.udb -fastaout tmp_full_length_plus.fa -threads 75 -quiet
    $usearch -fastx_uniques tmp_full_length_plus.fa -fastaout tmp_full_length_plus_uniq.fa -sizeout -minuniquesize 1 -strand plus -relabel preFLASV -threads 75 -quiet
    $usearch -unoise3 tmp_full_length_plus_uniq.fa -zotus zotus.fa -minsize 2
else
    echo "########################################"
    echo "Skip: Denoising sequences using UNOISE3..."
    echo "########################################"
    $usearch -usearch_global zotus.fa -db merge_uniques.relabel.udb -maxaccepts 0 -maxrejects 0 -top_hit_only -strand plus -id 0 -blast6out ref_based_zotus.b6 -threads 75
    python ref_anno.py
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.987 -maxrejects 0 -uc zotus_sp.uc -centroids zotus_sp.fa -sortedby other
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.945 -maxrejects 0 -uc zotus_ge.uc -centroids zotus_ge.fa -sortedby other
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.865 -maxrejects 0 -uc zotus_fa.uc -centroids zotus_fa.fa -sortedby other
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.82 -maxrejects 0 -uc zotus_or.uc -centroids zotus_or.fa -sortedby other
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.785 -maxrejects 0 -uc zotus_cl.uc -centroids zotus_cl.fa -sortedby other
    # $usearch -quiet -cluster_smallmem zotus.fa -id 0.75 -maxrejects 0 -uc zotus_ph.uc -centroids zotus_ph.fa -sortedby other
fi

