#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
#define LIGHT_PIN A1

// ONLY the connected pins (A0, A2, A5)
const int PLANT_PINS[] = {A0, A2, A5};
const int NUM_PLANTS = 3;
const int SAMPLES = 50;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(LIGHT_PIN, INPUT);
  for(int i=0; i<NUM_PLANTS; i++) {
    pinMode(PLANT_PINS[i], INPUT);
  }
  
  Serial.println(F("--- GARDENOS FIRMWARE v2.1 TARGETED ---"));
  Serial.println(F("GARDEN_UNIVERSAL_READY"));
}

int getAveragedRead(int pin) {
  long sum = 0;
  analogRead(pin); // Switch mux
  delay(20);       // Longer settling time
  
  for(int i=0; i<SAMPLES; i++) {
    sum += analogRead(pin);
    delay(2);
  }
  return (int)(sum / SAMPLES);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int light = getAveragedRead(LIGHT_PIN);

  if (isnan(h) || isnan(t)) { h = 0; t = 0; }

  // Output: TEMP|HUM|LIGHT|A0|A2|A5
  Serial.print(t); Serial.print("|");
  Serial.print(h); Serial.print("|");
  Serial.print(light);

  for(int i=0; i<NUM_PLANTS; i++) {
    Serial.print("|");
    Serial.print(getAveragedRead(PLANT_PINS[i]));
  }
  Serial.println();
  delay(5000);
}