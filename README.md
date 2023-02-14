# stella-onair

This is circuitpython code for an adafruit Matrixportal M4 to drive a 64x64 rgb matrix with a graphical On Air Off Air sign for Stella. Button presses will toggle the display.

This is meant to be mounted behind a 10x10 canvas and put up on a wall or door to prevent interruptions. (like at https://learn.adafruit.com/use-an-art-canvas-to-diffuse-RGB-matrix/64x64-pixel-3mm-pitch)

Future work can be a remote trigger button soldered and triggered on A1:
Pinouts for the board are at https://learn.adafruit.com/adafruit-matrixportal-m4/pinouts

```
#  setup for external button
e_button = DigitalInOut(board.A1)
e_button = Direction.INPUT
e_button.pull = Pull.UP
```


or alexa integration by chaining through IFTTT with adafruit.io:
https://www.reddit.com/r/raspberry_pi/comments/5p1p35/short_guide_on_using_adafruitio_and_ifttt_with/
```
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_USERNAME = "yourusername"
ADAFRUIT_IO_KEY = "youraiokey"

def connected(client):
    client.subscribe('ifttt') # or change to whatever name you used

# this gets called every time a message is received
def message(client, feed_id, payload):
     if payload == "test":
        print "Message test received from IFTTT."
     else:
        print "Message from IFTTT: %s" % payload

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_message    = message

client.connect()

client.loop_blocking() # block forever on client loop
```


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
