# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 04:31:35 2019

@author: taha2
"""
import statistics 
import pandas as pd  
from scipy.stats import skew 
from scipy.stats import kurtosis
import numpy as np
import math

class statistical_analysis():
    def __init__(self) : 
        pass
    
    def getMean(self,arr):
        return sum(arr) / len(arr) 
    
    def getVariance(self,arr):
        return statistics.variance(arr)
    
    def getEnergy(self,arr):
        array = []
        for x in range(len(arr)):
            array[x]  = arr[x]*arr[x]
        return statistics.variance(array)
    
    def getAvgAbs(self,arr):
        return pd.Series(arr).mad()
    
    def getSkew(self,arr):
        return skew(arr)
    
    def getKurt(self,arr):
        return kurtosis(arr)
    
    def getRMS(self,arr):
        return
    
    def sign(self,val):
        if(val<0):
            return 0
        else:
            return 1
    
    def getZeroCrossingRate(self,arr):
        total=0
        for i in range(len(arr)):
            if(i==0):
                continue
            total+=abs(self.sign(arr[i])-self.sign(arr[i-1]))
        return float(total)
    
    def getMeanCrossingRate(self,arr):
        total=0
        for i in range(len(arr)):
            if(i==0):
                continue
            total+=abs(self.sign((arr[i]-self.getMean(arr))-self.sign(arr[i-1]-self.getMean(arr))))
        return float(total)
    
    
    def getRootMeanSquare(self,arr): 
        square = 0
        mean = 0.0
        root = 0.0
          
        #Calculate square 
        for i in range(0,len(arr)): 
            square += (arr[i]**2) 
          
        #Calculate Mean  
        mean = (square / (float)(len(arr))) 
          
        #Calculate Root 
        root = math.sqrt(mean) 
      
        return float("{0:.4f}".format(root))
    
    
    
# =============================================================================
#     def getZeroCrossingRate(self,arr):
#         my_array = np.array(arr)
#         return float("{0:.2f}".format((((my_array[:-1] * my_array[1:]) < 0).sum())/len(arr)))
#     
#     def getMeanCrossingRate(self,arr):
#         return self.getZeroCrossingRate(np.array(arr) - np.mean(arr))
#     
# ==========================================================================