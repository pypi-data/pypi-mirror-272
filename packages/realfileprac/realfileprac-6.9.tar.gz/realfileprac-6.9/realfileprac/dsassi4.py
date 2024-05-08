def practical4():
    print('''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv")

df.head(3)

df.info()
df.shape

df.isnull().sum()

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.displot(df['medv'], bins=30)
plt.show()

correlation_matrix = df.corr().round(2)
sns.heatmap(data=correlation_matrix, annot=True)

X = df[['lstat', 'rm']]
Y = df[['medv']]
X.head(10)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

xtrain,xtest,ytrain,ytest = train_test_split(X, Y, test_size=0.2, random_state=42)
print(xtrain.shape,xtest.shape,ytrain.shape,ytest.shape)

linear_model = LinearRegression()
linear_model.fit(xtrain, ytrain)

ypredict = linear_model.predict(xtest)

r2_score(ytest,ypredict)

mean_squared_error(ytest,ypredict)''')

practical4()