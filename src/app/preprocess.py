import pandas as pd

df = pd.read_excel("C:\\Users\\msi\\Desktop\\DB_dropped_duplicates.xlsx", encoding='utf-8')


# df.sort_values('pcode')

# print(df[['pcode','cid']])
df = df.drop_duplicates(subset = ['pcode','cid'], keep='first')

print(df[['pcode','cid']])
df.to_excel("DB_dropped_duplicates.xlsx", encoding='utf-8')
