import pandas as pd

uc_file = pd.read_csv("./merge_uniques.relabel.uc", sep='\t', header = None)

uc_list = {}
uniq_list = {}

for i in range(0, len(uc_file)):
    label = "Uniq" + str(int(uc_file.iloc[i,1]) + 1)
    query = uc_file.iloc[i,8].strip().split("+")[0]
    target = uc_file.iloc[i,9].strip().split("+")[0]
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

uc_df = pd.DataFrame([uc_list]).T
uc_df.columns = ['query']
uc_df['label'] = uc_df.index
uc_df['query_length'] = uc_df['query'].str.len()
tmp_df = pd.DataFrame(uc_df["query"].tolist())
uc_df = uc_df[['label', 'query_length']]
tmp_list = ["query"+str(i) for i in range(len(tmp_df.columns))]
tmp_list[0] = "target"
tmp_df.columns = tmp_list
tmp_df["label"] = list(uc_df["label"])
#uc_df2 = pd.concat([uc_df, tmp_df], axis=1)
uc_df2 = pd.merge(uc_df, tmp_df, on="label")
uc_df2.to_csv("./uc_list.tsv",index=False,sep ='\t')