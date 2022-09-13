# -*- coding: utf-8 -*-
"""Momento_Retroalimentacion_M2_framework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ye7JpshhXhysts2Gf8qjkmPBpqzy-i21
"""

import pandas as pd 
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("BankChurners.csv").drop_duplicates()#lee y elimina los duplicados del dataset

#dropeamos las columnas que no sirven especificadas en kaggle
data = df.drop("Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",axis = 1)
df = data.drop("Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",axis = 1)

df.info()#analizamos la tipologia de los datos

df.head()

df.shape

"""##Categorizacion de los valores cualitativos"""

#importamos de sklearn preprocessing
from sklearn import preprocessing
# se carga una la funcion que labelEncoder
label_encoder = preprocessing.LabelEncoder()
#La funcion LabelEncoder nos permite pasar los valores unicos a valores numericos y categorizar dichas variables

df['Attrition_Flag'] = label_encoder.fit_transform(df['Attrition_Flag'])
df['Gender'] = label_encoder.fit_transform(df['Gender'])
df['Education_Level'] = label_encoder.fit_transform(df['Education_Level'])
df['Marital_Status'] = label_encoder.fit_transform(df['Marital_Status'])
df['Card_Category'] = label_encoder.fit_transform(df['Card_Category'])

#En caso de la variable Income_Category

df["Income_Category"].unique() #analizamos los valores unicos

df["Income_Category"] = df["Income_Category"].map({'$60K - $80K': "C",'Less than $40K' : "A",'$80K - $120K': "D",
                                                   '$40K - $60K':"B", '$120K +': "E",'Unknown': "N" }) # SUSTITUYO el rango con un valor mas legible

df["Income_Category"].unique() #checamos que se hizo el cambio,este proceso hace entendible el cambio a numerico

df['Income_Category'] = label_encoder.fit_transform(df['Income_Category']) #se categoriza a numerico

"""##Analisis de los valores NULL O NA

"""

df.isnull().sum() #suma de los valores nulos

df.shape

df.isna().sum() #suma de los valores NA

"""Nos damos cuenta de que no hay valores faltantes por lo que no es necesario utilizar fillna para sustituir los valores por la media y la moda de manera respesctiva."""

#un ejemplo claro de como se rellenaria con media y moda seria el siguiente:
# mode_Card_Cat = df["Card_Category"].mode()[0]
#df["Card_Category"].fillna(mode_Card_Cat,inplace = True) #cambiar por moda

#Avg_Months_on_book  = df["Months_on_book"].mean()            
#df["Months_on_book"].fillna(Avg_Months_on_book,inplace = True) #cambiar por media

"""##Distribuciones"""

#Histogramas de las variables
fig = plt.figure(figsize=(25,25))
ax = fig.gca()
df.hist(ax=ax, bins=30, grid = True,)

"""##Separacion de los datos en train y test"""

x = df.drop(["Attrition_Flag"],axis = 1) # se dropea la variable objetivo para tener todo menos la columna target
y = df["Attrition_Flag"] # seleccionar el target que es la calificacion de posible abandono del banco

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size = 0.30, random_state = 45) # se hace un split de los datos de train y test 70% train 30% test

"""##Estandarizar de los datos"""

#estandarizacion min-max#
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

"""##Modelado"""

plt.figure(figsize=(45, 35))
sns.heatmap(df.corr(), annot=True)
#Generamos un mapa de calor que es lo mismo que nuestra MATRIZ DE CORRELACION

"""##Arbol de decisiones

"""

from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score

clf = DecisionTreeClassifier(criterion = "entropy", random_state = 40, splitter = "best")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_pred

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm # genera la matriz de confusion que nos dice el numero de elementos clasificados de manera correcta e incorrecta

ac = accuracy_score(y_test,y_pred)
ac # se calcula la excatitud para saber que tan bueno es el modelo

from sklearn.metrics import precision_score
from sklearn.metrics import roc_auc_score, roc_curve

PR = precision_score(y_test,y_pred)
PR # se calcula la precision para saber que tan cerca estan los valores de su valor real

ROC = roc_auc_score(y_test,y_pred)
ROC # se genera el coeficiente roc para conocer la sensibilidad de nuestro modelo

from sklearn import tree

fig = plt.figure(figsize = (360,340))
tree.plot_tree(clf,filled = True)
plt.show() # generamos una grafica de nuestro modelo en la cual se pueden apreciar las reglas de dicho modelo