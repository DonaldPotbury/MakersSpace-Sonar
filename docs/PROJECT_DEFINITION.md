# Sonar Emulator — Project Definition

Build a Sonar Emulator using a Wemos D1 Mini, HC-SR04 ultrasonic sensor, and SG90 servo motor. The system must sweep the sensor with the servo, measure distance, and display the result as a live radar screen.

## Hardware and firmware

Create an Arduino sketch for a Wemos D1 Mini using these pins:

- `SERVO_PIN = D5`
- `ECHO_PIN = D6`
- `TRIGGER_PIN = D7`

The sketch must:

- Sweep the SG90 from 15° to 165° and back in 2° increments.
- Read the HC-SR04 after each servo movement.
- Send readings over USB serial at 115200 baud.
- Use one line per reading in this format:

```
angle,distance_cm
```

- Limit reported distances to 0–200 cm.
- Include appropriate timing for servo settling and ultrasonic measurement timeouts.

## Desktop Python application

Create `Sonar_Emulator/sonar_emulator.py`.

The Python application must:

- Use `pyserial`.
- Automatically identify and use the first USB serial port associated with an Arduino, Wemos, or common Arduino-compatible USB adapter, including CH340, CP210x, and FTDI.
- Open the port at 115200 baud.
- Parse `angle,distance_cm` serial lines.
- Show a Tkinter radar display with:
  - A dark background and green radar graphics.
  - A semicircular radar scan from 15° to 165°.
  - Distance rings and radial angle lines.
  - Red target dots for detected objects.
  - A green sweep line.
  - A connection/status line showing the latest angle and distance.
- Include a vertical desktop range slider labeled `RANGE (cm)`.
- Let the slider redraw the desktop radar at a selected maximum range from 25–200 cm.
- Preserve a short trail of recent measurements near the sweep angle.

## Local-network Web Radar

Keep the desktop application and USB serial connection functioning. Add a mobile-friendly web radar that receives the same live readings from the same Python process.

Architecture:

```
Wemos D1 Mini → USB serial → Python application
                                  ├─ Tkinter desktop radar
                                  └─ Local-network web radar
```

The web radar must:

- Use Flask.
- Be available to phones, tablets, and computers on the same local Wi-Fi network.
- Bind to all network interfaces so a device can use the computer’s local IP address.
- Print the selected address in the Python console, such as:

```
http://192.168.1.42:5000
```

- Serve a responsive browser radar page at `/`.
- Provide current radar data as JSON at `/api/radar`.
- Include a browser range slider from 25–200 cm that redraws only that browser’s radar view.
- Work in Safari on iPhone and common Android browsers.
- Preserve the desktop radar while the browser radar is active.

For the web-server port:

1. Try port 5000.
2. If unavailable, try 5010.
3. If unavailable, try 5020.
4. If unavailable, try 5030.
5. If all are unavailable, raise a clear exception listing the attempted ports.

## Project files and documentation

Include:

```
WemosSonar/WemosSonar.ino
Sonar_Emulator/sonar_emulator.py
Sonar_Emulator/web_templates/radar.html
requirements.txt
docs/WEB_RADAR.md
docs/CHANGELOG.md
```

`requirements.txt` must include:

```
pyserial>=3.5
Flask>=3.0
```

Document:

- Wiring and pin assignments.
- Required HC-SR04 Echo voltage level shifting for the 3.3 V Wemos.
- Separate regulated 5 V power for the SG90, with a shared ground.
- How to install dependencies.
- How to run the application from a terminal or Thonny.
- How to open the web radar from another device using the printed local-network address.
- Common connection troubleshooting, including firewall and guest Wi-Fi limitations.
- All project changes in `docs/CHANGELOG.md`.

Verify the Python syntax and verify that the Flask root page and `/api/radar` endpoint respond successfully before delivering the completed project.