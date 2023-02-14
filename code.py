# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# ON AIR sign
# Runs on Matrix Portal M4 with 64x65 RGB Matrix display & shield

import time
import board
import digitalio
import displayio
import framebufferio
import rgbmatrix
import adafruit_display_text.label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.polygon import Polygon
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

# setup buttons
b1 = digitalio.DigitalInOut(board.BUTTON_UP)
b1.switch_to_input(pull=digitalio.Pull.UP)
b2 = digitalio.DigitalInOut(board.BUTTON_DOWN)
b2.switch_to_input(pull=digitalio.Pull.UP)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Number of seconds between checking, if this is too quick the query quota will run out
UPDATE_DELAY = 300

# Times are in 24-hour format for simplification
OPERATING_TIME_START = "12:00"  # what hour to start checking
OPERATING_TIME_END = "19:00"  # what hour to stop checking

# --- Display setup ---
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD,
        board.MTX_ADDRE
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix)

#print("height=", display.height)
#print("width=", display.width)

# show network status on the neopixel
network = Network(status_neopixel=board.NEOPIXEL, debug=False)

# --- Drawing setup ---
# Create a Group
group = displayio.Group()
# Create a bitmap object
bitmap = displayio.Bitmap(64, 64, 2)  # width, height, bit depth
# Create a color palette
color = displayio.Palette(4)
color[0] = 0x000000  # black
color[1] = 0xFF0000  # red
color[2] = 0x444444  # dim white
color[3] = 0xDD8000  # gold
# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
# Add the TileGrid to the Group
group.append(tile_grid)


# draw the frame for startup
rect1 = Rect(0, 0, 2, 64, fill=color[2])
rect2 = Rect(62, 0, 2, 64, fill=color[2])
rect3 = Rect(2, 0, 9, 2, fill=color[2])
rect4 = Rect(53, 0, 9, 2, fill=color[2])
rect5 = Rect(2, 62, 12, 2, fill=color[2])
rect6 = Rect(50, 62, 12, 2, fill=color[2])

group.append(rect1)
group.append(rect2)
group.append(rect3)
group.append(rect4)
group.append(rect5)
group.append(rect6)


def redraw_frame():  # to adjust spacing at bottom later
    rect3.fill = color[2]
    rect4.fill = color[2]
    rect5.fill = color[2]
    rect6.fill = color[2]


# draw the wings w polygon shapes
# offset the wings for a larger panel
w_x = 0
w_y = 16

wing_polys = []

wing_polys.append(Polygon([(3, 3 + w_y), (9, 3 + w_y), (9, 4 + w_y), (4, 4 + w_y)], outline=color[1]))
wing_polys.append(Polygon([(5, 6 + w_y), (9, 6 + w_y), (9, 7 + w_y), (6, 7 + w_y)], outline=color[1]))
wing_polys.append(Polygon([(7, 9 + w_y), (9, 9 + w_y), (9, 10 + w_y), (8, 10 + w_y)], outline=color[1]))
wing_polys.append(Polygon([(54, 3 + w_y), (60, 3 + w_y), (59, 4 + w_y), (54, 4 + w_y)], outline=color[1]))
wing_polys.append(Polygon([(54, 6 + w_y), (58, 6 + w_y), (57, 7 + w_y), (54, 7 + w_y)], outline=color[1]))
wing_polys.append(Polygon([(54, 9 + w_y), (56, 9 + w_y), (55, 10 + w_y), (54, 10 + w_y)], outline=color[1]))

for wing_poly in wing_polys:
    group.append(wing_poly)


def redraw_wings(index):  # to change colors
    for wing in wing_polys:
        wing.outline = color[index]



# --- Content Setup ---
deco_font = bitmap_font.load_font("/fonts/BellotaText-Bold-21.bdf")

# Create two lines of text. Besides changing the text, you can also
# customize the color and font (using Adafruit_CircuitPython_Bitmap_Font).

# text positions
on_x = 15
off_x = 12

on_y = 25
off_y = 25

air_x = 15
air_y = 45


text_line1 = adafruit_display_text.label.Label(deco_font, color=color[3], text="OFF")
text_line1.x = off_x
text_line1.y = off_y

text_line2 = adafruit_display_text.label.Label(deco_font, color=color[1], text="AIR")
text_line2.x = air_x
text_line2.y = air_y

# Put each line of text into the Group
group.append(text_line1)
group.append(text_line2)


def startup_text():
    text_line1.text = "Stella"
    text_line1.x = 8
    text_line1.y = 16
    text_line1.color = color[2]
    text_line2.text = "Star"
    text_line2.x = 12
    text_line2.y = 42
    text_line2.color = color[2]
    redraw_wings(0)
    display.show(group)
    time.sleep(2)


startup_text()  # display the startup text


def update_text(state):
    if state:  # if switch is on, text is "ON" at startup
        text_line1.text = "ON"
        text_line1.x = on_x
        text_line1.y = on_y
        text_line1.color = color[1]
        text_line2.text = "AIR"
        text_line2.x = air_x
        text_line2.y = air_y
        text_line2.color = color[1]
        redraw_wings(1)
        redraw_frame()
        display.show(group)
    else:  # else, text if "OFF" at startup
        text_line1.text = "OFF"
        text_line1.x = off_x
        text_line1.y = off_y
        text_line1.color = color[3]
        text_line2.text = "AIR"
        text_line2.x = air_x
        text_line2.y = air_y
        text_line2.color = color[3]
        redraw_wings(3)
        redraw_frame()
        display.show(group)


def get_status():
    """
    Get the status whether we are on/off air within operating hours
    If outside of hours, return False
    """
    # Get the time values we need
    now = time.localtime()
    start_hour, start_minute = OPERATING_TIME_START.split(":")
    end_hour, end_minute = OPERATING_TIME_END.split(":")

    # Convert time into a float for easy calculations
    start_time = int(start_hour) + (int(start_minute) / 60)
    end_time = int(end_hour) + (int(end_minute) / 60)
    current_time = now[3] + (now[4] / 60)

    if start_time <= current_time < end_time:
        try:
            return True
        except RuntimeError:
            return False


    return False


# start off air
mode_state = 0
#update_text(mode_state)

while True:

    # change with buttons
    if not b1.value:
        if mode_state:
            mode_state = 0
            time.sleep(.5)
        else:
            mode_state = 1
            time.sleep(.5)

    update_text(mode_state)






