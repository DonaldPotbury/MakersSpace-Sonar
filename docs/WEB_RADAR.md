# Web radar

The desktop Sonar Emulator now also hosts a live radar page for phones, tablets, and other computers on the same Wi-Fi network. The Wemos remains connected to the computer by USB; only the screen is shared over the network.

## Start the program

Install the Python requirements, then start the existing application from the project root:

```sh
python3 -m pip install -r requirements.txt
python3 Sonar_Emulator/sonar_emulator.py
```

The terminal prints an address similar to `http://192.168.1.42:5000`. Open that address on the phone or tablet while it is connected to the same Wi-Fi network. The desktop radar and web radar update from the same serial reading. If port 5000 is busy, the program tries 5010, 5020, then 5030 and prints the address it selected.

## If the phone cannot connect

- Confirm that the phone and computer are on the same local network; guest Wi-Fi networks commonly prevent devices from talking to one another.
- Leave the Python application open.
- Allow incoming connections for Python when the computer firewall asks. The web radar uses local-network port 5000, or 5010, 5020, or 5030 when 5000 is already in use.
- Use the numeric address printed by the program, not `localhost`. On a phone, `localhost` means the phone itself.

## Web controls

Use **Maximum range** to redraw the web radar from 25 to 200 cm. This affects only that browser's view; the desktop slider and other devices can use different ranges.
