def practical5():
    print('''
    import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://raw.githubusercontent.com/shivang98/Social-Network-ads-Boost/master/Social_Network_Ads.csv')
df.head(3)

df['Gender'].replace({'male':0,'female':1}, inplace=True)

x = df[['User ID', 'Gender', 'Age', 'EstimatedSalary']]
y = df['Purchased']

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.25,random_state=29)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(xtrain,ytrain)
ypred = model.predict(xtest)
ypred

from tabulate import tabulate


ftable = pd.DataFrame(np.column_stack((ytest,ypred)), columns=["Actual Purchased", "Predicted Purchased"])
table = tabulate(ftable.head(10), headers="keys", tablefmt="fancy_grid", showindex=False)
print(table)

cm = confusion_matrix(ytest, ypred, labels = model.classes_)
cm

tp,fn,fp,tn = confusion_matrix(ytest,ypred,labels=[1,0]).reshape(-1)
print(f"tn {tn}")
print(f"fp {fp}")
print(f"fn {fn}")
print(f"tp {tp}")

from sklearn.metrics import ConfusionMatrixDisplay

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.show()

from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score


a=accuracy_score(ytest,ypred)
e=1-a
recall = recall_score(ytest,ypred)
p = precision_score(ytest,ypred)

print(f"accuracy {a}")
print(f"error {e}")
print(f"recall score {recall}")
print(f"Precision score {p}")

print(confusion_matrix.__doc__)

''')
practical5()