import pandas as pd
import re
df = pd.read_csv('TMU.csv')

df.fillna(-1, inplace=True)
df.drop(['Unnamed: 0.4'], axis=1, inplace=True)
df.to_csv('TMU.csv', index='CHR_NO')