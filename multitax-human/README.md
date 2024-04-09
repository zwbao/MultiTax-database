# MultiTax-human Database Construction Process

The file `human_16s_all.fastq` contains all human-origin full-length 16s rRNA data sequences in a FASTQ format.

```bash
# Quality Control
# Loop through all FASTQ files in the human_16s directory and perform quality control with fastp.
# Sequences shorter than 1000 bases are discarded.
ls ../human_16s/*fastq | cut -d"/" -f3 | while read id; do
    fastp -i $id -o ${id}_clean.fastq --length_required 1000;
done

# OTU (Operational Taxonomic Unit) Processing
# Preprocess clean FASTQ files for OTU analysis.
ls ../human_16s/*_clean.fastq | cut -d"/" -f3 | while read id; do
    bash preprocess_minisize4.sh $id;
done

# OTU Relabeling, output file: run_anno.txt.
# Identifies the source of each OTU.
python zotus_relabel.py
mv ./zotus_minsize4/*_relabel.fa ./zotus_relabel/
cat ./zotus_relabel/*fa > merge_zotus_relabel.fa

# De-duplication of OTUs
# Finds unique sequences among the relabeled OTUs.
usearch11.0.667_i86linux64 -fastx_uniques merge_zotus_relabel.fa -fastaout merge_zotus_uniques.relabel.fasta -uc merge_zotus_uniques.relabel.uc -strand plus -threads 75 -relabel Uniq

# Analyze the distribution of duplicate sequences across different locations
cut -f9 merge_zotus_uniques.relabel.uc > tmp1.txt
cut -f10 merge_zotus_uniques.relabel.uc > tmp2.txt
cut -f1-8 merge_zotus_uniques.relabel.uc > tmp3.txt
mv merge_zotus_uniques.relabel.uc merge_zotus_uniques.relabel.raw.uc
paste tmp3.txt tmp1.txt tmp2.txt > merge_zotus_uniques.relabel.uc

# Generate statistics on the occurrence of zotus across different locations
python gen_sampletype_list.py
mkdir -p temp
mv tmp* ./temp/
# Results in sampletype_list_df.tsv and merge_zotus_uniques.relabel.fasta

# Merge Database
# Aligns unique OTUs against a merged database, creating a reference-based OTU table.
usearch11.0.667_i86linux64 -usearch_global merge_zotus_uniques.relabel.fasta -db merge_database.udb -maxaccepts 0 -maxrejects 0 -strand both -top_hit_only -id 0 -blast6out ref_based_zotus.b6 -threads 75

cp ref_based_zotus.b6 humann_other_based_zotus.b6

python human_ref_anno.py

# Results in human_related_zotus_anno.tsv
```

Run the Python script `add_human_anno.py` to integrate human-source annotations into the merged database annotations and add human sequence names not yet included in the merged database.

Run the Python script `add_human_seq.py` to integrate new sequences from humans into the database's FASTA file:

To index the database:

```bash
usearch11.0.667_i86linux64 -makeudb_usearch merged_human_all.fasta -output merged_human_all.udb
```

This process outlines the steps taken to construct the MultiTax-human database, emphasizing quality control, operational taxonomic unit processing, and integration of human-source sequences and annotations. The objective is to create a comprehensive and reliable resource for sequence alignment and analysis, leveraging the power of usearch for database indexing and alignment tasks.