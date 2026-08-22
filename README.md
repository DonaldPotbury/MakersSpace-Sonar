# Sonar Emulator

A Wemos D1 Mini sweeps an HC-SR04 ultrasonic sensor with an SG90 servo and sends each reading over USB serial. `sonar_emulator.py` automatically selects the first detected Arduino-compatible USB serial port and renders the readings as a radar display.

## Wiring

| Module | Wemos D1 Mini pin | Notes |
| --- | --- | --- |
| HC-SR04 TRIG | D5 (GPIO14) | Direct connection |
| HC-SR04 ECHO | D6 (GPIO12) | **Use a 5 V-to-3.3 V voltage divider or logic level shifter.** |
| SG90 signal | D7 (GPIO13) | Servo control signal |
| All grounds | GND | Must share a common ground |
| HC-SR04 VCC | 5V | Sensor supply |
| SG90 VCC | External regulated 5 V | Do not power the servo from the Wemos USB/3.3 V rail. Connect its ground to Wemos GND. |

## Upload and run

1. In the Arduino IDE, install the ESP8266 board package and select **LOLIN(WEMOS) D1 R2 & mini**.
2. Open and upload [`WemosSonar/WemosSonar.ino`](WemosSonar/WemosSonar.ino). Close the Arduino Serial Monitor afterwards; it cannot share the port with the radar app.
3. On the computer, install the Python dependency:

   ```sh
   python3 -m pip install -r requirements.txt
   ```

4. Start the display:

   ```sh
   python3 sonar_emulator.py
   ```

The sketch emits `angle,distance_cm` lines at 115200 baud. The display supports measurements from 0–200 cm and scans from 15° to 165°.

## Port selection

The app examines USB serial ports in the order reported by the operating system. It accepts Arduino VID/PIDs and typical clone interfaces (CH340, CP210x, FTDI, Wemos, and matching descriptions), then connects to the first match. If it cannot find one, connect the board by USB and restart the program.
