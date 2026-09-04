# Change log

## 2026-09-03

- Added web-server port fallback: 5000 is tried first, then 5010, 5020, and 5030 before an error is raised.
- Added a local-network web radar for iPhone, Android, tablets, and computers while preserving the existing desktop display and USB serial reader.

## 2026-08-22

- Added a vertical range slider to the Python radar display; it redraws the view for a selected 25–200 cm maximum range.
- Updated the HC-SR04 wiring: trigger is D7 and echo is D6.
- Moved `sonar_emulator.py` into `Sonar_Emulator` for direct execution.
- Updated Wemos wiring assignments: SG90 signal on D5, HC-SR04 trigger on D6, and HC-SR04 echo on D7.
- Updated the README with project setup, hardware, wiring, and citation information; added the sonar and wiring diagrams to `images`.
- Renamed the project documentation folder from `Docs` to `docs`.
- Added an `images` folder for project imagery and visual assets.
- Added the Wemos D1 Mini firmware that sweeps an SG90 and reports HC-SR04 distance readings over USB serial.
- Added the Python Sonar Emulator radar display with automatic Arduino/clone USB-port discovery.
- Added wiring, upload, run, serial protocol, and safety guidance.
