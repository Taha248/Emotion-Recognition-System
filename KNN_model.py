# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split



class KNN_Model():
    def __init__(self):
        self.classifier = KNeighborsClassifier(n_neighbors=5)
        self.scaler = StandardScaler()
            
    
    def train_model(self):
         
         names = ['Pulse', 'GSR','Emotions']
         dataset = pd.read_csv("C:/Users/Zeeshan/dec.csv",names=names)
         print(dataset)
         X = dataset.iloc[:, :-1].values
         y = dataset.iloc[:, 2].values
        
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)
         
         self.scaler.fit(X_train)
    
         X_train = self.scaler.transform(X_train)
         X_test = self.scaler.transform(X_test)
        
         self.classifier.fit(X_train, y_train)
        
         test=self.scaler.transform(X_test)
         y_pred = self.classifier.predict(test)
         print(confusion_matrix(y_test, y_pred))
         print(classification_report(y_test, y_pred))
         
        
    def test_model(self,testSet):
         p=self.scaler.transform(testSet)
         k_pred = self.classifier.predict(p)
         return k_pred
    

x=KNN_Model();
x.train_model()   
print(x.test_model( [[8 ,300],[7.5,300 ], [3.6,100]]) )
print(x.test_model( [[3.2 ,100],[7.5,300 ], [9.6,200]]) )
     
             
        
        
        
