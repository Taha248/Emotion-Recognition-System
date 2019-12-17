# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split



class KNN_Model():
    def __init__(self):
        self.classifier = KNeighborsClassifier(n_neighbors=1)
        self.scaler = StandardScaler()
        self.train_model()
            
    
    def train_model(self):
         
         names = ['','Mean(T)' ,'AAV(T)','AAD(T)','Variance(T)','Energy(T)','MCR(T)','RMS(T)','Skewness(T)','Kurtosis(T)','ZCR(T)','Mean(G)' ,'AAV(G)','AAD(G)','Variance(G)','Energy(G)','MCR(G)','RMS(G)','Skewness(G)','Kurtosis(G)','ZCR(G)','Mean(B)' ,'AAV(B)','AAD(B)','Variance(B)','Energy(B)','MCR(B)','RMS(B)','Skewness(B)','Kurtosis(B)','ZCR(B)']
       
        # Create the list for the three DataFrames you want to create:
         dataset = []
       #  for filename in filenames:
       #     dataset.append(pd.read_csv(filename,names=names))
         
         dataset = pd.read_csv("train\statistical_analysis1.csv",names=names)
       #  dataset.append(pd.read_csv("train\statistical_analysis2.csv"))
         print(dataset)
         
         del dataset['']
        # print(dataset[1:])
         X = dataset.iloc[1:, :-1].values
         y = dataset.iloc[1:, 29].values
     #    print(X)
         
        
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
    


#x=KNN_Model()
#z = [[32.916666666666664, 49.375, 0.125, 0.05555555555555556, 1083.5833333333333, 0.25, 32.917525, -0.17677669529663315, 0.37499999999999645, 0.0, 218.16666666666666, 327.25, 20.75, 1530.888888888889, 49701.666666666664, 0.5, 222.30545, -0.17677669529663684, 0.3749999999999998, 0.0, 270.0833333333333, 405.125, 83.625, 6418.277777777778, 82091.91666666666, 0.75, 283.80129999999997, -0.24401822970073495, 0.75]]
#print(len(z[0]))
#z = [[32.9,4.3,0.125,0.05555555555555556,1083.5833333333333,0.25,32.917525,-0.17677669529663315,0.37499999999999645,0.0,218.16666666666666,327.25,20.75,1530.888888888889,49701.666666666664,0.5,222.30545,-0.17677669529663684,0.3749999999999998,0.0,270.0833333333333,405.125,83.625,6418.277777777778,82091.91666666666,0.75,283.80129999999997,-0.24401822970073495,0.75]]
#print(len(z[0]))

#print(x.test_model(z))     
             
        
        
        
