# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 02:57:59 2019

@author: taha2
"""

import numpy as np
import statistics 
import pyhrv.tools as tools
from biosppy import utils

class time_domain():
    def __init__(self):
        pass
    
    def timeDomain(self,NN):
        L = len(NN)    
        ANN = np.mean(NN)
        SDNN = np.std(NN)
        SDSD = np.std(np.diff(NN))    
        NN50 = len(np.where(np.diff(NN) > 0.05)[0])    
        pNN50 = NN50/L    
        NN20 = len(np.where(np.diff(NN) > 0.02)[0])
        pNN20 = NN20/L
        rMSSD = np.sqrt((1/L) * sum(np.diff(NN) ** 2))        
        MedianNN = np.median(NN)
        SDANN = self.sdann(NN)['sdann']
        SDNN_INDEX=self.sdnn_index(NN)['sdnn_index']
        RRI_MEAN=self.RRI_Mean(NN)['rri_mean']
        
        timeDomainFeats = {
            "ANN": ANN, "SDNN": SDNN,
            "SDSD": SDSD, "NN50": NN50,
                           "SDANN":SDANN , 
                            "SDNN_INDEX": SDNN_INDEX,
                           "RRI_Mean": RRI_MEAN,
                           "pNN50": pNN50, "NN20": NN20,
                           "pNN20": pNN20, "rMSSD": rMSSD,
                           "MedianNN":MedianNN}
                           
        return timeDomainFeats
    
    
    def sdnn_index(self,nni=None, rpeaks=None, full=True, overlap=False, duration=300):
    
        # Check input
        nn = tools.check_input(nni, rpeaks)
    
        # Signal segmentation into 5 min segments
        segments, seg = tools.segmentation(nn,  full=full, overlap=overlap, duration=duration)
    
        if seg:
            sdnn_values = [sdnn(x)['sdnn'] for x in segments]
            sdnn_index = np.mean(sdnn_values)
        else:
            sdnn_index = float('nan')
            if tools.WARN:
                warnings.warn("Signal duration too short for SDNN index computation.")
    
        # Output
        args = [sdnn_index]
        names = ['sdnn_index']
        return utils.ReturnTuple(args, names)
    
    
    def sdann(self,nni=None, rpeaks=None, full=True, overlap=False, duration=300):
    
        # Check input
        nn = tools.check_input(nni, rpeaks)
    
        # Signal segmentation into 5 min segments
        segments, seg = tools.segmentation(nn, full=full, overlap=overlap, duration=duration)
    
        if seg:
            mean_values = [np.mean(x) for x in segments]
            sdann_ = tools.std(mean_values)
        else:
            sdann_ = float('nan')
            if tools.WARN:
                warnings.warn("Signal duration too short for SDANN computation.")
    
        # Output
        args = [sdann_]
        names = ['sdann']
        return utils.ReturnTuple(args, names)
    
    
    def RRI_Mean(self,nni=None, rpeaks=None, full=True, overlap=False, duration=300):
    
        # Check input
        nn = tools.check_input(nni, rpeaks)
        
        # Signal segmentation into 5 min segments
        segments, seg = tools.segmentation(nn, full=full, overlap=overlap, duration=duration)
        if seg:
            rri_mean_ = statistics.mean([np.mean(x) for x in segments])
    
        else:
            rri_mean_ = float('nan')
            if tools.WARN:
                warnings.warn("Signal duration too short for RRI Mean computation.")
    
        # Output
        args = [rri_mean_]
        names = ['rri_mean']
        return utils.ReturnTuple(args, names)