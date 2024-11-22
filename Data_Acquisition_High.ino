
#include <ADC.h>
#include <_Teensy.h>
#include <stdio.h>

const int readpin1 = A3;  // First analog input pin
const int readpin2 = A8;  // Second analog input pin

ADC *adc = new ADC(); // ADC object

#define SAMPRATE 200000  // Sampling rate 200 000 Hz
#define AVERAGING 1
#define RESOLUTION 12

#define ADCSAMPLES 10000 // Number of samples to collect
// This code records 10000 Samples using the internal teensy ADC, at a sampling rate of 200-400 Khz, These samples are recorded
// on the internal buffer of the teensy, and are sent one the sampling is done

uint16_t adcbuffer1[ADCSAMPLES]; // Buffer for first analog input
uint16_t adcbuffer2[ADCSAMPLES]; // Buffer for second analog input
volatile uint32_t adcidx = 0; // Must be volatile as it is changed in interrupt handler
unsigned long startTime, endTime; // Variables to store start and end time
const char compileTime[] = "ADC Timer test Compiled on " __DATE__ " " __TIME__;

void setup() {
  delay(10);
  Serial.begin(200000);
  delay(500);
  pinMode(readpin1);
  pinMode(readpin2);
  adc->adc0->setAveraging(AVERAGING); // Set number of averages
  adc->adc0->setResolution(RESOLUTION); // Set bits of resolution
  adc->adc0->setConversionSpeed(ADC_CONVERSION_SPEED::HIGH_SPEED);  // Set the conversion speed
  adc->adc0->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // Set the sampling speed

  adc->adc1->setAveraging(AVERAGING); // Set number of averages
  adc->adc1->setResolution(RESOLUTION); // Set bits of resolution
  adc->adc1->setConversionSpeed(ADC_CONVERSION_SPEED::HIGH_SPEED);  // Set the conversion speed
  adc->adc1->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // Set the sampling speed
  delay(500);
  // These delays are inserted so that the ADC finishes setting up
  Serial.print("\n\n");
  Serial.println(compileTime);
  Serial.println("Press <n> to collect and display data");

  
}

void loop() {
  char ch;
  if (Serial.available()) {
    ch = Serial.read();
    //once n is pressed, Data Acquisition starts
    if (ch == 'n') GetADCData();
  }
}

// This ISR reads both ADCs
void adc0_isr() {
  uint16_t adc_val1, adc_val2;

  // Read analog values from both ADCs
  adc_val1 = adc->adc0->readSingle();
  adc_val2 = adc->adc1->readSingle();

  if (adcidx < ADCSAMPLES) {  // Storage stops when enough samples collected
    adcbuffer1[adcidx] = adc_val1;
    adcbuffer2[adcidx] = adc_val2;
    adcidx++;
  }

  // Trigger the next reads
  adc->adc0->startSingleRead(readpin1);
  adc->adc1->startSingleRead(readpin2);
}

void GetADCData(void) {
  // THis function uses the adc library to collect 10 000 samples and records the time taken to collect them
  delay(100); // Wait for USB serial to finish
  adcidx = 0;
  // Setup initial reads
  adc->adc0->startSingleRead(readpin1); 
  adc->adc1->startSingleRead(readpin2);
  adc->adc0->enableInterrupts(adc0_isr);

  startTime = micros(); // Record the start time
  while (adcidx < ADCSAMPLES) {
    // Wait for data collection to complete
  }
  endTime = micros(); // Record the end time

  adc->adc0->stopTimer();
  Serial.println("Collection complete.");
  ShowADC();
}

// Display the start of data in counts. Send 10 values per line
// Data is in the global variables adcbuffer1 and adcbuffer2.
void ShowADC(void) {
  uint32_t i;
  Serial.println("ADC Data in Counts");
  for (i = 0; i < ADCSAMPLES; i++) {
    if ((i % 10) == 0) {
      Serial.printf("\n% 3d: ", i);
    }
    Serial.printf("% 5d, % 5d", adcbuffer1[i], adcbuffer2[i]);
    if ((i + 1) % 10 == 0) {
      Serial.println();
    }
  }
  Serial.println();
  // Calculate and print the total time taken to collect the samples, this is our reference for the sampling rate
  Serial.print("Time taken to record samples: ");
  Serial.print(endTime - startTime);
  Serial.println(" microseconds");
}
