#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>

Adafruit_BME680 bme; // I2C

#define LIGHT_PIN A1

// Moisture pins moved from A5 to A3 for I2C compatibility
const int PLANT_PINS[] = {A0, A2, A3};
const int NUM_PLANTS = 3;
const int SAMPLES = 50;

void setup() {
  Serial.begin(9600);
  delay(3000); // Settle I2C bus
  if (!bme.begin(0x76) && !bme.begin(0x77)) {
    Serial.println(F("Could not find a valid BME680 sensor, check wiring!"));
  } else {
    // Set up oversampling and filter initialization
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320*C for 150 ms
  }

  pinMode(LIGHT_PIN, INPUT);
  for(int i=0; i<NUM_PLANTS; i++) {
    pinMode(PLANT_PINS[i], INPUT);
  }

  Serial.println(F("--- GARDENOS FIRMWARE v2.2 (BME680) TARGETED ---"));
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
  float h = 0;
  float t = 0;
  float p = 0;
  float g = 0;

  if (bme.performReading()) {
    h = bme.humidity;
    t = bme.temperature;
    p = bme.pressure / 100.0; // hPa
    g = bme.gas_resistance / 1000.0; // KOhms
  }

  int light = getAveragedRead(LIGHT_PIN);

  // Output: TEMP|HUM|LIGHT|A0|A2|A3|PRESS|GAS
  Serial.print(t); Serial.print("|");
  Serial.print(h); Serial.print("|");
  Serial.print(light);

  for(int i=0; i<NUM_PLANTS; i++) {
    Serial.print("|");
    Serial.print(getAveragedRead(PLANT_PINS[i]));
  }
  Serial.print("|");
  Serial.print(p);
  Serial.print("|");
  Serial.print(g);
  Serial.println();

  delay(5000);
}