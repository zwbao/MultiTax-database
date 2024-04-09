import pandas as pd

uc_file = pd.read_csv("./merge_zotus_uniques.relabel.uc", sep='\t', header = None)
uc_list = {}
uniq_list = {}

for i in range(0, len(uc_file)):
    label = "Uniq" + str(int(uc_file.iloc[i,1]) + 1)
    query = uc_file.iloc[i,8].strip()
    target = uc_file.iloc[i,9].strip()
    cat = str(uc_file.iloc[i,0])

    if cat == "H":
        if label not in uc_list:
            uc_list[label] = []
            uc_list[label].append(target)
            uc_list[label].append(query)
        else:
            if query not in uc_list[label]:
                uc_list[label].append(query)
    if cat == "S":
        if label not in uniq_list:
            uc_list[label] = []
            uc_list[label].append(query)

for i in uniq_list:
    if i not in uc_list:
        uc_list[uc_list[label]] = uc_list[label]

sampletype_list = {}

for i in uc_list:
    sampletype = []
    for item in uc_list[i]:
        parts = item.split('_')
        sampletype.append(parts[2])
        sampletype.sort()
    sampletype = list(set(sampletype))
    sampletype_list[i] = sampletype
   
sampletype_list_df = pd.DataFrame([sampletype_list]).T
sampletype_list_df.columns = ['query']
sampletype_list_df['label'] = sampletype_list_df.index
sampletype_list_df['query_length'] = sampletype_list_df['query'].str.len()
tmp_df = pd.DataFrame(sampletype_list_df["query"].tolist())
sampletype_list_df = sampletype_list_df[['label', 'query_length']]
tmp_list = ["query"+str(i) for i in range(len(tmp_df.columns))]
tmp_list[0] = "target"
tmp_df.columns = tmp_list
tmp_df["label"] = list(sampletype_list_df["label"])
sampletype_list_df2 = pd.merge(sampletype_list_df, tmp_df, on="label")
sampletype_list_df2.to_csv("./sampletype_list_df.tsv",index=False,sep ='\t') 
