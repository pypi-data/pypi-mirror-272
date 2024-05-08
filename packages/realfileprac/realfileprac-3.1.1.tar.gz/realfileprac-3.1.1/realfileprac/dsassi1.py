def practical1():
  print('''
import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/imports-85.csv')

df.head(5)

df.replace('?', np.NaN, inplace=True)
df.head(5)

df.shape

df.info()

df.describe()

df.isnull().sum()

df['normalized-losses'] = pd.to_numeric(df['normalized-losses'], errors='coerce')
df['normalized-losses'].fillna(df['normalized-losses'].mean(), inplace=True)

df.head(5)

column_to_fill = ['bore', 'stroke','peak-rpm','horsepower']
for col in column_to_fill:
  df[col] = pd.to_numeric(df[col], errors='coerce')
  df[col].replace(np.NaN, df[col].mean(), inplace=True)

df.isnull().sum()

df['num-of-doors'].value_counts()

df['num-of-doors'].value_counts().idxmax()
df['num-of-doors'].replace(np.NaN, 'four', inplace=True)

df.dropna(subset=['price'],axis=0,inplace=True)
df['price']=pd.to_numeric(df['price'], errors='coerce')
df.isnull().sum()

df['city-mpg'] = pd.to_numeric(df['city-mpg'],errors='coerce')
df['highway-mpg'] =pd.to_numeric(df['highway-mpg'],errors='coerce')

df['city-mpg'] = 235/df['city-mpg'].astype('float')
df['highway-mpg'] = 235/df['highway-mpg'].astype('float')
df.rename(columns={'highway-mpg':'highway-L/100km', 'city-mpg': 'city-L/100km'},inplace=True)
df.head(5)

cols = ['length','width','height']
for i in cols:
  df[i]=pd.to_numeric(df[i],errors='coerce')

df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df['height'] = df['height']/df['height'].max()

df[['length','width','height']].head()

df['num-of-doors'] = df['num-of-doors'].replace({'two':2, 'four':4})
df['aspiration'] = df['aspiration'].replace({'std':0 ,'turbo':1})

df[['num-of-doors','aspiration']].head(10)

df.head(5)

''')
practical1()