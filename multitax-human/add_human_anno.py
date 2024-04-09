import pandas as pd
import re
import pickle
import csv
import copy

# Load the pickled data containing annotations
with open("./other_uc_dict_new.gtdb_anno.pkl", 'rb') as pickle_file:
    other_uc_dict_new = pickle.load(pickle_file)

# Dictionary for otu annotations to body sites:
human_related_zotus_type_dict = {}

# Read the TSV file and create the dictionary with human-related zotus types
with open("sampletype_list_df.tsv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    header = next(reader)  # Skip the header row
    for row in reader:
        key = row[0]
        value = row[2:] if len(row) > 2 else row[2]  # Get all values from the 3rd column onwards as a list
        filtered_value = [item for item in value if item != '']
        human_related_zotus_type_dict[key] = filtered_value

# Dictionary for otu annotations to the integrated database:
human_related_zotus_anno_df = pd.read_csv("human_related_zotus_anno.tsv", sep='\t', header=0, index_col=0)
human_related_zotus_anno_dict = human_related_zotus_anno_df.to_dict()['anno']

# Create a copy of the other_uc_dict_new dictionary
other_uc_dict_human_anno = copy.deepcopy(other_uc_dict_new)
new_otus = {}

# Process the annotations and update the other_uc_dict_human_anno dictionary
for i in human_related_zotus_anno_dict:
    if human_related_zotus_anno_dict[i] in other_uc_dict_human_anno:
        if len(human_related_zotus_type_dict[i]) >1:
            for human_loca in human_related_zotus_type_dict[i]:
                other_uc_dict_human_anno[human_related_zotus_anno_dict[i]].append("human_related+" + human_loca)
        else:
            other_uc_dict_human_anno[human_related_zotus_anno_dict[i]].append("human_related+" + human_related_zotus_type_dict[i][0])
    else:
        for gtdb_anno in other_uc_dict_human_anno[human_related_zotus_anno_dict[i].split('_')[0]]:
            if re.search(r'gtdb+', gtdb_anno, re.IGNORECASE):
                gtdb_anno_list = gtdb_anno.split(";")
                gtdb_added = human_related_zotus_anno_dict[i].split("_")[2]

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

                added_number = 'Uniq' + str(len(other_uc_dict_human_anno) + 1)
                new_otus[added_number] = i
                other_uc_dict_human_anno[added_number] = [gtdb_anno_result]
                
                if len(human_related_zotus_type_dict[i]) >1:
                    for human_loca in human_related_zotus_type_dict[i]:
                        other_uc_dict_human_anno[added_number].append("human_related+" + human_loca)
                else:
                    other_uc_dict_human_anno[added_number].append("human_related+" + human_related_zotus_type_dict[i][0])

# other_uc_dict_human_anno should be de-duplicated
for key in other_uc_dict_human_anno:
    # Convert the list value to a set to remove duplicates, then convert it back to a list
    other_uc_dict_human_anno[key] = list(set(other_uc_dict_human_anno[key]))
     
# Convert the updated dictionary to a DataFrame and save to a TSV file
other_uc_dict_human_anno_df = pd.DataFrame.from_dict(other_uc_dict_human_anno, orient='index')
other_uc_dict_human_anno_df.to_csv('other_uc_dict_human_anno.tsv', sep='\t', index_label='index')

with open('other_uc_dict_human_anno.pkl', 'wb') as file:
    pickle.dump(other_uc_dict_human_anno, file)