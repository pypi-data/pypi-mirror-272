def practical2():
    print('''

import pandas as pd
import numpy as np

df=pd.read_csv("academic.csv",na_values="?")
df

df

df.isnull().sum()

#no need to do because it has no null values ,but practice
df=df.dropna(subset=["Relation","GradeID"]) #this deletes the rows which has null values

df.isnull().sum()

df.describe()

import matplotlib.pyplot as plt
df["SectionID"].value_counts()

fig,x=plt.subplots(figsize=(6,4))
ax=plt.hist(df["SectionID"],color="b",edgecolor="b")
plt.title("Bar plot")
plt.show()

df = df[df["SectionID"].str.contains("C")==False]
df
#outliers removed "C" from SectionID

df["SectionID"].value_counts()

df.drop(["ParentAnsweringSurvey"],axis=1,inplace=True)

df

df["raisedhands"]=df["raisedhands"]/df["raisedhands"].max()
df["VisITedResources"]=df["VisITedResources"]/df["VisITedResources"].max()

df[["raisedhands","VisITedResources"]].head(10)

df["GradeID"].value_counts()

df.GradeID.replace({"G-02":1,"G-08":2,"G-07":3,"G-04":4,"G-06":5,"G-11":6,"G-12":7,"G-09":8,"G-10":9,"G-05":10},inplace=True)
df["GradeID"].value_counts()

min_val=df["Discussion"].min()
max_val=df["Discussion"].max()
print(min_val)
print(max_val)

bins=np.linspace(min_val,max_val,4)    #evenly spaced
bins

''')
practical2()