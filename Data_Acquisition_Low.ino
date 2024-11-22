#include <_Teensy.h>
#include <stdio.h>

void setup() {
  // Initialize serial communication at 2000000 baud
  Serial.begin(2000000);
}

void loop() {
  // Read the analog value from pin A3 (value range 0-1023)
  int sensorValue1 = analogRead(14);
  int sensorValue2 = analogRead(18);

  // Send the sensor values as 4-byte integers
  Serial.write((uint8_t *)&sensorValue1, sizeof(sensorValue1));
  Serial.write((uint8_t *)&sensorValue2, sizeof(sensorValue2));
  }
