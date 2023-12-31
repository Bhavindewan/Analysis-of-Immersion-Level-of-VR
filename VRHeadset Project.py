# -*- coding: utf-8 -*-
"""Project 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iOkF8vvQBa7cfy7nuGRwBr_1zQETSjh_
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

vr_df=pd.read_csv('/content/data.csv')

vr_df.head()

vr_df.info()

vr_df.isna().sum()

#check correlation
vr_df.corr()

sns.heatmap(vr_df.corr(),annot=True,cmap='Blues')

#names of columns
vr_df.columns

#coutning values
g=vr_df['Gender'].value_counts()
print(g)

#gender distribution
plt.figure(figsize=(10,9))
g.plot(kind='bar',alpha=0.5)
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Gender Distribution')
plt.show()

#coutning vales of VR headset
vr=vr_df['VRHeadset'].value_counts()
vr

#VRHeadet distribution
plt.figure(figsize=(10,9))
vr.plot(kind='bar',alpha=0.5)
plt.xlabel('VRHeadset')
plt.ylabel('Count')
plt.title('VRHeadset Distribution')
plt.show()

#Dist Plot
sns.distplot(x=vr_df['Duration'])
plt.title('Distribution of duration in minutes')
plt.xlabel('Duration in minutes')
plt.grid()
plt.show()

#Dist Plot motion sickness
sns.distplot(x=vr_df['MotionSickness'])
plt.title('Motion Sickness Distribution')
plt.xlabel('Sound in db')
plt.grid()
plt.show()

#Biverate Analysis
fig=px.box(x=vr_df['Age'],y=vr_df['Duration'])
fig.update_layout(title='Age vs Duration', xaxis_title='Age',yaxis_title='Duration in minutes')
fig.show()

fig=px.box(x=vr_df['Age'],y=vr_df['Duration'],color=vr_df['Gender'])
fig.update_layout(title='Age vs Duration', xaxis_title='Age',yaxis_title='Duration in minutes')
fig.show()

fig=px.box(x=vr_df['VRHeadset'],y=vr_df['Duration'],color=vr_df['Gender'])
fig.update_layout(title='VRHeadset vs Duration', xaxis_title='Age',yaxis_title='Duration in minutes')
fig.show()

fig=px.scatter(x=vr_df['Age'],y=vr_df['Duration'],size=vr_df['MotionSickness'])
fig.update_layout(title='Age vs Duration', xaxis_title='Age',yaxis_title='Duration in minutes')
fig.show()

fig=px.box(x=vr_df['MotionSickness'],y=vr_df['Duration'],color=vr_df['VRHeadset'])
fig.update_layout(title='MotionSickness vs Duration', xaxis_title='Age',yaxis_title='Duration in minutes')
fig.show()

#Model Building
df_1=vr_df.copy()
df_1
df_1.info()

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, RepeatedStratifiedKFold, StratifiedGroupKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, confusion_matrix, classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from scipy.stats import loguniform

#Pre-processing
le = LabelEncoder()

#le.fit(df['Gender'])

df_1['Gender'] = le.fit_transform(df_1['Gender'])
print("""Label Encoder for Gender category

Female - 0
Male - 1
Other- 2 """)

df_1['VRHeadset'] = le.fit_transform(vr_df['VRHeadset'])
print("""Label encoder for VR Headset Category

HTC Vive - 0
Oculus Rift - 1
PlayStation VR - 2""")

df_1['ImmersionLevel'] = le.fit_transform(df_1['ImmersionLevel'])
df_1['ImmersionLevel'].value_counts()

x=df_1.drop('ImmersionLevel',axis=1)
y=df_1['ImmersionLevel']

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=42)
print(xtrain.shape)
print(ytrain.shape)
print(xtest.shape)
print(ytest.shape)

#MAE=mean absolute error
#Accuracy score
#Confusion matrix
#Classification report
def model_evaluation(y_pred,ytest=ytest):
  print('*'*70)
  print('mean absolute error: ',mean_absolute_error(y_pred,ytest))
  print('*'*70)
  print('accuracy_score: ',accuracy_score(y_pred,ytest))
  print('*'*70)
  print('Confusion matrix: ',confusion_matrix(y_pred,ytest))
  print('*'*70)
  print('Classification report: ',classification_report(y_pred,ytest))

dtc=DecisionTreeClassifier(max_depth=10,max_features=5,min_samples_leaf=4,min_samples_split=5)

dtc.fit(xtrain,ytrain)

dtc_pred=dtc.predict(xtest)
model_evaluation(dtc_pred)

xgb = XGBClassifier(learning_rate=0.002, n_estimators=500, nthread=3)

xgb.fit(xtrain,ytrain)
xgb_pred = xgb.predict(xtest)

model_evaluation(xgb_pred)