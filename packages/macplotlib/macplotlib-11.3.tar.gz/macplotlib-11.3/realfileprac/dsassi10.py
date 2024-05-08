def practical10():
    print('''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

iris_data = pd.read_csv("IRIS.csv")

"""# Display the first few rows of the dataset to understand its structure"""

print(iris_data.head())

"""# List down features and their types"""

print(iris_data.info())

"""# Create histograms for each feature"""

plt.figure(figsize=(12, 8))
for i, feature in enumerate(iris_data.columns[:-1]):
    plt.subplot(2, 2, i + 1)
    sns.histplot(iris_data[feature], kde=True)
    plt.title(f'Histogram of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

"""# Create boxplots for each feature"""

plt.figure(figsize=(12, 8))
for i, feature in enumerate(iris_data.columns[:-1]):
    plt.subplot(2, 2, i + 1)
    sns.boxplot(y=iris_data[feature])
    plt.title(f'Boxplot of {feature}')
    plt.ylabel(feature)
plt.tight_layout()
plt.show()

"""# Compare distributions visually using histograms and boxplots

# Calculate and display outliers using the Interquartile Range (IQR) method
"""

outliers = {}
for feature in iris_data.columns[:-1]:
    Q1 = iris_data[feature].quantile(0.25)
    Q3 = iris_data[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    feature_outliers = iris_data[(iris_data[feature] < lower_bound) | (iris_data[feature] > upper_bound)][feature]
    outliers[feature] = feature_outliers

"""# Display outliers"""

print("Outliers:")
for feature, values in outliers.items():
    if not values.empty:
        print(f"Feature: {feature}, Outliers: {values.values}")

''')
practical10()