# stella-onair

This is circuitpython code for an adafruit Matrixportal M4 to drive a 64x64 rgb matrix with a graphical On Air Off Air sign for Stella. Button presses will toggle the display.

This is meant to be mounted behind a 10x10 canvas and put up on a wall or door to prevent interruptions. (like at https://learn.adafruit.com/use-an-art-canvas-to-diffuse-RGB-matrix/64x64-pixel-3mm-pitch)

Future work can be a remote trigger button or alexa integration to activate.

Pinouts for the board are at https://learn.adafruit.com/adafruit-matrixportal-m4/pinouts

This ran succesfully with 
adafruit-circuitpython-matrixportal_m4-en_US-8.0.0.uf2
adafruit-circuitpython-bundle-8.x-mpy-20230214

Other files on the board:
Need to grab BellotaText-Bold-21.bdf and put it in /fonts/
Need to have the adfruit modules in /lib:
- adafruit_bitmap_font
- adafruit_display_shapes
- adafruit_display_text
- adafruit_fakerequests
- adafruit_io
- adafruit_matrixportal
- adafruit_minimqtt
- adafruit_portalbase
