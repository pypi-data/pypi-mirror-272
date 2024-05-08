def practical9():
    print('''
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""# Part 1

# Loading dataset
"""

data = pd.read_csv("Titanic-Dataset.csv")

data.head()

data.describe()

data.info()

data.isnull().sum()

"""# Removing null values"""

data['Age'] = data['Age'].fillna(np.mean(data['Age']))
data['Cabin'] = data['Cabin'].fillna(data['Cabin'].mode()[0])
data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])

data.isnull().sum()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Sex', y='Age', hue='Survived', data=data)
plt.title('Distribution of Age by Gender and Survival Status')
plt.xlabel('Gender')
plt.ylabel('Age')
plt.legend(title='Survived', loc='upper right', labels=['No', 'Yes'])
plt.show()

"""# As for the observations:

###    Age Distribution: From the box plot, we can observe the distribution of ages for both males and females. It appears that the median age for males is slightly higher than for females.

###    Survival by Gender: Within each gender, we can observe differences in the distribution of ages between those who survived and those who did not. This could indicate potential differences in the demographics of survivors within each gender group.

###    Outliers: The box plot also highlights any outliers in the age distribution within each gender and survival category, which might indicate unusual cases or data errors.
"""

''')
practical8()