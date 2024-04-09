import os
from Bio import SeqIO

# Path to the annotation TSV file
tsv_file = "run_anno.txt"
# Get the current working directory
current_directory = os.getcwd()

# Open and read the TSV file
with open(tsv_file, 'r') as f:
    lines = f.readlines()

# Skip the header and iterate over each line
for line in lines[1:]:
    # Split each line into columns
    columns = line.strip().split('\t')
    # Construct the file name for the input fasta file
    file_name = columns[0] + "_zotus.fa"
    # Create the full path to the input fasta file
    file_path = os.path.join(current_directory, file_name)
    # Check if the file exists and is not empty
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        # Create the output file name
        out_file = columns[0] + "_zotus_relabel.fa"
        # Open the output file in append mode
        with open(out_file, "a") as output_handle:
            # Open the input fasta file
            with open(file_path, 'r') as fa_file:
                # Parse the fasta file
                for record in SeqIO.parse(fa_file, 'fasta'):
                    # Add sampletype, run information to the sequence ID
                    # This enhances traceability by embedding metadata directly into the sequence ID
                    record.id = record.id + "_" + columns[0] + "_" + columns[1] + "_" + columns[2]
                    # Clear the sequence name and description to maintain focus on the modified ID
                    record.name = ""
                    record.description = ""
                    # Write the modified record to the output file
                    SeqIO.write(record, output_handle, "fasta")
