# MultiTax Reference Database Construction Process

## Parsing the Database and Quality Control

### Greengenes2 Database Processing

```python
import csv
from Bio import SeqIO
import re

# Path to the taxonomy ID TSV file within the merged database
tsv_file = './merged_database/2022.10.taxonomy.id.tsv'
dictionary = {}

# Read the TSV file and create a dictionary mapping taxon to description
with open(tsv_file, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row

    for row in reader:
        taxon = row[0]
        des = row[1].replace("; ",";")
        des = "gg2+" + des.split(" ")[0]  # Prefix descriptions with 'gg2+'
        dictionary[taxon] = des

# Input and output file paths
in_file = open("./merged_database/2022.10.seqs.fna","r")
out_file = "./merged_database/filter_gg2.fna"

# Quality control parameters
num_degenerates = 5
homopolymer_length = 8
min_length = 1200
in_file_count = 0
out_file_count = 0

# Filter and rewrite sequences that meet quality criteria
with open(out_file, "a") as output_handle:
    for seq_record in SeqIO.parse(in_file, "fasta"):
        in_file_count += 1
        # Filtering sequences by minimum length
        if len(seq_record.seq) >= min_length:
            # Count degenerate nucleotide occurrences
            degenerates_in_seq = sum(seq_record.seq.count(nuc) for nuc in "RYMKSWHBVDN")
            # Filter sequences with excessive degenerate bases
            if not degenerates_in_seq >= num_degenerates:
                # Define and search for homopolymer patterns
                regex_str = "([ACGTURYSWKMBDHVN])\\1{%s,}" % (homopolymer_length - 1)
                if not any(re.finditer(regex_str, str(seq_record.seq))):
                    # Update sequence ID from dictionary or add prefix if not found
                    seq_record.id = dictionary.get(seq_record.id, "gg2+" + seq_record.id)
                    seq_record.name = ""
                    seq_record.description = ""
                    SeqIO.write(seq_record, output_handle, "fasta")
                    out_file_count += 1

in_file.close()

# Print statistics about the filtering process
print(f"in: {in_file_count} reads")
print(f"out: {out_file_count} reads")
print(f"filter: {in_file_count-out_file_count} reads")
```

### GTDB (Genome Taxonomy Database) Processing

The GTDB preprocessing script is tailored for sequences obtained from the Genome Taxonomy Database. The process is similar to that of the GG2 database but specifically focuses on sequences within the GTDB database, using GTDB-specific sequence IDs and descriptions.

```python
from Bio import SeqIO
import re

# Input and output file paths for GTDB sequences
in_file = open("./merged_database/ssu_all_r207.fna","r")
out_file = "./merged_database/filter_gtdb.fna"

# Parameters for quality control checks
num_degenerates = 5
homopolymer_length = 8
min_length = 1200
in_file_count = 0
out_file_count = 0

# Filter and process GTDB sequences
with open(out_file, "a") as output_handle:
    for seq_record in SeqIO.parse(in_file, "fasta"):
        in_file_count += 1
        # Filtering based on minimum sequence length
        if len(seq_record.seq) >= min_length:
            # Counting degenerate bases in the sequence
            degenerates_in_seq = sum(seq_record.seq.count(nuc) for nuc in "RYMKSWHBVDN")
            # Filtering out sequences with a high number of degenerate bases
            if not degenerates_in_seq >= num_degenerates:
                # Searching for and filtering out sequences with long homopolymers
                regex_str = "([ACGTURYSWKMBDHVN])\\1{%s,}" % (homopolymer_length - 1)
                if not any(re.finditer(regex_str, str(seq_record.seq))):
                    # Prefixing GTDB sequences with 'gtdb+' for identification
                    seq_record.id = "gtdb+" + seq_record.description.split(" ")[1]
                    seq_record.name = ""
                    seq_record.description = ""
                    SeqIO.write(seq_record, output_handle, "fasta")
                    out_file_count += 1

in_file.close()

# Reporting the count of input

 and filtered sequences
print(f"in: {in_file_count} reads")
print(f"out: {out_file_count} reads")
print(f"filter: {in_file_count-out_file_count} reads")
```

### RDP (Ribosomal Database Project) Processing

For sequences from the RDP, additional steps are taken to categorize sequences by their taxonomic classification. This involves parsing the sequence IDs to extract taxonomic ranks and appending them to the sequence ID.

```python
from Bio import SeqIO
import re

# Input and output file paths for RDP sequences
in_file = open("./merged_database/rdp_train_set_14.fa","r")
out_file = "./merged_database/filter_rdp.fna"

# Same quality control parameters as for GTDB
num_degenerates = 5
homopolymer_length = 8
min_length = 1200
in_file_count = 0
out_file_count = 0

# Filter and process RDP sequences, incorporating taxonomic information
with open(out_file, "a") as output_handle:
    for seq_record in SeqIO.parse(in_file, "fasta"):
        in_file_count += 1
        if len(seq_record.seq) >= min_length:
            degenerates_in_seq = sum(seq_record.seq.count(nuc) for nuc in "RYMKSWHBVDN")
            if not degenerates_in_seq >= num_degenerates:
                regex_str = "([ACGTURYSWKMBDHVN])\\1{%s,}" % (homopolymer_length - 1)
                if not any(re.finditer(regex_str, str(seq_record.seq))):
                    # Splitting the ID to extract and format taxonomic classification
                    name = seq_record.id.split(";")
                    # Truncate or expand the classification to fit a standard format
                    # and prefix with 'rdp+' for identification
                    # [Code similar to the example, adjusting the taxonomy levels]
                    seq_record.id = "rdp+" + ";".join(name)
                    seq_record.name = ""
                    seq_record.description = ""
                    SeqIO.write(seq_record, output_handle, "fasta")
                    out_file_count += 1

in_file.close()

# Reporting statistics for RDP sequence processing
print(f"in: {in_file_count} reads")
print(f"out: {out_file_count} reads")
print(f"filter: {in_file_count-out_file_count} reads")
```

### Silva Database Processing

The processing steps for Silva database sequences are akin to those for RDP and GTDB, with particular attention to Silva's unique sequence descriptions and the extraction of taxonomic information.

```python
from Bio import SeqIO
import re

# Input and output file paths for Silva sequences
in_file = open("./merged_database/SILVA_138.1_SSURef_NR99_tax_silva.fasta","r")
out_file = "./merged_database/filter_silva.fna"

# Repeating the quality control parameters and filtering process
# [Similar to the GTDB and RDP scripts, with specifics for handling Silva taxonomy]
num_degenerates = 5
homopolymer_length = 8
min_length = 1200
in_file_count = 0
out_file_count = 0

with open(out_file, "a") as output_handle:
    for seq_record in SeqIO.parse(in_file, "fasta"):
        in_file_count += 1
        if len(seq_record.seq) >= min_length:
            degenerates_in_seq = sum(seq_record.seq.count(nuc) for nuc in "RYMKSWHBVDN")
            if not degenerates_in_seq >= num_degenerates:
                regex_str = "([ACGTURYSWKMBDHVN])\\1{%s,}" % (homopolymer_length - 1)
                if not any(re.finditer(regex_str, str(seq_record.seq))):
                    # Processing for Silva taxonomy extraction and formatting
                    # [Code similar to the example, adjusting the taxonomy levels]
                    seq_record.id = "silva+" + ";".join(name)
                    seq_record.name = ""
                    seq_record.description = ""
                    SeqIO.write(seq_record, output_handle, "fasta")
                    out_file_count += 1

in_file.close()

# Report on the number of processed Silva sequences
print(f"in: {in_file_count} reads")
print(f"out: {out_file_count} reads")
print(f"filter: {in_file_count-out_file_count} reads")
```

## Merge Process

After filtering sequences from each database, they are merged into a comprehensive dataset for further analysis.

```bash
# Concatenate all filtered sequences from different databases into one file
cat filter_* > filter_all.fna
# Execute a bash script to further process the combined dataset
bash merge_database.sh
```

This final step combines the quality-controlled sequences from all databases, creating a unified resource for bioinformatics research and analysis.