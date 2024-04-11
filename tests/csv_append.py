import pandas as pd

dfs = []

for file in ['P2777.csv', 'P2776.csv']:
    dfs.append(pd.read_csv(file))

df = pd.concat(dfs)
df.to_csv('merged.csv', index=False)
