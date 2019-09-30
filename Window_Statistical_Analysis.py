# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:02:09 2019

@author: Taha.Tauqir
"""
from statistical_analysis import statistical_analysis 
import pandas as pd
import os
INPUT_PATH = "C:\\Users\\taha.tauqir\\Desktop\\output\\"
SAMPLE_ID = "SAMPLE0001"
class Window_Statistical_Analysis():
    def __init__(self):
        pass
    
    
    def getCalculatedAttributes(self,df):
        temperatureAttributes,GsrAttributes, BpmAttributes = [],[],[]
        Temperature=df['Temperature'].values
        GSR=df['GSR'].values
        BPM=df['BPM'].values
        stats = statistical_analysis()
        
        temperatureAttributes.append(stats.getMean(Temperature))
        temperatureAttributes.append(stats.getAAV(Temperature))
        temperatureAttributes.append(stats.getAAD(Temperature))
        temperatureAttributes.append(stats.getVariance(Temperature))
        temperatureAttributes.append(stats.getEnergy(Temperature))
        temperatureAttributes.append(stats.getMeanCrossingRate(Temperature))
        temperatureAttributes.append(stats.getRootMeanSquare(Temperature))
        temperatureAttributes.append(stats.getSkewness(Temperature))
        temperatureAttributes.append(stats.getKurtosis(Temperature))
        temperatureAttributes.append(stats.getZeroCrossingRate(Temperature))
        
        GsrAttributes.append(stats.getMean(GSR))
        GsrAttributes.append(stats.getAAV(GSR))
        GsrAttributes.append(stats.getAAD(GSR))
        GsrAttributes.append(stats.getVariance(GSR))
        GsrAttributes.append(stats.getEnergy(GSR))
        GsrAttributes.append(stats.getMeanCrossingRate(GSR))
        GsrAttributes.append(stats.getRootMeanSquare(GSR))
        GsrAttributes.append(stats.getSkewness(GSR))
        GsrAttributes.append(stats.getKurtosis(GSR))
        GsrAttributes.append(stats.getZeroCrossingRate(GSR))
        
        BpmAttributes.append(stats.getMean(BPM))
        BpmAttributes.append(stats.getAAV(BPM))
        BpmAttributes.append(stats.getAAD(BPM))
        BpmAttributes.append(stats.getVariance(BPM))
        BpmAttributes.append(stats.getEnergy(BPM))
        BpmAttributes.append(stats.getMeanCrossingRate(BPM))
        BpmAttributes.append(stats.getRootMeanSquare(BPM))
        BpmAttributes.append(stats.getSkewness(BPM))
        BpmAttributes.append(stats.getKurtosis(BPM))
        BpmAttributes.append(stats.getZeroCrossingRate(Temperature))
        
        return temperatureAttributes+GsrAttributes+BpmAttributes
        
        
        
        

    

