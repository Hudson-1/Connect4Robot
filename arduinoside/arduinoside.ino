#include <Servo.h>

Servo servo;

int positions[] = {1273, 1340, 1400, 1455, 1520, 1575, 1640, 2220}; // Adjust angles for 7 positions
const int restPosition = 2300; // Adjust based on rest position

void setup() {
  Serial.begin(9600);
  servo.attach(9);  // Attach the servo to pin 9
  servo.write(restPosition);  // Move to rest position
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("MOVE_TO")) {
      int col = command.substring(8).toInt();
      if (col >= 0 && col <= 6) {
        servo.write(positions[col]);
        delay(2000);  // Wait for the servo to move
      }
    } else if (command == "RESET") {
      servo.write(restPosition);
      delay(2000);  // Wait for the servo to return
    }
  }
}
