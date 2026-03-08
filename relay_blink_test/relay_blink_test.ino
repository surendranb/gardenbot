#define RELAY_PIN 3

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  digitalWrite(RELAY_PIN, LOW);  // Turn ON (Active LOW relay)
  delay(2000);
  digitalWrite(RELAY_PIN, HIGH); // Turn OFF
  delay(2000);
}
