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
import copy

class statistical_analysis():
    def __init__(self) : 
        pass
    
    def getMean(self,arr):
        if((sum(arr) / len(arr))== 0  or (sum(arr) / len(arr))== "" ):
            return 0
        return sum(arr) / len(arr) 
    
    def getVariance(self,arr):
        mean = sum(arr) / len(arr) 
        variance=0.0
        for i in range(len(arr)):
            variance+=(arr[i]-mean)**2
            
            if((variance/len(arr)== 0)  or variance/len(arr)== "" ):
                return 0
            
        return variance/len(arr)
    
    def getEnergy(self,arr):
        array=copy.deepcopy(arr)
        for x in range(len(arr)):
            array[x]  = arr[x]*arr[x]
            if((sum(array) / len(array) == 0)  or sum(array) / len(array) == "" ):
                 return 0
        return sum(array) / len(array) 
    
    def getAAV(self,arr):
        s = 0
        for x in arr:
            s+=abs(x)
        
        if((s/(len(arr)-1) == 0)  or s/(len(arr)-1) == "" ):
            return 0
        return s/(len(arr)-1)
    
    def getAAD(self,arr):
        s=0
        for i in range(1,len(arr)):
           s+=abs(arr[i-1]-arr[i])
           
        if(s==0 ):
            return 0
        return s/(len(arr)-1)
    
    
    def getSkewness(self,arr):
        x,y=0.0,0.0
        mean = sum(arr) / len(arr) 
        for i in range(len(arr)):
            x=x+((arr[i]-mean)**3)
        x=x/len(arr)
        for i in range(len(arr)):
            y=y+((arr[i]-mean)**2)
        y=y/len(arr)
        y=(math.sqrt(y))**3
        
        if(x == 0  and y == 0):
            return 0       
        
        return x/y
        
    
    
    def getKurtosis(self,arr):
        x,y=0.0,0.0
        
        mean = sum(arr) / len(arr) 
        for i in range(len(arr)):
            val=(arr[i]-mean)**4
            x=x+(val)
        x=x/len(arr)
        
        for i in range(len(arr)):
            val = (arr[i]-mean)**2
            y=y+(val)
        y=y/len(arr)
        y=y**2
        
        if(x == 0  and y == 0):
            return 0     
        
        return x/y
    
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
        if(float(total)) == 0  or float(total) == "":
            return 0     
            
        return float(total)
    
    def getMeanCrossingRate(self,arr):
        total=0
        for i in range(len(arr)):
            if(i==0):
                continue
            total+=abs(self.sign((arr[i]-self.getMean(arr))-self.sign(arr[i-1]-self.getMean(arr))))
        if(float(total)) == 0  or float(total) == "":
            return 0            
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
        if(float("{0:.4f}".format(root))) == 0  or float("{0:.4f}".format(root)) == "":
            return 0           
        return float("{0:.4f}".format(root))
    
    