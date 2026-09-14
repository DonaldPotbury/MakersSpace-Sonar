# Student Guide: Build a Sonar Emulator

## What you will make

You will build a small radar-like distance sensor. A servo motor turns an ultrasonic sensor left and right. The sensor measures how far away an object is, and a Python program on your computer draws the object on a radar screen.

![Completed sonar emulator](../images/Sonar%20Emulator%20Photo.png)

## Learning goals

After completing this project, you should be able to:

- Connect electronic parts to a microcontroller using a wiring diagram.
- Upload an Arduino sketch to a Wemos D1 Mini.
- Use an ultrasonic sensor to measure distance.
- Use serial communication to send data from a microcontroller to a computer.
- Run a Python program and change the radar display range.



## Parts and software

### Hardware

- Wemos D1 Mini
- HC-SR04 ultrasonic distance sensor
- SG90 micro servo
- Breadboard
- Jumper wires: male-to-male and male-to-female
- USB data cable for the Wemos D1 Mini
- A regulated 5 V power source for the servo is recommended
- A voltage divider or logic-level shifter for the HC-SR04 Echo signal

### Software

- [Arduino IDE](https://www.arduino.cc/en/software/) - https://www.arduino.cc/en/software/
  - The ESP8266 board package for the Arduino IDE

- [Thonny](https://thonny.org/) Python IDE - https://thonny.org/

  - Python 3 should be bundled with Thonny

- [Codex by ChatGPT](https://chatgpt.com/download/) - https://chatgpt.com/download/

  

# Steps:

## Download and Install the Software:



## Understand the Parts and Wire the Circuit:

| Part          | Job in this project                                          |
| ------------- | ------------------------------------------------------------ |
| Wemos D1 Mini | Runs the program and sends measurements to the computer.     |
| HC-SR04       | Sends an ultrasonic sound pulse and measures the returning echo. |
| SG90 servo    | Turns the HC-SR04 so it can scan across an area.             |
| Computer      | Runs Python and draws the radar screen.                      |

The HC-SR04 measures distance by timing how long sound takes to travel to an object and return. Soft materials, angled surfaces, and very small objects may not reflect sound well.



### Use this table as your wiring checklist.

| Wemos D1 Mini | Connect to                                   | Notes                                             |
| ------------- | -------------------------------------------- | ------------------------------------------------- |
| GND           | HC-SR04 GND and servo black/brown wire       | All grounds must connect together.                |
| 5V            | HC-SR04 VCC                                  | Powers the sensor.                                |
| D7 (GPIO13)   | HC-SR04 Trig                                 | Trigger signal.                                   |
| D6 (GPIO12)   | HC-SR04 Echo through a level shifter/divider | Never connect the 5 V Echo signal directly to D6. |
| D5 (GPIO14)   | Servo yellow/orange signal wire              | Servo control signal.                             |

![Wiring diagram](../images/Wiring%20Diagram%20Half%20Board.png)

Before continuing, check the wire colors and labels on your own servo. Wire colors sometimes differ between manufacturers.



## Assemble the Scanner

Attach the HC-SR04 to the SG90 servo horn or the project mount. The sensor should point forward when the servo is near the middle of its travel. Leave enough slack in the wires for the sensor to rotate without pulling them loose.

Do not force the servo by hand while it is powered.


## Open ChatGPT and Setup a Project
- Go to the Codex section
- You will find a Projects Section along the left side.
- Click the (+) sign
- Project Name:  MakersSpace-Sonar
- Click Add a folder to this computer
  - Browse to the location you wish place the folder
  - Create a folder named MakersSpace-Sonar
  - Click Open
  - Click Create Project
  - Click File/New Chat
  - Choose the MakersSpace-Sonar project
  - You should see "What should we work on in MakersSpace-Sonar"
    - If not, you can select that project in the space just above where is says "Do anything"



## Type in your Instructions
These are the instructions I used:

- Create a "Sonar Emulator" using a Wemos D1 Mini, HC-SR04, SG90 servo. The output should be a Python script running on my computer that resembles a radar screen. Serial communication shall be used between the Wemos D1 Mini and my computer. The python script shall identify and use the first usb port with an arduino or clone attached. Log all changes in a /Docs folder
- Please make SERVO_PIN = D5, ECHO_PIN = D6, TRIGGER_PIN = D7
- Please make a vertical slider bar in the python script. Moving it will change the maximum range and redraw the radar screen to suit

**At this point AI shojld have created code in your project folder**

- Use the Arduino IDE to upload the Arduino code to the WeMos D1 Mini

- Launch Thonny and Open the Python code
  - The program may fail the first time you run it.  That's because there are some modules that will needed downloaded.
  - Make a note of the names.
  - Select **Tools → Manage packages…**.
  - Search for and install those packages.

- Try again



## Troubleshooting

| Problem | Things to check |
| --- | --- |
| The servo does not move | Check D5, servo power, and the shared ground. Use an external 5 V servo supply. |
| The radar window says no Arduino-compatible device was found | Check the USB data cable, reconnect the Wemos, and confirm that the correct driver is installed. |
| The Python program cannot open the port | Close Arduino Serial Monitor and any other program using the Wemos port. |
| Distances jump around | Check loose wires, use a stable power supply, and keep the sensor and servo firmly mounted. |
| Everything stops when the servo moves | The servo likely needs more power. Use a separate regulated 5 V supply with a shared ground. |
| Objects are not detected | Aim at a large, flat object. Very soft, narrow, or angled objects may reflect too little ultrasonic sound. |



## Try these challenges

1. Measure the distance to a wall and compare the radar value with a tape measure.
2. Change the maximum display range and observe how the radar scale changes.
3. Place objects made of cardboard, fabric, plastic, and metal in front of the sensor. Which materials produce the most reliable readings?
4. Change the sweep angle in the Arduino sketch and observe how the radar display changes.
5. Add a small label or 3D-printed mount to make the project easier for someone else to use.
