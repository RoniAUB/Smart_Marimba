# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:25:53 2024

@author: Administrator
"""

import serial
import struct
import time
import numpy as np
import matplotlib.pyplot as plt

class ArduinoReader:
    
    # This function initializes the Serial port to COM3, and a baudrate of 115200 by default
    def __init__(self, baudrate=115200, port="COM3"):
        self.ser = serial.Serial(port, baudrate)
        time.sleep(5)  # Wait for the serial connection to initialize

    # This function reads a single value from each sensor
    def read_sensor(self):
        data1 = self.ser.read(2)  # Read 2 bytes for sensorValue1
        sensorValue1 = struct.unpack('H', data1)[0]  # Unpack as unsigned short (2 bytes)
        data2 = self.ser.read(2)  # Read 2 bytes for sensorValue2
        sensorValue2 = struct.unpack('H', data2)[0]  # Unpack as unsigned short (2 bytes)
        return sensorValue1, sensorValue2
    
    # This function reads a queue of sensor values
    def read_sensor_queue(self, queue_size):
        queue1 = np.zeros(queue_size)
        queue2 = np.zeros(queue_size)
        for i in range(queue_size):
            queue1[i],queue2[i]=self.read_sensor()
        return queue1, queue2

    #This function estimates the sampling rate for a specified sample number
    def estimate_sampling_rate(self, sample_number):
        t1 = time.time()
        for i in range(sample_number):
            _, _ = self.read_sensor()
        t2 = time.time()
        return sample_number / (t2 - t1)

    # This function closes the Serial communication
    def close(self):
        self.ser.close()

# Main function to execute when the script is run directly
def main():
    # Initialize the Arduino reader
    arduino_reader = ArduinoReader(baudrate=115200, port="COM3") 

    # Read 1000 values from the sensors
    queue_size = 1000
    queue1, queue2 = arduino_reader.read_sensor_queue(queue_size)
    
    # Plot the values
    plt.figure(figsize=(10, 5))
    plt.plot(queue1, label='Sensor 1')
    plt.plot(queue2, label='Sensor 2 ')
    plt.title('Sensor data plot')
    plt.xlabel('Sample number')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

    # Close the serial connection
    arduino_reader.close()

# Only run the main function if the script is executed directly
if __name__ == "__main__":
    main()
