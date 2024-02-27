import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import serial;
import binascii;

debug_frame = False;

fig = plt.figure()

serial_port = None;

def init():
    global serial_port;
    try:
        serial_port = serial.Serial('COM12', 921600);
        serial_port.reset_input_buffer();
        serial_port.reset_output_buffer();
        serial_port.flush();
    except:
        print('Failed to open the serial port');
        exit(0);

init();

frame: float = [0] * 768


def get_frame():
    global serial_port;
    try:
        frame = serial_port.read( 32 * 24 * 4);
        # Debug print
        if None != frame and len(frame) > 0 and True == debug_frame :
            print(binascii.hexlify(frame));
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
"#FF8674",
"#FA8072",
"#F98B88",
"#F08080",
"#F67280",
"#E77471",
"#F75D59",
"#E55451",
"#CD5C5C",
"#FF6347",
"#E55B3C",
"#FF4500",
"#FF0000",
"#FD1C03",
"#FF2400",
"#F62217",
"#F70D1A",
"#F62817",
"#E42217",
"#E41B17",
];

cmap = ListedColormap(colors);

im = plt.imshow(get_frame(), animated=True, cmap = cmap, interpolation='gaussian');

def updatefig(*args):
    im.set_array(get_frame())
    return im,

# TODO: FIXME:  UserWarning: frames=None which we can....,
ani = animation.FuncAnimation(fig, updatefig, frames=len(frame), interval=30, blit=True, repeat=True )
plt.show()

"""
Board: Nano ESP32 (Official Arduino Board)
Firmware Code:

#include <Adafruit_MLX90640.h>

Adafruit_MLX90640 mlx;
float frame[32*24]; // buffer for full frame of temperatures

#define FRAMERATE MLX90640_2_HZ

#define SCANMODE MLX90640_CHESS
// MLX90640_CHESS or MLX90640_INTERLEAVED


void setup() {
  while (!Serial) delay(10);
  Serial.begin(921600);
  delay(100);

  if (! mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire)) {
    Serial.println("MLX90640 not found!");
    while (1) delay(10);
  }
  mlx.setMode(SCANMODE);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(FRAMERATE);
}

void loop() {
  delay(50);
  memset(frame, 0, sizeof(frame));
  if (mlx.getFrame(frame) != 0) {
    Serial.println("Failed");
    return;
  }else {
    Serial.write((const uint8_t *)frame, sizeof(frame));
    Serial.flush();
  }
}
"""
