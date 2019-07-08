# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 03:11:04 2019

@author: taha2
"""

from scipy.signal import butter, sosfilt, sosfilt_zi, sosfiltfilt, lfilter, lfilter_zi, filtfilt, sosfreqz, resample
from utils import hamilton_detector, christov_detector, findpeaks, engzee_detector
from ecg_detectors.ecgdetectors import Detectors, MWA, panPeakDetect, searchBack







class qrs_detection():
    def __init__(self):
        pass
    
    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype="band", output="sos")
        return sos


    def butter_bandpass_filter(self,data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos,
                    data)  # Filter data along one dimension using cascaded second-order sections. Using lfilter for each second-order section.
        return y
    
    
    def butter_bandpass_filter_once(self,data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        # Apply the filter to data. Use lfilter_zi to choose the initial condition of the filter.
        zi = sosfilt_zi(sos)
        z, _ = sosfilt(sos, data, zi=zi * data[0])
        return sos, z, zi
    
    
    def butter_bandpass_filter_again(self,sos, z, zi):
        # Apply the filter again, to have a result filtered at an order the same as filtfilt.
        z2, _ = sosfilt(sos, z, zi=zi * z[0])
        return z2
    
    
    def butter_bandpass_forward_backward_filter(self,data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfiltfilt(sos,
                        data)  # Apply a digital filter forward and backward to a signal.This function applies a linear digital filter twice, once forward and once backwards. The combined filter has zero phase and a filter order twice that of the original.
        return y
    
    def pan_tompkins_detector(self,raw_ecg, mwa, fs, N):
       
    #     N = int(0.12 * fs)
    #     mwa = MWA(squared, N)
    #     mwa[:int(0.2 * fs)] = 0
    
        N = int(N / 100 * fs)
        mwa_peaks = panPeakDetect(mwa, fs)
    
        r_peaks = searchBack(mwa_peaks, raw_ecg, N)
    
        return r_peaks
    
    
