#include <Servo.h>

// Constants
const int NUM_SENSORS = 7;
const int SENSOR_PINS[NUM_SENSORS] = {2, 3, 4, 5, 6, 7, 8}; // Break beam sensor pins
const int SERVO_PIN = 9; // Servo control pin
const int SERVO_POSITIONS[NUM_SENSORS] = {10, 30, 50, 70, 90, 110, 130}; // Servo positions for each column

// Servo object
Servo armServo;

// Variables
int detectedColumn = -1; // Stores the column detected by sensors

void setup() {
  // Initialize servo
  armServo.attach(SERVO_PIN);
  armServo.write(0); // Start servo at home position

  // Initialize break beam sensors as inputs
  for (int i = 0; i < NUM_SENSORS; i++) {
    pinMode(SENSOR_PINS[i], INPUT_PULLUP); // Use internal pullup resistors
  }

  // Begin serial communication for debugging
  Serial.begin(9600);
  Serial.println("Connect 4 Robot Initialized");
}

void loop() {
  // Detect human move
  detectedColumn = detectHumanMove();
  if (detectedColumn != -1) {
    Serial.print("Human dropped a piece in column: ");
    Serial.println(detectedColumn);

    // Move servo to the detected column
    moveArmToColumn(detectedColumn);

    // Wait for the robot to place its piece
    delay(1000);

    // Move servo back to home position
    moveArmHome();

    // Wait for the human's next turn
    delay(1000);
  }
}

// Function to detect which column the human dropped a piece into
int detectHumanMove() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    if (digitalRead(SENSOR_PINS[i]) == LOW) { // Sensor beam is broken
      delay(500); // Debounce delay to avoid multiple detections
      return i;
    }
  }
  return -1; // No move detected
}

// Function to move the arm to the specified column
void moveArmToColumn(int column) {
  if (column >= 0 && column < NUM_SENSORS) {
    int position = SERVO_POSITIONS[column];
    Serial.print("Moving arm to column ");
    Serial.println(column);
    armServo.write(position); // Move servo to the specified position
    delay(500); // Allow time for movement
  }
}

// Function to move the arm back to the home position
void moveArmHome() {
  Serial.println("Moving arm to home position");
  armServo.write(0); // Move servo to home position
  delay(500); // Allow time for movement
}
