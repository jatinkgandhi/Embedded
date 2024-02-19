# Jatin Gandhi: Modified Afafruit code to plt data at runtime
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pip3 install hidapi
# pip3 install adafruit-blinka
# set BLINKA_MCP2221=1 : Windows or export BLINKA_MCP2221="1" : Mac/Linux
# Ref: https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221


# Force set :)
import os
os.environ["BLINKA_MCP2221"] = "1";


import board
import busio
import adafruit_mlx90640
# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


i2c = None;
mlx = None;
fig = plt.figure()

def init():
    global i2c;
    global mlx;
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    print("MLX addr detected on I2C")
    print([hex(i) for i in mlx.serial_number])
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

init();

frame = [0] * 768


def get_frame():
    try:
        mlx.getFrame(frame)
        fb = [];
        for h in range(24):
            row = [];
            for w in range(32):
                row.append(int(frame[h * 32 + w]));
            fb.append(row);
        return fb;
    except ValueError:
        # Its life ignore and move on!!!
        return list(); # return empty list
        pass;

colors = [
"#CC0000",
"#CC3300",
"#CC6600",
"#CC9900",
"#CCCC00",
"#CCFF00",
"#FF0000",
"#FF3300",
"#FF6600",
"#FF9900",
"#FFCC00",
"#FFFF00"
];

cmap = ListedColormap(colors);

im = plt.imshow(get_frame(), animated=True, cmap = cmap);

def updatefig(*args):
    im.set_array(get_frame())
    return im,

# TODO: FIXME:  UserWarning: frames=None which we can....,
ani = animation.FuncAnimation(fig, updatefig, frames=len(frame), interval=30, blit=True, repeat=True )
plt.show()
