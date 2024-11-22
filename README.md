# Smart_Marimba
This repositry will contains all the codes of the Smart Marimba project, they will be updated regularly.

## Data_Acquisition
Files that start with this name refer to the Arduino/Teensy code that is used to record the data points.

### Data_Acquisition_Low
This file is used to record data from the two piezo devices using the regular sampling speed.

### Data_Acquisition_High
This file is used to record data from the two piezo devices at 400 KHz, the data are saved on the interior buffer of the chip, then are sent to the computer.

## Data_Processing
Files that start with this name refer to the python code that is used to read, and process the data acquired

