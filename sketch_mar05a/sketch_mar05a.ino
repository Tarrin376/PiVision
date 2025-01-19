
const int ledPin = 3;     // the number of the LED pin, D3
const int buttonPin = 4;  // the number of the pushbutton pin, D4
int buttonState;          // the state of the button
int ledState = LOW;       // the state of the LED
int prevButtonState = 1;  // The previous state of the LED Button
int joystickVal = 0;      // Determines if the user is scrolling in, out, or not at all (values would be 1, -1, 0 respectively)

void setup() {
  // Configures the button pin on the arduino as input
  pinMode(buttonPin, INPUT);
  // Configures the LED pin on the arduino as output
  pinMode(ledPin, OUTPUT);
  // Writes the current LED state to the LED pin
  digitalWrite(ledPin, ledState);
  // Initialises the serial communication as 9600 bits per second
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  
  // Determines if the button has been pressed (0) or not (1)
  int buttonPress = !buttonState && !prevButtonState ? 1 : buttonState;
  // Maps the light value from the light sensor to a number from 0 to 10
  int light = map(analogRead(A3), 0, 800, 0, 10);
  
  // Reads the x coordinate value on the joystick
  int xCoord = analogRead(A1);
  // Determines if the user is zooming in (1), zooming out (-1), or not at all (0)
  int joystickVal = xCoord > 520 ? 1 : xCoord < 500 ? -1 : 0;
  
  // Data that will be sent to the raspberry PI in stringified form
  int data[3] = {buttonPress, light, joystickVal};
  int length = sizeof(data) / sizeof(data[0]);
  String result = "";
  
  for (int i = 0; i < length; i++) {
    if (i < length - 1) result += String(data[i]) + " ";
    else result += String(data[i]);
  }
  
  // Prints the stringified result of "data" to the serial port for the raspberry PI to read
  Serial.println(result);
  
  // Updates the button state
  prevButtonState = buttonState;
  delay(200);
}

