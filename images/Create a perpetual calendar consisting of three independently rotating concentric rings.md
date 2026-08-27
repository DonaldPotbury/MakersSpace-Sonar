Create a perpetual calendar consisting of three independently rotating concentric rings.  The outer ring represents the day of the month (1-31).  The middle ring will show the month name (January-December).  And the inner ring will display the day of the week (Monday-Sunday).

Each ring has an internal gear that is rotated using a 28-byj48 stepper motor.  Magnets will be embedded in each ring triggers a Hall Effect sensor to insure proper positioning.

The perpetual calendar will be controlled using an ESP32 which periodically checks the date via NPT and rotates the rings to display it.