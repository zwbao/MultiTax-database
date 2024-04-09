import pandas as pd
blast_file = pd.read_csv("./humann_other_based_zotus.b6", sep='\t', header = None)

blast_file["anno"] = blast_file[1].str.split(pat=";",n=1, expand=True)[0]
blast_file.loc[(blast_file[2] >= 94.5) & (blast_file[2] < 98.7) ,"anno"] += "_new_species"
blast_file.loc[(blast_file[2] >= 86.5) & (blast_file[2] < 94.5) ,"anno"] += "_new_genus"
blast_file.loc[(blast_file[2] >= 82.0) & (blast_file[2] < 86.5) ,"anno"] += "_new_family"
blast_file.loc[(blast_file[2] >= 78.5) & (blast_file[2] < 82.0) ,"anno"] += "_new_order"
blast_file.loc[(blast_file[2] >= 75.0) & (blast_file[2] < 78.5) ,"anno"] += "_new_class"
blast_file.loc[(blast_file[2] < 75.0) ,"anno"] += "_new_phylum"

out_file = blast_file[[0,"anno"]]
out_file.columns = ["zotus","anno"]
out_file.to_csv("./human_related_zotus_anno.tsv",index=False,sep ='\t')
