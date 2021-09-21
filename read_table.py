import pandas as pd
import pdb

df = pd.read_csv('fuzzy_table.csv',index_col="e")
columns = df.columns
indices = df.index
# for c in columns:
#     for i in indices:
#         df[c][i]


pdb.set_trace()
