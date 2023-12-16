# -*- coding: utf-8 -*-
"""DL AAT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10wI6Ek4Vr3xxfy1w6VqZUhhjlQwCMu64
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('water_potability.csv')
df.head()

#Check for missing data.
df.isnull().sum()

df = df.dropna()
df.isnull().sum()

fig = px.scatter_3d(df,
                    x='Hardness',
                    y='Sulfate',
                    z='Chloramines',
                    color='Potability')
fig.show();

fig = px.scatter_3d(df,
                    x='ph',
                    y='Solids',
                    z='Conductivity',
                    color='Potability')
fig.show();

dataset = df.values
X = dataset[:,0:9]
y = dataset[:,9]

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)
X_scale

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True)
plt.xticks(rotation=45);

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_scale, y, test_size=0.3)
Y_train = Y_train.astype(np.float32)
Y_test = Y_test.astype(np.float32)

# Build neural network model with a sequential model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

model = Sequential([
Dense(32, activation='relu', input_shape=(9,)),
Dense(64, activation='relu'),
Dropout(0.5),
Dense(32, activation='relu'),
Dense(1, activation='sigmoid'),])

model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, Y_train, epochs=500,
                    validation_data=(X_test, Y_test), verbose=2)

# Plotting training accuracy and validation accuracy while comparing them
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], 'r', label='Accuracy Training')
plt.plot(history.history['val_accuracy'], 'b', label='Accuracy Validation')
plt.title('Accuracy Training dan Validation')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc=0)
plt.show()

# Plotting training loss and validation loss while comparing them
import matplotlib.pyplot as plt
plt.plot(history.history['loss'], 'r', label='Loss Training')
plt.plot(history.history['val_loss'], 'b', label='Loss Validation')
plt.title('Loss Training dan Validation')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc=0)
plt.show()

y_test = Y_test
y_train = Y_train
X_test_scaled = X_test
X_train_scaled =X_train

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score,f1_score,accuracy_score,roc_auc_score,recall_score,classification_report,confusion_matrix
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.model_selection import GridSearchCV

DT_model = DecisionTreeClassifier(random_state=42)
DT_model.fit(X_train, Y_train)
y_pred = DT_model.predict(X_test)
y_train_pred = DT_model.predict(X_train)



print(confusion_matrix(Y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(Y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")

param_grid = {"splitter":["best", "random"],
              "max_features":[None, 3, 5, 7],
              "max_depth": [None, 4, 5, 6, 7, 8, 9, 10],
              "min_samples_leaf": [2, 3, 5],
              "min_samples_split": [2, 3, 5, 7, 9, 15]}

DT_grid_model = DecisionTreeClassifier(class_weight = "balanced", random_state=42)

DT_grid_model = GridSearchCV(estimator=DT_grid_model,
                            param_grid=param_grid,
                            scoring='recall',
                            n_jobs = -1, verbose = 0).fit(X_train, Y_train)

from termcolor import colored
print(colored('\033[1mBest Parameters of GridSearchCV for DT Model:\033[0m', 'blue'), colored(DT_grid_model.best_params_, 'cyan'))
print("--------------------------------------------------------------------------------------------------------------------")
print(colored('\033[1mBest Estimator of GridSearchCV for DT Model:\033[0m', 'blue'), colored(DT_grid_model.best_estimator_, 'cyan'))

DT_grid_model.fit(X_train, Y_train)
y_pred = DT_grid_model.predict(X_test)

y_train_pred = DT_grid_model.predict(X_train)

dt_grid_f1 = f1_score(y_test, y_pred)
dt_grid_acc = accuracy_score(y_test, y_pred)
dt_grid_recall = recall_score(y_test, y_pred)
dt_grid_auc = roc_auc_score(y_test, y_pred)

print(confusion_matrix(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")



from sklearn.ensemble import RandomForestClassifier
RF1_model = RandomForestClassifier(random_state=42)
RF1_model.fit(X_train_scaled, y_train)
y_pred = RF1_model.predict(X_test_scaled)

y_train_pred = RF1_model.predict(X_train_scaled)

rf1_f1 = f1_score(y_test, y_pred)
rf1_acc = accuracy_score(y_test, y_pred)
rf1_recall = recall_score(y_test, y_pred)
rf1_auc = roc_auc_score(y_test, y_pred)

print(confusion_matrix(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")

param_grid = {'n_estimators':[50, 100, 300],
             'max_features':[2, 3, 4],
             'max_depth':[3, 5, 7, 9],
             'min_samples_split':[2, 5, 8]}

RF_grid_model = RandomForestClassifier(class_weight = "balanced", random_state=42)

RF_grid_model = GridSearchCV(estimator=RF_grid_model,
                             param_grid=param_grid,
                             scoring = "recall",
                             n_jobs = -1, verbose = 0).fit(X_train_scaled, y_train)

print(colored('\033[1mBest Parameters of GridSearchCV for RF Model:\033[0m', 'blue'), colored(RF_grid_model.best_params_, 'cyan'))
print("--------------------------------------------------------------------------------------------------------------------")
print(colored('\033[1mBest Estimator of GridSearchCV for RF Model:\033[0m', 'blue'), colored(RF_grid_model.best_estimator_, 'cyan'))

y_pred = RF_grid_model.predict(X_test_scaled)
y_train_pred = RF_grid_model.predict(X_train_scaled)

rf_grid_f1 = f1_score(y_test, y_pred)
rf_grid_acc = accuracy_score(y_test, y_pred)
rf_grid_recall = recall_score(y_test, y_pred)
rf_grid_auc = roc_auc_score(y_test, y_pred)

print(confusion_matrix(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")



from xgboost import XGBClassifier
XGB_model1 = XGBClassifier(random_state=42)
XGB_model1.fit(X_train, y_train)
y_pred = XGB_model1.predict(X_test)
y_train_pred = XGB_model1.predict(X_train)

xgb1_f1 = f1_score(y_test, y_pred)
xgb1_acc = accuracy_score(y_test, y_pred)
xgb1_recall = recall_score(y_test, y_pred)
xgb1_auc = roc_auc_score(y_test, y_pred)

print(confusion_matrix(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")

param_grid = {"n_estimators":[100, 300],
              "max_depth":[3,5,6],
              "learning_rate": [0.1, 0.3],
              "subsample":[0.5, 1],
              "colsample_bytree":[0.5, 1]}

XGB_grid_model = XGBClassifier(random_state=42)
XGB_grid_model = GridSearchCV(XGB_grid_model, param_grid, scoring = "f1", verbose=0, n_jobs = -1)
XGB_grid_model.fit(X_train_scaled, y_train)

print(colored('\033[1mBest Parameters of GridSearchCV for XGB Model:\033[0m', 'blue'), colored(XGB_grid_model.best_params_, 'cyan'))
print("--------------------------------------------------------------------------------------------------------------------")
print(colored('\033[1mBest Estimator of GridSearchCV for XGB Model:\033[0m', 'blue'), colored(XGB_grid_model.best_estimator_, 'cyan'))

y_pred = XGB_grid_model.predict(X_test_scaled)
y_train_pred = XGB_grid_model.predict(X_train_scaled)

xgb_grid_f1 = f1_score(y_test, y_pred)
xgb_grid_acc = accuracy_score(y_test, y_pred)
xgb_grid_recall = recall_score(y_test, y_pred)
xgb_grid_auc = roc_auc_score(y_test, y_pred)

print(confusion_matrix(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")
print(classification_report(y_test, y_pred))
print("\033[1m--------------------------------------------------------\033[0m")

print("Thank You")

