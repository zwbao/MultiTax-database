import sys
import subprocess
import pandas as pd

def run_usearch(usearch_path, input_file, database_file, output_file):
    # Run usearch command
    bash_command = f"{usearch_path} -usearch_global {input_file} -db {database_file} -maxaccepts 0 -maxrejects 0 -strand both -top_hit_only -id 0 -blast6out {output_file} -threads 75"
    subprocess.run(bash_command, shell=True, check=True)

def annotate_zotus(input_file, output_file, output_file_new_taxa):
    blast_file = pd.read_csv(input_file, sep='\t', header=None)
    blast_file["anno"] = blast_file[1].str.split(pat=";", n=1, expand=True)[0]

    blast_file.loc[(blast_file[2] >= 94.5) & (blast_file[2] < 98.7), "anno"] += "_new_species"
    blast_file.loc[(blast_file[2] >= 86.5) & (blast_file[2] < 94.5), "anno"] += "_new_genus"
    blast_file.loc[(blast_file[2] >= 82.0) & (blast_file[2] < 86.5), "anno"] += "_new_family"
    blast_file.loc[(blast_file[2] >= 78.5) & (blast_file[2] < 82.0), "anno"] += "_new_order"
    blast_file.loc[(blast_file[2] >= 75.0) & (blast_file[2] < 78.5), "anno"] += "_new_class"
    blast_file.loc[blast_file[2] < 75.0, "anno"] += "_new_phylum"

    out_file = blast_file[[0, "anno"]]
    out_file.columns = ["zotus", "anno"]
    out_file.to_csv(output_file, index=False, sep='\t')

    # Create zotus_anno_new_taxa.tsv containing only rows with "new" in the "anno" column
    out_file_new_taxa = out_file[out_file["anno"].str.contains("new", case=False)]
    out_file_new_taxa.to_csv(output_file_new_taxa, index=False, sep='\t')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python ref_anno.py input_file database_file output_file output_file_new_taxa")
        sys.exit(1)

    input_file = sys.argv[1]
    database_file = sys.argv[2]
    output_file = sys.argv[3]
    output_file_new_taxa = sys.argv[4]

    usearch_path = "usearch11.0.667_i86linux64"  # Modify this to the actual usearch path if needed

    run_usearch(usearch_path, input_file, database_file, "ref_based_zotus.b6")
    annotate_zotus("ref_based_zotus.b6", output_file, output_file_new_taxa)

    print(f"Annotation complete. The results are saved in {output_file} and {output_file_new_taxa}.")

