def practical3():
    print('''

import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/Mohshaikh23/Dynamic-Pricing-Strategy/main/dynamic_pricing.csv')

df.head(3)

df.info()

df2 = df.groupby(['Customer_Loyalty_Status', 'Location_Category','Time_of_Booking'])['Average_Ratings'].describe()
df2

df2 = df.groupby(['Customer_Loyalty_Status', 'Location_Category'])['Average_Ratings'].mean()
df2

df2 = df.groupby(['Customer_Loyalty_Status', 'Location_Category'])['Average_Ratings'].median()
df2

df = pd.read_csv('https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')

df.info()

df.head(3)

df['variety'].value_counts()

sepalLengthStats = df.groupby(['variety'])['sepal.length'].describe()[['mean','max','min','50%','75%']]
sepalLengthStats

sepal = df['sepal.length']
p = [25,50,75]
sepalper = np.percentile(sepal,p)
print(f"sepal percentile {p}:{sepalper}")

''')
practical3()