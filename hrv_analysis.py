# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 02:31:40 2019

@author: taha2
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import warnings
import pandas as pd
from scipy.signal import butter, sosfilt, sosfilt_zi, sosfiltfilt, lfilter, lfilter_zi, filtfilt, sosfreqz, resample
from utils import hamilton_detector, christov_detector, findpeaks, engzee_detector
from ecg_detectors.ecgdetectors import Detectors, MWA, panPeakDetect, searchBack
import os
import csv
from numpy import genfromtxt
import pyhrv.tools as tools
from biosppy import utils
import statistics 
import json
from time_domain import time_domain
from qrs_detection import qrs_detection
from frequency_domain import frequency_domain



SAMPLE_FILE='sample1-default'
#SAMPLE_FILE='sample2-external'
SAMPLE_FILE_RESULT="samples/"+SAMPLE_FILE+"-result.json"

# Sample rate and desired cutoff frequencies (in Hz).
FS = 200  # corresponds to 60 beats per min (normal for human), assumed.
LOWCUT = 0.05 * 3.3  # 9.9 beats per min
HIGHCUT = 15  # 900 beats per min



def loadData():
    temp=pd.read_csv("samples/"+str(SAMPLE_FILE)+".csv")
    
    data=np.empty([len(temp)])
    for x in range(len(temp)):
        data[x]=temp.values[x][0]
    return data

def writeJSONFile(result):
    f = open(SAMPLE_FILE_RESULT, "w")
    f.write(result)
    f.close()

def getRRInterval(data):
    
    x=data
    
    for order in [1, 2, 4, 6, 8]:
        sos = qrs_detection.butter_bandpass(LOWCUT, HIGHCUT, FS, order=order)
        w, h = sosfreqz(sos, worN=2000)    
    
    # Calculate time values in seconds
    #times = np.arange(x.shape[0], dtype='float') / fs
    y = qrs_detection.butter_bandpass_forward_backward_filter(x, LOWCUT, HIGHCUT, FS, order=4)
    
    # Derivative - provides QRS slope information.
    differentiated_ecg_measurements = np.ediff1d(y)
    
    # Squaring - intensifies values received in derivative. 
    # This helps restrict false positives caused by T waves with higher than usual spectral energies..
    squared_ecg_measurements = differentiated_ecg_measurements ** 2
    
    # Moving-window integration.
    integration_window = 50  # Change proportionally when adjusting frequency (in samples)
    integrated_ecg_measurements = np.convolve(squared_ecg_measurements, np.ones(integration_window))
    
    # Fiducial mark - peak detection on integrated measurements.
    rpeaks = qrs_detection.pan_tompkins_detector(data, integrated_ecg_measurements, FS, integration_window)
    
    
    # RR Interval
    rr = np.diff(rpeaks) / FS * 1000  # in miliseconds
    #hr = 60 * 1000 / rr
    return rr
    
    

if __name__ == "__main__":
    x=loadData()
    qrs_detection= qrs_detection()
    RR_Interval=getRRInterval(x)

    
    # Time Domain Analysis
    time_domain = time_domain()
    time_domain_result = time_domain.timeDomain(RR_Interval)
    
    
    
    frequency_domain = frequency_domain()
    frequency_domain_result = frequency_domain.frequency_domain(nni=RR_Interval)
    
    
    LF_HF=float((float(frequency_domain_result['fft_peak'][1]))
          /(float(frequency_domain_result['fft_peak'][2])))
    
    Json_Result=str((str(time_domain_result).replace("'",'"')).replace('nan','"nan"')).split('}')[0]+','+'"VLF" : '+str(frequency_domain_result['fft_peak'][0])+','+'"LF" : '+str(frequency_domain_result['fft_peak'][1])+','+'"HF" : '+str(frequency_domain_result['fft_peak'][2])+','+'"LF/HF" : '+str(LF_HF)+'}'
                         
    
    
    print(Json_Result)
    #Write Data in JSON File
    writeJSONFile((str(Json_Result).replace("'",'"')).replace('nan','"nan"'))
    

    

        
    
    