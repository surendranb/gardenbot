#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
#define RELAY_PIN 3
#define TRIG_PIN 4
#define ECHO_PIN 5
#define SOIL_PIN A0
#define LIGHT_PIN A1

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // Relay OFF (Active LOW)
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  dht.begin();
  Serial.println(F("SMART_GARDEN_READY"));
}

long getWaterDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2; // Distance in cm
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int soilValue = analogRead(SOIL_PIN);
  int lightValue = analogRead(LIGHT_PIN);
  long waterDist = getWaterDistance();
  String relayStatus = (digitalRead(RELAY_PIN) == LOW) ? "ON" : "OFF";

  // Data Format: TEMP|HUM|SOIL|LIGHT|WATER_DIST|RELAY
  Serial.print(t); Serial.print("|");
  Serial.print(h); Serial.print("|");
  Serial.print(soilValue); Serial.print("|");
  Serial.print(lightValue); Serial.print("|");
  Serial.print(waterDist); Serial.print("|");
  Serial.println(relayStatus);

  // Handle manual commands from Python
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "WATER_ON") digitalWrite(RELAY_PIN, LOW);
    if (command == "WATER_OFF") digitalWrite(RELAY_PIN, HIGH);
  }

  delay(2000); // Read every 2 seconds
}
