#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
#define LIGHT_PIN A1

// Define potential Plant Pins (A0, A2-A5)
const int PLANT_PINS[] = {A0, A2, A3, A4, A5};
const int NUM_PLANTS = 5;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  // Initialize pins
  pinMode(LIGHT_PIN, INPUT);
  for(int i=0; i<NUM_PLANTS; i++) {
    pinMode(PLANT_PINS[i], INPUT);
  }
  
  Serial.println(F("GARDEN_UNIVERSAL_READY"));
}

void loop() {
  // 1. Environment
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int light = analogRead(LIGHT_PIN);

  // Check if DHT read failed, using 0 as fallback to keep format
  if (isnan(h) || isnan(t)) {
    h = 0;
    t = 0;
  }

  // 2. Output Stream: TEMP|HUM|LIGHT|A0|A2|A3|A4|A5
  Serial.print(t); Serial.print("|");
  Serial.print(h); Serial.print("|");
  Serial.print(light);

  for(int i=0; i<NUM_PLANTS; i++) {
    Serial.print("|");
    Serial.print(analogRead(PLANT_PINS[i]));
  }
  
  Serial.println(); // End of line

  // Wait 2 seconds before next read
  delay(2000);
}