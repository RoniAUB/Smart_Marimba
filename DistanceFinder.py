# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:29:08 2024

@author: Administrator
"""

import numpy as np
import scipy as sp
import math

class DistanceFinder:
    
    #initialize the class with the constant variables
    def __init__(self, speed_of_sound=4500, distance_between_sensors=0.5, average_sampling_rate=30000):
        self.speed_of_sound = speed_of_sound
        self.distance_between_sensors = distance_between_sensors
        self.average_sampling_rate = average_sampling_rate
        
    #All obtained distances are rescaled to a scale of 1 to 7 that represents our musical notes,
    #This can be modified or removed, but for now I am adding/subtracting octaves to the pitch based on this
        
    #This function uses the cross correlation in the Fourrier domain to estimate the distance
    def distance_finder_corrFFT(self, queue_sensor1, queue_sensor2):
        correlation = sp.signal.correlate(queue_sensor1, queue_sensor2, mode='full')
        max_index = np.argmax(correlation)
        delay = max_index / self.average_sampling_rate
        distance = delay * self.speed_of_sound + self.distance_between_sensors / 2
        return int((distance / self.distance_between_sensors) * 7)

    #This function uses the cross correlation to estimate the distance
    def distance_finder_corrNP(self, queue_sensor1, queue_sensor2):
        correlation = np.correlate(queue_sensor1, queue_sensor2, mode='full')
        max_index = np.argmax(correlation)
        delay = max_index / self.average_sampling_rate
        distance = delay * self.speed_of_sound + self.distance_between_sensors / 2
        return int((distance / self.distance_between_sensors) * 7)
    
    #This function uses the ratio of the maximum peaks to estimate the distance
    def distance_finder_ratio(self, queue_sensor1, queue_sensor2):
        # I still have an error here, the distance is proportional to the ratio, where is beta?
        max1 = np.max(queue_sensor1)
        max2 = np.max(queue_sensor2)
        ratio = max1 / max2
        distance = self.speed_of_sound * math.log(ratio) + self.distance_between_sensors / 2
        return  int((distance / self.distance_between_sensors) * 7)

    #This function uses a convolution to smoothen the signal then a threshold to estimate the distance
    def distance_finder_threshold(self,queue_sensor1,queue_sensor2,threshold,window_size):
        #When a hit is detected, the flags get switched and no recordings are done within the defined window size
        
        flag_11=0
        flag_12=1
        flag_21=0
        flag_22=1
        #Here we smoothen the readings by applying a moving convolution over both sensors
        weights = np.ones(window_size) / window_size 
        moving_avg1 = np.convolve(queue_sensor1, weights, mode='valid')
        moving_avg2 = np.convolve(queue_sensor2, weights, mode='valid')
        
        Amp1=np.max(moving_avg1)
        Amp2=np.max(moving_avg2)
        
        for i in range(len(moving_avg1)):
            if (moving_avg1[i] >threshold )and (flag_11==0):
                #The first time a curve crosses the threshold, we consider the impact reachd the sensor
                #We use this to estimate the time between receiving each hit and use it to find the distance
                d11=i
                flag_11=1
                flag_12=0
            elif (moving_avg1[i] >threshold)and (flag_12==0):
                #We consider that the hit waves has passed when the curve crosses
                #the threshold for the first time, then goes back to the threshold
                #we use this to estimate the width of the curve
                d12=i
                flag_12=1
        for i in range(len(moving_avg1)):
            if (moving_avg2[i] >threshold )and (flag_21==0):
                d21=i
                flag_21=1
                flag_22=0
            elif (moving_avg2[i] >threshold) and (flag_22==0):
                d22=i
                flag_12=1
        distance=((d11-d21)*self.average_sampling_rate)*self.speed_of_sound
        width=(d22-d12)*self.average_sampling_rate
        Amplitude=max(Amp1,Amp2)
        return int((distance / self.distance_between_sensors) * 7)
    
    #This function implements Linear regression to predict the distance
    def distance_finder_ML(self,queue_sensor1,queue_sensor2):
        pass


