# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:02:20 2019

@author: Taha.Tauqir
"""
import pandas as pd 
import os
from Window_Statistical_Analysis import Window_Statistical_Analysis 

SAMPLE_ID="SAMPLE0002"
FILE_PATH="sample.csv";
WINDOW_OUTPUT_PATH="output";
STATS_OUTPUT_PATH="output";

OVERLAPPING = 0.5
WINDOW_SIZE= 1

class WindowSlidingClassification():
    # Assuming the data have same time difference
    def getSegmentedWindows(self,data,size,overlapping):
        start,end,startingValues,endingValues,result=0,0,[],[],[]
        
        if size<=overlapping:
            print('Window size must be greater than overlapping!')
            return
        
        for index, row in data.iterrows():
            #Setting Initial Starting & Ending Values
            
            if index==0:
                start=row[0]
                end = row[0]+size
            
            if row[0]==start+(size) :
                startingValues.append(start)
                start=start+(size-overlapping)
                
            if row[0]==end:
                endingValues.append(end)
                end=end+(size-overlapping)
            
            isLastIndex=(index==(len(data)-1))
            isNotEqualToEnd=(row[0]!= end-(size-overlapping))
            isNotEqualToStart= row[0]!=start+(size)
            
            if isLastIndex and isNotEqualToStart and isNotEqualToEnd :
                startingValues.append(start)
                endingValues.append(end)
        
        # Applying Filter on Dataframe
        for start,end in zip(startingValues,endingValues):
            result.append(data[((data.Time>=start) & (data.Time <= end))])
        
        #print(result)
        return result
    
    def dataFrameToCSV(self,df,path):
        os.makedirs(str(path)+'/'+SAMPLE_ID+'/Windows/', exist_ok=True)
        for index,data in enumerate(df):
            data.to_csv(str(path)+'/'+SAMPLE_ID+'/Windows/window-'+str((index+1))+'.csv',index=False)
        
    
#if __name__=='__main__':
#    
#    df=pd.read_csv(FILE_PATH)
#    window_sliding = WindowSlidingClassification()
#    
#    result = window_sliding.getSegmentedWindows(df,WINDOW_SIZE,OVERLAPPING)
#    window_sliding.dataFrameToCSV(result,WINDOW_OUTPUT_PATH)
#    col=['Mean(T) ','AAV(T)','AAD(T)','Variance(T)','Energy(T)','MCR(T)','RMS(T)','Skewness(T)','Kurtosis(T)','ZCR(T)','Mean(G) ','AAV(G)','AAD(G)','Variance(G)','Energy(G)','MCR(G)','RMS(G)','Skewness(G)','Kurtosis(G)','ZCR(G)','Mean(B) ','AAV(B)','AAD(B)','Variance(B)','Energy(B)','MCR(B)','RMS(B)','Skewness(B)','Kurtosis(B)','ZCR(B)']
#
#    x = Window_Statistical_Analysis()
#    arr = os.listdir(STATS_OUTPUT_PATH+'/'+SAMPLE_ID+'/Windows/')
#    data=[]
#    indexes=[]
#    
#    for index,filename in enumerate(arr):
#        df=pd.read_csv(WINDOW_OUTPUT_PATH+'\\'+SAMPLE_ID+'\\Windows\\'+filename)
#        data.append(x.getCalculatedAttributes(df))
#        indexes.append('Window '+str(index+1))
#        
#    dataframe= pd.DataFrame(data,columns=col,index=indexes)
#    dataframe.to_csv(str(STATS_OUTPUT_PATH)+'/'+SAMPLE_ID+'/statistical_analysis.csv',index=True)
#        
#    