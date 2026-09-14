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

- [Arduino IDE](https://www.arduino.cc/en/software/)
- The ESP8266 board package for the Arduino IDE
- [Thonny](https://thonny.org/) Python IDE
- Python 3

## Safety first

The Wemos uses 3.3 V logic, but the HC-SR04 Echo pin can output 5 V. Do **not** connect Echo directly to the Wemos. Use a logic-level shifter or a voltage divider between HC-SR04 Echo and Wemos D6.

Servos can draw more current than the Wemos can safely provide. For reliable operation, power the SG90 from a separate regulated 5 V supply. Connect the servo power supply ground to the Wemos GND so every part shares a common ground.

Disconnect USB power before changing wires.

## Step 1: Understand the parts

| Part | Job in this project |
| --- | --- |
| Wemos D1 Mini | Runs the program and sends measurements to the computer. |
| HC-SR04 | Sends an ultrasonic sound pulse and measures the returning echo. |
| SG90 servo | Turns the HC-SR04 so it can scan across an area. |
| Computer | Runs Python and draws the radar screen. |

The HC-SR04 measures distance by timing how long sound takes to travel to an object and return. Soft materials, angled surfaces, and very small objects may not reflect sound well.

## Step 2: Wire the circuit

Use this table as your wiring checklist.

| Wemos D1 Mini | Connect to | Notes |
| --- | --- | --- |
| GND | HC-SR04 GND and servo black/brown wire | All grounds must connect together. |
| 5V | HC-SR04 VCC | Powers the sensor. |
| D7 (GPIO13) | HC-SR04 Trig | Trigger signal. |
| D6 (GPIO12) | HC-SR04 Echo through a level shifter/divider | Never connect the 5 V Echo signal directly to D6. |
| D5 (GPIO14) | Servo yellow/orange signal wire | Servo control signal. |
| External 5 V positive | Servo red wire | Recommended servo power. |
| External 5 V ground | Wemos GND and servo black/brown wire | Creates the shared ground. |

![Wiring diagram](../images/Wiring%20Diagram%20Half%20Board.png)

Before continuing, check the wire colors and labels on your own servo. Wire colors sometimes differ between manufacturers.

## Step 3: Assemble the scanner

Attach the HC-SR04 to the SG90 servo horn or the project mount. The sensor should point forward when the servo is near the middle of its travel. Leave enough slack in the wires for the sensor to rotate without pulling them loose.

Do not force the servo by hand while it is powered.

## Step 4: Prepare the Arduino IDE

1. Install and open Arduino IDE.
2. Add the ESP8266 board package using Arduino IDE's **Boards Manager**.
3. Connect the Wemos D1 Mini with a USB data cable.
4. In **Tools → Board**, choose **LOLIN(WEMOS) D1 R2 & mini** or the matching Wemos D1 Mini board.
5. In **Tools → Port**, choose the port for the Wemos.
6. Open `WemosSonar/WemosSonar.ino` from this project.

The sketch sweeps from 15° to 165°, reads the sensor at each position, and sends readings in this format:

```text
angle,distance_cm
```

For example, `90,42` means the sensor detected an object 42 cm away while pointing straight ahead.

## Step 5: Upload and test the Wemos sketch

1. Click **Upload** in Arduino IDE.
2. Wait for the upload to complete.
3. Optional: open the Serial Monitor and set it to **115200 baud**.
4. Confirm that lines such as `90,42` appear as the servo moves.
5. Close the Serial Monitor before running the Python program. Only one program can use the serial port at a time.

If upload fails, confirm that you selected the correct board and USB port. Some clone Wemos boards use a CH340 USB-to-serial chip and may need a compatible driver.

## Step 6: Prepare Python in Thonny

1. Open Thonny.
2. Open `Sonar_Emulator/sonar_emulator.py`.
3. Select **Tools → Manage packages…**.
4. Search for and install `pyserial`.
5. Confirm Thonny is using Python 3 in **Tools → Options → Interpreter**.

You can also install the requirement from a terminal in the project folder:

```sh
python3 -m pip install -r requirements.txt
```

## Step 7: Run the radar

1. Make sure the Arduino Serial Monitor is closed.
2. Keep the Wemos connected by USB.
3. In Thonny, click the green **Run** button.
4. The program automatically looks for the first connected Arduino-compatible USB serial device.
5. Move your hand or another object in front of the sensor.

The green line is the current scan direction. Red dots show objects detected within the selected range.

Use the vertical **RANGE (cm)** slider to set the maximum displayed distance from 25 to 200 cm. A smaller range makes nearby objects appear farther apart on the screen.

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

## Clean up

Close the Python program before disconnecting the Wemos. Turn off the external servo power supply before changing or storing wiring.
