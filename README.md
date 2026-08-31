
# Goal:

Create a "Sonar Emulator" with the information presented in the form of a "radar" screen.
All coding will be generated using Codex.

![](images/Sonar%20Emulator.png)





# Software:

- [Arduino IDE](https://www.arduino.cc/en/software/)
	- "The Arduino IDE is a free, open-source program for writing code (“sketches”), checking it for errors, and uploading it to an Arduino boards."
	- For this project we need to configure the IDE for an ESP8266.  Instructions can be found here...
	  https://www.youtube.com/watch?v=UUQ84VKg3oM
	
- [Thonny](https://thonny.org/)
	- Thonny is a beginner-friendly app for writing and running Python code.

- [Codex by ChatGPT](https://chatgpt.com/codex/?utm_source=google&utm_medium=paid_search&c_id=23226110534&c_agid=194939268903&c_crid=807810285009&c_kwid=kwd-827611117561&c_ims=&c_pms=9016357&c_nw=g&c_dvc=c&gad_source=1&gad_campaignid=23226110534&gbraid=0AAAAA-I0E5f7W5mTFuf6gr5LX9oKT2n66&gclid=CjwKCAjwkaXUBhASEiwAZI3ds9iR6Z_cTBhbpIHWuGR-XCghlkN1L37nnO0KQ0bv7Ey1-0yHv3DdmBoCnoEQAvD_BwE)
	- OpenAI's AI coding agent built into ChatGPT. It's designed specifically to help with software development (OpenAI)
		- Downloaded and install.
		- You will be prompted to create an account.  I chose the free level.
- [Github](https://github.com/)
	- GitHub is an online platform for storing, sharing, and collaborating on software projects.
		- While technically not needed, using it is considered best practice.
		- You will need to create an account.
# Hardware:
- [WeMos D1 Mini](https://www.amazon.com/dp/B0CL9CTXZH?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
- [HC-SR04 Ultrasonic Module Distance Sensor](https://a.co/d/0bF3r0CX)
- [Sg90 9g Micro Servo Motor](https://a.co/d/08NuCzbu) 
- [Solderless breadboard](https://a.co/d/0ajafzjM)
- [Jumper Wires](https://a.co/d/02a42jzD)
  - You will need both (male to male) and (male to female) jumpers.



# 3D Printed Parts:

https://makerworld.com/en/models/3213247-radar-sonar-emulator

![Sonar Emulator Mount 1](/Users/donpotbury/Documents/GitHub/MakersSpace-Sonar/images/Sonar Emulator Mount 1.png)



# Pinouts:

![WeMos-D1-Mini-Pinout](/Users/donpotbury/Documents/GitHub/MakersSpace-Sonar/images/WeMos-D1-Mini-Pinout.png)



![HD-SR04 Pinout](/Users/donpotbury/Documents/GitHub/MakersSpace-Sonar/images/HD-SR04 Pinout.jpeg)





# Wiring:

| WeMos D1 Mini | HC-SR04 | Servo                |
| ------------- | ------- | -------------------- |
| GND           | GND     | GND (black wire)     |
| VBUS          | Vcc     | Power (red wire)     |
| D7 (GPIO13)   | Trig    |                      |
| D6 (GPIO12)   | Echo    |                      |
| D5 (GPIO14)   |         | Signal (yellow wire) |



##### ![Wiring Diagram](/Users/donpotbury/Documents/GitHub/MakersSpace-Sonar/images/Wiring Diagram.png)













# WeMos D1 Mini Code:

```
/*
  Sonar Emulator transmitter
  Wemos D1 Mini + HC-SR04 + SG90

  Sends one CSV measurement per line: angle,distance_cm
*/

#include <Servo.h>

const uint8_t TRIGGER_PIN = D7; // 13
const uint8_t ECHO_PIN = D6;    //12
const uint8_t SERVO_PIN = D5;   //14
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

```





# Python Code:

```
#!/usr/bin/env python3
"""Desktop radar display for a Wemos D1 Mini + HC-SR04 + SG90 sonar."""

from __future__ import annotations

import math
import queue
import re
import sys
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from typing import Optional

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("Missing dependency: install it with 'python3 -m pip install -r requirements.txt'.")
    raise SystemExit(1)


BAUD_RATE = 115200
SENSOR_MAX_DISTANCE_CM = 200
MIN_DISPLAY_RANGE_CM = 25
DEFAULT_DISPLAY_RANGE_CM = SENSOR_MAX_DISTANCE_CM
SCAN_ANGLES = range(15, 166, 2)
RADAR_GREEN = "#38ff75"
BACKGROUND = "#031007"

# Arduino and common USB-to-serial chips found on Arduino-compatible boards.
KNOWN_USB_IDS = {
    (0x2341, None), (0x2A03, None), (0x1A86, 0x7523),  # Arduino, CH340
    (0x10C4, 0xEA60), (0x0403, 0x6001),               # CP210x, FTDI
    (0x239A, None), (0x1B4F, None),
}
CLONE_KEYWORDS = ("arduino", "wemos", "ch340", "cp210", "usb serial", "wch", "ftdi")
LINE_PATTERN = re.compile(r"^\s*(\d{1,3})\s*,\s*(\d{1,3})\s*$")


@dataclass(frozen=True)
class Measurement:
    angle: int
    distance_cm: int


def find_arduino_port() -> Optional[str]:
    """Return the first USB serial port that appears to be an Arduino or clone."""
    for port in list_ports.comports():
        description = " ".join(filter(None, (port.description, port.manufacturer, port.product))).lower()
        known_id = any(
            port.vid == vendor and (product is None or port.pid == product)
            for vendor, product in KNOWN_USB_IDS
        )
        if known_id or any(word in description for word in CLONE_KEYWORDS):
            return port.device
    return None


class SerialReader(threading.Thread):
    def __init__(self, port: str, output: queue.Queue[Measurement | Exception]):
        super().__init__(daemon=True)
        self.port = port
        self.output = output
        self.stop_requested = threading.Event()
        self.connection: Optional[serial.Serial] = None

    def run(self) -> None:
        try:
            self.connection = serial.Serial(self.port, BAUD_RATE, timeout=0.5)
            # ESP8266 boards often reset when the serial connection opens.
            time.sleep(1.5)
            self.connection.reset_input_buffer()
            while not self.stop_requested.is_set():
                raw_line = self.connection.readline().decode("ascii", errors="ignore").strip()
                match = LINE_PATTERN.match(raw_line)
                if not match:
                    continue
                angle, distance = map(int, match.groups())
                if 0 <= angle <= 180 and 0 <= distance <= SENSOR_MAX_DISTANCE_CM:
                    self.output.put(Measurement(angle, distance))
        except Exception as error:  # Report connection failures to the UI thread.
            self.output.put(error)
        finally:
            if self.connection:
                self.connection.close()

    def close(self) -> None:
        self.stop_requested.set()


class SonarEmulator:
    def __init__(self, root: tk.Tk, port: str):
        self.root = root
        self.root.title("Sonar Emulator")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.max_distance_cm = DEFAULT_DISPLAY_RANGE_CM
        display = tk.Frame(root, bg=BACKGROUND)
        display.pack(padx=12, pady=(12, 4))
        self.canvas = tk.Canvas(display, width=760, height=470, bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack(side="left")
        slider_frame = tk.Frame(display, bg=BACKGROUND)
        slider_frame.pack(side="left", fill="y", padx=(8, 0))
        tk.Label(slider_frame, text="RANGE\n(cm)", bg=BACKGROUND, fg=RADAR_GREEN,
                 font=("Arial", 10, "bold"), justify="center").pack(pady=(6, 0))
        self.range_slider = tk.Scale(
            slider_frame,
            from_=SENSOR_MAX_DISTANCE_CM,
            to=MIN_DISPLAY_RANGE_CM,
            orient="vertical",
            length=350,
            resolution=5,
            command=self.set_display_range,
            bg=BACKGROUND,
            fg=RADAR_GREEN,
            troughcolor="#197a3c",
            activebackground=RADAR_GREEN,
            highlightthickness=0,
        )
        self.range_slider.set(self.max_distance_cm)
        self.range_slider.pack(fill="y", expand=True)
        self.status = tk.StringVar(value=f"Connected: {port}  |  Waiting for sensor data...")
        tk.Label(root, textvariable=self.status, bg=BACKGROUND, fg=RADAR_GREEN,
                 font=("Arial", 11)).pack(pady=(0, 10))
        self.messages: queue.Queue[Measurement | Exception] = queue.Queue()
        self.reader = SerialReader(port, self.messages)
        self.points: dict[int, int] = {}
        self.last_angle = 90
        self.reader.start()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.draw_radar()
        self.consume_messages()

    def draw_radar(self) -> None:
        self.canvas.delete("all")
        center_x, center_y, radius = 380, 430, 390
        # Semicircular range rings and radial markings.
        for fraction in (0.25, 0.5, 0.75, 1):
            r = radius * fraction
            self.canvas.create_arc(center_x - r, center_y - r, center_x + r, center_y + r,
                                   start=0, extent=180, outline="#197a3c", width=1)
            self.canvas.create_text(center_x + 8, center_y - r, text=f"{int(self.max_distance_cm * fraction)} cm",
                                    anchor="w", fill="#4fae68", font=("Arial", 9))
        for angle in (15, 45, 75, 90, 105, 135, 165):
            x, y = self.position(angle, self.max_distance_cm)
            self.canvas.create_line(center_x, center_y, x, y, fill="#197a3c")
        self.canvas.create_text(16, 16, text="SONAR EMULATOR", anchor="nw", fill=RADAR_GREEN,
                                font=("Arial", 16, "bold"))
        self.canvas.create_text(744, 16, text="15° — 165°", anchor="ne", fill="#4fae68", font=("Arial", 10))

        for angle, distance in self.points.items():
            if distance < self.max_distance_cm:
                x, y = self.position(angle, distance)
                self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#ff5454", outline="")
        sweep_x, sweep_y = self.position(self.last_angle, self.max_distance_cm)
        self.canvas.create_line(center_x, center_y, sweep_x, sweep_y, fill=RADAR_GREEN, width=2)

    def position(self, angle: int, distance: float) -> tuple[float, float]:
        radians = math.radians(angle)
        scale = 390 / self.max_distance_cm
        return 380 + distance * scale * math.cos(radians), 430 - distance * scale * math.sin(radians)

    def set_display_range(self, value: str) -> None:
        """Apply a new maximum display range from the vertical range slider."""
        self.max_distance_cm = int(float(value))
        self.draw_radar()

    def consume_messages(self) -> None:
        redraw = False
        try:
            while True:
                message = self.messages.get_nowait()
                if isinstance(message, Exception):
                    self.status.set(f"Serial error: {message}")
                    continue
                self.last_angle = message.angle
                self.points[message.angle] = message.distance_cm
                # Measurements from the trailing side of the sweep fade away.
                for angle in list(self.points):
                    if abs(angle - self.last_angle) > 28:
                        del self.points[angle]
                self.status.set(f"Connected: {self.reader.port}  |  {message.angle:3d}°  {message.distance_cm:3d} cm")
                redraw = True
        except queue.Empty:
            pass
        if redraw:
            self.draw_radar()
        self.root.after(25, self.consume_messages)

    def close(self) -> None:
        self.reader.close()
        self.root.destroy()


def main() -> None:
    port = find_arduino_port()
    if not port:
        print("No Arduino-compatible USB serial device found. Connect the Wemos D1 Mini and try again.")
        raise SystemExit(2)
    root = tk.Tk()
    SonarEmulator(root, port)
    root.mainloop()


if __name__ == "__main__":
    main()


```













# Notes:
> [!NOTE]
>
> I attempted to push my changes up to GitHub and was presented with this error:
>
>  Your remote uses HTTPS, so the simplest route is GitHub CLI authentication:
>  gh auth login
>  Choose:
>
>   1. GitHub.com
>   2. HTTPS
>   3. Login with a web browser
>   4. Confirm Yes when asked to authenticate Git for this account.
>      Finish the browser sign-in, then verify and push:
>       gh auth status
>       git push origin main
>       If gh isn’t installed, install GitHub CLI first (on macOS: brew install gh) or > use a GitHub personal access token when Git prompts for a password—GitHub no longer accepts account passwords for Git over HTTPS. GitHub’s authentication guidance
>
> I did not have GitHub CLI so I opened a terminal and entered:
>
> ```
> brew install gh
> ```
>
> I then typed in the command below And followed the prompts.
>
> ```
> gh auth login
> ```
>



> [!NOTE]
> When trying to flash the WeMos D1 Mini on a Windows 11 PC the following error occurred.
>
> *A serial exception error occurred: Cannot configure port, something went wrong. Original message: PermissionError(13, 'A device attached to the system is not functioning.',*
>
> After much searching the problem seemed to be caused by the newest driver for CH340 USB to Serial chip.  The most prevalent solution was to roll back the driver to the previous version.  ***The problem with this was the "Fix" might have to be re-applied after a Windows Update.***  
>
> Another proposed solution was to change the properties of the driver of the driver to "Enable the Serial Port Enumerator".  See https://www.youtube.com/watch?v=M6oq3dl5gBQ.  ***These simply did not work in our case***.
>
> Brian Witt wrote an article about "Fake CH340 Chips" https://www.digitaltown.co.uk/66FakeCH340Chips.php.  He pointed out the differences between a genuine CH340 chip which had clear markings on top and the "fake" chip which has no markings.  Had D1 minis in both configurations.   The genuine WCH CH340 worked with the latest driver where the fake one did not.  The photo below shows WCH CH340C marking.
>
> <img src="/Users/donpotbury/Documents/GitHub/MakersSpace-Sonar/images/WeMos D1 Mini.png" alt="WeMos D1 Mini" style="zoom:50%;" />
>
> ***Our solution was to purchase devices with the genuine CH340 chip.***






---
# Works Cited:
- “Arduino Software.” _Arduino_, [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software). Accessed 22 Aug. 2026.

- “What Is GitHub?” _GitHub Docs_, GitHub, [https://docs.github.com/en/get-started/start-your-journey/what-is-github](https://docs.github.com/en/get-started/start-your-journey/what-is-github). Accessed 22 Aug. 2026.

- *OpenAI*. “Codex.” _OpenAI_, [https://openai.com/codex/](https://openai.com/codex/). Accessed 22 Aug. 2026.
  _Thonny: Python IDE for Beginners._ Thonny, [https://thonny.org/](https://thonny.org/). Accessed 22 Aug. 2026.

- “Installing.” _ESP8266 Arduino Core Documentation_, [https://arduino-esp8266.readthedocs.io/en/latest/installing.html](https://arduino-esp8266.readthedocs.io/en/latest/installing.html). Accessed 22 Aug. 2026.

- Santos, Rui. “Installing ESP8266 Board in Arduino IDE (Windows, Mac OS X, Linux).” *Random Nerd Tutorials*, Random Nerd Tutorials. [https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/?utm_source=chatgpt.com)

- Witt, Brian. “Fake CH340 Chips.” *Digital Town*, https://www.digitaltown.co.uk/66FakeCH340Chips.php. Accessed 26 Aug. 2026.

- Random Nerd Tutorials. “ESP8266 Pinout Reference: Which GPIO Pins Should You Use?” *Random Nerd Tutorials*, https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/. Accessed 26 Aug. 2026.

- Prabhu, Shreepad. "WeMos D1 Mini Pinout Reference." *Last Minute Engineers, https://lastminuteengineers.com/wemos-d1-mini-pinout-reference/.  Accessed 31 Aug. 2026

- Prabhu, Amrit. “How HC-SR04 Ultrasonic Sensor Works & Interface It With Arduino.” *Last Minute Engineers*, 20 Jan. 2026, https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/. Accessed 31 Aug. 2026.



