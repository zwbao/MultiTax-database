from Bio import SeqIO

merged_db_file = "merge_uniques.relabel.fasta"
human_zotu_file = "merge_zotus_uniques.relabel.fasta"

# Read the integrated database file
merged_db_records = list(SeqIO.parse(merged_db_file, "fasta"))
# Read the human deduplicated zotus
human_zotu_file_records = list(SeqIO.parse(human_zotu_file, "fasta"))

# Merge the human deduplicated zotus into the integrated database
for i in new_otus:
    for record in human_zotu_file_records:
        if record.name == new_otus[i]:
            record.id = i
            record.name = ""
            record.description = ""
            merged_db_records.append(record)

# Write the merged sequences to a new fasta file
output_file = "merged_human_all.fasta"
with open(output_file, "w") as outfile:
    SeqIO.write(merged_db_records, outfile, "fasta")

print("Merging completed. Results are saved in the file:", output_file)