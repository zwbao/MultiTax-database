import pandas as pd
import re
import pickle
from Bio import SeqIO

def load_pickled_data(file_path):
    with open(file_path, 'rb') as pickle_file:
        return pickle.load(pickle_file)

def process_annotations(H120_zotus_anno_dict, other_uc_dict_human_anno):
    human_anno = copy.deepcopy(other_uc_dict_human_anno)
    new_otus = {}

    # Process the annotations and update the human_anno dictionary
    for i in H120_zotus_anno_dict:
        added_number = 'Uniq' + str(len(human_anno) + 1)
        new_otus[added_number] = i

        for gtdb_anno in human_anno[H120_zotus_anno_dict[i].split('_')[0]]:
            if re.search(r'gtdb+', gtdb_anno, re.IGNORECASE):
                gtdb_anno_list = gtdb_anno.split(";")
                gtdb_added = H120_zotus_anno_dict[i].split("_")[2]

                if re.search(r'new', gtdb_anno, re.IGNORECASE):
                    if gtdb_added[0] == "p":
                        if len(gtdb_anno_list) >1:
                            gtdb_anno_list = gtdb_anno_list[:1]
                            if not re.search(r'new_phylum', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_phylum")
                        else:
                            gtdb_anno_list.append("new_phylum")

                    if gtdb_added[0] == "c":
                        if len(gtdb_anno_list) >2:
                            gtdb_anno_list = gtdb_anno_list[:2]
                            if not re.search(r'new_class', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_class")
                        else:
                            gtdb_anno_list.append("new_class")

                    if gtdb_added[0] == "o":
                        if len(gtdb_anno_list) >3:
                            gtdb_anno_list = gtdb_anno_list[:3]
                            if not re.search(r'new_order', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_order")
                        else:
                            gtdb_anno_list.append("new_order")

                    if gtdb_added[0] == "f":    
                        if len(gtdb_anno_list) >4:
                            gtdb_anno_list = gtdb_anno_list[:4]
                            if not re.search(r'new_family', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_family")
                        else:
                            gtdb_anno_list.append("new_family")

                    if gtdb_added[0] == "g":    
                        if len(gtdb_anno_list) >5:
                            gtdb_anno_list = gtdb_anno_list[:5]
                            if not re.search(r'new_genus', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_genus")
                        else:
                            gtdb_anno_list.append("new_genus")

                    if gtdb_added[0] == "s":    
                        if len(gtdb_anno_list) >6:
                            gtdb_anno_list = gtdb_anno_list[:6]
                            if not re.search(r'new_species', gtdb_anno, re.IGNORECASE):
                                gtdb_anno_list.append("new_species")
                        else:
                            gtdb_anno_list.append("new_species")

                    tmp = gtdb_anno_list
                else:
                    if gtdb_added[0] == "p":
                        tmp = [gtdb_anno_list[0], "new_phylum"]
                    elif gtdb_added[0] == "c":
                        tmp = [gtdb_anno_list[0], gtdb_anno_list[1], "new_class"]
                    elif gtdb_added[0] == "o":
                        tmp = [gtdb_anno_list[0], gtdb_anno_list[1], gtdb_anno_list[2], "new_order"]
                    elif gtdb_added[0] == "f":
                        tmp = [gtdb_anno_list[0], gtdb_anno_list[1], gtdb_anno_list[2], gtdb_anno_list[3], "new_family"]
                    elif gtdb_added[0] == "g":
                        tmp = [gtdb_anno_list[0], gtdb_anno_list[1], gtdb_anno_list[2], gtdb_anno_list[3], gtdb_anno_list[4], "new_genus"]
                    elif gtdb_added[0] == "s":
                        tmp = [gtdb_anno_list[0], gtdb_anno_list[1], gtdb_anno_list[2], gtdb_anno_list[3], gtdb_anno_list[4], gtdb_anno_list[5], "new_species"]


                gtdb_anno_result = ';'.join(tmp)
                
                if added_number not in human_anno:
                    human_anno[added_number] = [gtdb_anno_result]
                    human_anno[added_number].append("human_related+gut")
                else:
                    human_anno[added_number].append(gtdb_anno_result)

    return human_anno, new_otus

def save_dataframe_to_tsv(dataframe, output_file):
    dataframe.to_csv(output_file, sep='\t', index_label='index')

def merge_sequences_to_fasta(merged_db_file, human_zotu_file, new_otus, output_file):
    merged_db_records = list(SeqIO.parse(merged_db_file, "fasta"))
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
    with open(output_file, "w") as outfile:
        SeqIO.write(merged_db_records, outfile, "fasta")

    print("Merging completed. Results are saved in the file:", output_file)

if __name__ == "__main__":
    # Input file paths
    H120_zotus_anno_tsv = "H120_merged_human_all_anno_new_taxa.tsv"
    other_uc_dict_human_anno_pkl = "other_uc_dict_human_anno.pkl"
    merged_db_file = "merged_human_all.fasta"
    human_zotu_file = "H120_all_zotus.fa"

    # Output file paths
    human_anno_tsv = "human_anno.tsv"
    human_anno_pkl = "human_anno.pkl"
    output_file_merged = "merged_human_all_H120.fasta"

    # Load pickled data containing annotations
    other_uc_dict_human_anno = load_pickled_data(other_uc_dict_human_anno_pkl)

    # Read H120 zotus annotations from tsv file and process annotations
    H120_zotus_anno_df = pd.read_csv(H120_zotus_anno_tsv, sep='\t', header=0, index_col=0)
    H120_zotus_anno_dict = H120_zotus_anno_df.to_dict()['anno']
    human_anno, new_otus = process_annotations(H120_zotus_anno_dict, other_uc_dict_human_anno)

    # Convert the updated dictionary to a DataFrame and save to a TSV file
    human_anno_df = pd.DataFrame.from_dict(human_anno, orient='index')
    save_dataframe_to_tsv(human_anno_df, human_anno_tsv)

    # Save human_anno dictionary as a pickle file
    with open(human_anno_pkl, 'wb') as file:
        pickle.dump(human_anno, file)

    # Merge human deduplicated zotus into the integrated database and save to a new fasta file
    merge_sequences_to_fasta(merged_db_file, human_zotu_file, new_otus, output_file_merged)