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
