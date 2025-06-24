import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os


df_original = pd.read_csv("titanic.csv")  
df = df_original.copy()  


print("\n🔹 First few rows:")
print(df.head())


print("\n🔹 Original data shape:", df.shape)


df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df.drop('Cabin', axis=1, inplace=True)


df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)


scaler = StandardScaler()
df[['Age', 'Fare']] = scaler.fit_transform(df[['Age', 'Fare']])

sns.boxplot(x=df['Fare'])
plt.title("Fare Outliers (Before Removal)")
plt.show()


Q1 = df['Fare'].quantile(0.25)
Q3 = df['Fare'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['Fare'] < (Q1 - 1.5 * IQR)) | (df['Fare'] > (Q3 + 1.5 * IQR)))]

print("\n🔹 Data shape after outlier removal:", df.shape)

print("\n🔹 Final column names:")
print(df.columns)

sns.boxplot(x=df['Fare'])
plt.title("Fare After Outlier Removal")
plt.show()



df.to_csv("titanic_cleaned.csv", index=False)
print("\n✅ Data preprocessing complete. File saved as 'titanic_cleaned.csv'.")


try:
    os.startfile("titanic_cleaned.csv")
    print("📂 Opening 'titanic_cleaned.csv' in Excel...")
except:
    print("⚠ Could not open file automatically. Please open manually.")
