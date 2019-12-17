from flask import Flask,request,jsonify,Response
from flask_restful import Resource,Api
from PIL import Image,ImageFile
import cv2
import numpy
import tensorflow as tf
import json
import sys
import base64
import pandas as pd 
import os
import shutil  

from Window_Statistical_Analysis import Window_Statistical_Analysis 
from WindowSlidingClassification_main import WindowSlidingClassification
from KNN_model import KNN_Model

SAMPLE_ID="SAMPLE0002"
FILE_PATH="input.csv";
WINDOW_OUTPUT_PATH="output";
STATS_OUTPUT_PATH="output";

OVERLAPPING = 0.5
WINDOW_SIZE= 1

app = Flask(__name__)
api = Api(app)


flags =  tf.app.flags
flags.DEFINE_string('MODE', 'demo', 
                    'Set program to run in different mode, include train, valid and demo.')
flags.DEFINE_string('checkpoint_dir', './ckpt', 
                    'Path to model file.')
flags.DEFINE_string('train_data', './data/fer2013/fer2013.csv',
                    'Path to training data.')
flags.DEFINE_string('valid_data', './valid_sets/',
                    'Path to training data.')
flags.DEFINE_boolean('show_box', False, 
                    'If true, the results will show detection box')
FLAGS = flags.FLAGS

SAMPLE_IMAGE_PATH=""

class Emotion_Recognition(Resource):
    def __init__(self):
        self.temp = 0
        self.hr = 0
        self.gsr = 0
        self.model = KNN_Model()
        
    def get(self):
        if not os.path.exists("input1.json") or not os.path.exists("input2.json") :
            return '{Error:"Input Files are not present"}'
            
        
        with open('input1.json') as json_file1:
            data1 = json.load(json_file1)
        with open('input2.json') as json_file2:
            data2 = json.load(json_file2)
            
        data= self.mergetwoJSONS(data1,data2)
        print(data)
        csv = self.convertJSONtoCSV(data)
        self.saveCSV(csv)
        self.executeSampleAnalysis()
        rs = self.makeOneFile()
        result = str('{result : "'+str(self.model.test_model(rs)[0])+'", Temperature : '+str(self.temp)+', BPM : '+str(self.hr)+', GSR : '+str(self.gsr)+'}')
        self.storeResult(result)
        return result
        
       
    
    def storeResult(self,data):
        f = open("result.json", "w")
        f.write(str(data))
        f.close()
        
        
    def makeOneFile(self):
        df = pd.read_csv("output\SAMPLE0002\statistical_analysis.csv")
        stat = "Mean(T) ,AAV(T),AAD(T),Variance(T),Energy(T),MCR(T),RMS(T),Skewness(T),Kurtosis(T),ZCR(T),Mean(G) ,AAV(G),AAD(G),Variance(G),Energy(G),MCR(G),RMS(G),Skewness(G),Kurtosis(G),ZCR(G),Mean(B) ,AAV(B),AAD(B),Variance(B),Energy(B),MCR(B),RMS(B),Skewness(B),Kurtosis(B),ZCR(B)\n"
        
        l,l1 = [],[]
        i=0
        mean = df.mean()
        for x in mean:
            if(i==0):
                self.temp = x
            if(i==10):
                self.gsr=x
            if(i==20):
                self.hr = x 
            
            i=i+1
            if(i<len(mean)):
                l.append(x)
        
        return [l]
        
    
    def post(self):
        inputJSON = request.get_json()
        self.saveCSV(self.convertJSONtoCSV(inputJSON))
        
        return request.get_json()
    
    def convertJSONtoCSV(self,data):
        jsonData = json.loads(data)
       # print(jsonData)
        outputString = "Time,GSR,BPM,Temperature\n"
        for key, value in jsonData.items():
            #print(key,value)
            outputString+=(str(value))
            if("Temp" in str(key)):
                #print(outputString)
                outputString+="\n"
            else:
                outputString+=","
        
     #   print(outputString)
        return outputString
    
    def saveCSV(self,data):
        f = open("input.csv", "w")
        f.write(data)
        f.close()
    def executeSampleAnalysis(self):
        df=pd.read_csv(FILE_PATH)
      #  print(str(df)+"------------")
        window_sliding = WindowSlidingClassification()
        result = window_sliding.getSegmentedWindows(df,WINDOW_SIZE,OVERLAPPING)
        
        window_sliding.dataFrameToCSV(result,WINDOW_OUTPUT_PATH)
        col=['Mean(T) ','AAV(T)','AAD(T)','Variance(T)','Energy(T)','MCR(T)','RMS(T)','Skewness(T)','Kurtosis(T)','ZCR(T)','Mean(G) ','AAV(G)','AAD(G)','Variance(G)','Energy(G)','MCR(G)','RMS(G)','Skewness(G)','Kurtosis(G)','ZCR(G)','Mean(B) ','AAV(B)','AAD(B)','Variance(B)','Energy(B)','MCR(B)','RMS(B)','Skewness(B)','Kurtosis(B)','ZCR(B)']
    
        x = Window_Statistical_Analysis()
        arr = os.listdir(STATS_OUTPUT_PATH+'/'+SAMPLE_ID+'/Windows/')
        data=[]
        indexes=[]
        
        for index,filename in enumerate(arr):
            df=pd.read_csv(WINDOW_OUTPUT_PATH+'\\'+SAMPLE_ID+'\\Windows\\'+filename)
            data.append(x.getCalculatedAttributes(df))
            indexes.append('Window '+str(index+1))
            
        dataframe= pd.DataFrame(data,columns=col,index=indexes)
        dataframe.to_csv(str(STATS_OUTPUT_PATH)+'/'+SAMPLE_ID+'/statistical_analysis.csv',index=True)
       
        
        
    def mergetwoJSONS(self,json1,json2):
        result="";
        result+="{"
        for (k,v), (k2,v2) in zip(json1.items(), json2.items()):
            result+="\""+str(k)+"\":\""+str(v)+"\","
            result+="\""+str(k2)+"\":\""+str(v2)+"\","
            #print(k,v,k2,v2)
        
        result = result[:-1:]
        result+="}"  
        return result
            


class Get_Result(Resource):        
    def get(self):
        f = open("result.json", "r")
        for x in f:
            rs=x
        return rs
    

        

class ClearResult(Resource):        
    def get(self):
        try:
            if os.path.exists("result.json"):
              os.remove("result.json")
            if os.path.exists("input.json"):
              os.remove("input.csv")
            if os.path.exists("input1.json"):
              os.remove("input1.json")
            if os.path.exists("input2.json"):
              os.remove("input2.json")
            if os.path.exists("statistical_analysis.csv"):
              os.remove("statistical_analysis.csv")
            if os.path.exists("output/SAMPLE0002/Windows/"):
              shutil.rmtree('output/SAMPLE0002/Windows/')
        except:
            return '{ Something Went Wrong while removing Files}'
        return '{Message : "Successfully Deleted All Files"}'
        
        
class Save_GSR(Resource):
    def post(self):
        f = open("input1.json", "w")
        f.write(str(request.get_json()).replace("\'","\""))
        f.close()
    
class Save_BPM(Resource):
    def post(self):
        print(str(request.get_json()).replace("\'","\""))
        f = open("input2.json", "w")
        f.write(str(request.get_json()).replace("\'","\""))
        f.close()

#-d data="Create"
class Response_Data(Resource):
    def get(self):
        if os.path.exists("result.json"):
            f = open("response.txt", "r")
        else :
            return '{Error : "Response File Not Present"}'
        return f.readline()
    def post(self):
        if os.path.exists("response.txt"):
            os.remove("response.txt")
            
            
        data =request.form['data']
        f = open("response.txt", "w")
        f.write(str(data))
        f.close()

class Multi(Resource):
    def get(self,num):
        return {'result':num*10}


# Saving GSR INPUT (Requires JSON Stirng)
api.add_resource(Save_GSR,'/Save_GSR/')

# Saving BPM & TEMP INPUT (Requires JSON Stirng)
api.add_resource(Save_BPM,'/Save_BPM/')

# Emotion Recognition 
api.add_resource(Emotion_Recognition,'/Emotion/')

# Get Result
api.add_resource(Get_Result,'/Get_Result/')

# Clearing all Previous Data
api.add_resource(ClearResult,'/Clear_Result/')

# Providing Action for Arduino 
api.add_resource(Response_Data,'/Response/')

# Testing API
api.add_resource(Multi,'/multi/<int:num>')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


