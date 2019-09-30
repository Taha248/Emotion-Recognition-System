# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:02:20 2019

@author: Taha.Tauqir
"""
import pandas as pd 
import os

SAMPLE_ID="SAMPLE0001"
FILE_PATH="C:/Users/taha.tauqir/Desktop/test2.csv";
OUTPUT_PATH="C:/Users/taha.tauqir/Desktop/output";
OVERLAPPING = 2
WINDOW_SIZE= 3

# Assuming the data have same time difference
def getSegmentedWindows(data,size,overlapping):
    start,end,startingValues,endingValues,result=0,0,[],[],[]
    
    if size<=overlapping:
        print('Window size must be greater than overlapping!')
        return
    
    for index, row in df.iterrows():
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
        
        isLastIndex=(index==(len(df)-1))
        isNotEqualToEnd=(row[0]!= end-(size-overlapping))
        isNotEqualToStart= row[0]!=start+(size)
        
        if isLastIndex and isNotEqualToStart and isNotEqualToEnd :
            startingValues.append(start)
            endingValues.append(end)
    
    # Applying Filter on Dataframe
    for start,end in zip(startingValues,endingValues):
        result.append(data[((data.Time>=start) & (data.Time <= end))])

    return result

def dataFrameToCSV(df,path):
    os.makedirs(str(path)+'/'+SAMPLE_ID, exist_ok=True)
    for index,data in enumerate(df):
        data.to_csv(str(path)+'/'+SAMPLE_ID+'/window-'+str((index+1))+'.csv',index=False)
    

if __name__=='__main__':
    df=pd.read_csv(FILE_PATH)
    result = getSegmentedWindows(df,WINDOW_SIZE,OVERLAPPING)
    print(result[0])
    print(result[1])
    dataFrameToCSV(result,OUTPUT_PATH)
    
    