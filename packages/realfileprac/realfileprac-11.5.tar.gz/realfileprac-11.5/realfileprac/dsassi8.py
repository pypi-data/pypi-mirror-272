def practicle8():
    print('''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("Titanic-Dataset.csv")

data

data.shape

data.describe()

data.describe(include = 'object')

data.isnull().sum()

"""# Removing Null values"""

data['Age'] = data['Age'].fillna(np.mean(data['Age']))

data['Cabin'] = data['Cabin'].fillna(data['Cabin'].mode()[0])

data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])

data.isnull().sum()

"""# Part 1

# Explore the dataset using Seaborn to find patterns
"""

sns.boxplot(data['Age'])

sns.boxplot(data['Fare'])

sns.boxplot(data['Pclass'])

sns.boxplot(data['SibSp'])

sns.catplot(x= 'Pclass', y = 'Age', data=data, kind = 'box')

sns.catplot(x= 'Pclass', y = 'Fare', data=data, kind = 'strip')

sns.catplot(x= 'Sex', y = 'Fare', data=data, kind = 'strip')

sns.catplot(x= 'Sex', y = 'Age', data=data, kind = 'strip')

"""# Creating a pairplot to visualize relationships between different variables"""

sns.pairplot(data)

sns.scatterplot(x = 'Fare', y = 'Pclass', hue = 'Survived', data = data)

sns.scatterplot(x = 'Survived', y = 'Fare', data = data)

sns.distplot(data['Age'])

sns.distplot(data['Fare'])

sns.jointplot(x = "Survived", y = "Fare", kind = "scatter", data = data)

"""# Part 2

# Ploting a histogram to visualize the distribution of ticket prices
"""

plt.figure(figsize=(10, 6))
sns.histplot(data['Fare'], bins=30, kde=True, color='blue')
plt.title('Distribution of Ticket Prices')
plt.xlabel('Fare')
plt.ylabel('Frequency')
plt.show()

''')
practicle8()