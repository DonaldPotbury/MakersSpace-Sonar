/*
  Sonar Emulator transmitter
  Wemos D1 Mini + HC-SR04 + SG90

  Sends one CSV measurement per line: angle,distance_cm
*/

#include <Servo.h>

const uint8_t TRIGGER_PIN = D6;
const uint8_t ECHO_PIN = D7;
const uint8_t SERVO_PIN = D5;
const int MIN_ANGLE = 15;
const int MAX_ANGLE = 165;
const int STEP_DEGREES = 2;
const int MAX_DISTANCE_CM = 200;

Servo scanner;

int readDistanceCm() {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  // 25 ms timeout is safely beyond the display range and prevents blocking.
  const unsigned long duration = pulseIn(ECHO_PIN, HIGH, 25000);
  if (duration == 0) return MAX_DISTANCE_CM;
  return constrain(duration / 58, 0, MAX_DISTANCE_CM);
}

void scan(int startAngle, int endAngle, int increment) {
  for (int angle = startAngle; angle != endAngle + increment; angle += increment) {
    scanner.write(angle);
    delay(35);  // Give the SG90 time to reach each step.
    Serial.printf("%d,%d\n", angle, readDistanceCm());
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  scanner.attach(SERVO_PIN);
  scanner.write(90);
  delay(500);
}

void loop() {
  scan(MIN_ANGLE, MAX_ANGLE, STEP_DEGREES);
  scan(MAX_ANGLE, MIN_ANGLE, -STEP_DEGREES);
}
