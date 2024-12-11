# Smart_Marimba
This repositry will contains all the codes of the Smart Marimba project, they will be updated regularly.

## ArduinoReader
This is a class containing all the Teensy/Arduino interactions, it can be used to read single values from the device, or read a queue of values.
Additionally, it contains a function to initialize the serial communication, to estimate the sampling rate, and to close the serial communication.

## HitDetection
This code is used to detect the hit using computer vision, where a green object is used as a reference point. This is later used to train our model.

## DistanceFinder
This class contains all the methods used to find the distance given the two sensor time series.

## MidiPlayer
This class is used to convert the distance into musical notes it contains functions that allows us to save these notes as a midi file, or to send them as midi messages. Additionally we can use this class to play a midi file, or synthesize midi events directly.

## Data_Acquisition
Files that start with this name refer to the Arduino/Teensy code that is used to record the data points.

### Data_Acquisition_Low
This file is used to record data from the two piezo devices using the regular sampling speed.

### Data_Acquisition_High
This file is used to record data from the two piezo devices at 400 KHz, the data are saved on the interior buffer of the chip, then are sent to the computer.

## Data_Processing
Files that start with this name refer to the python code that is used to read, and process the data acquired

