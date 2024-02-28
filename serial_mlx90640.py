import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import serial;
import binascii;

debug_frame = False;

fig = plt.figure()

serial_port = None;
baud_rate   = 2000000;
# baud_rate   = 921600;
def init():
    global serial_port;
    try:
        serial_port = serial.Serial('COM12', baud_rate);
        print("Sending ""start"" to controller");
        serial_port.write("start".encode());
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
        print("Max Temp = {}".format(max(frame)));
        fb = [];
        if None == frame or len(frame) <= 0:
            return fb;

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
"#000000",
"#040720",
"#0C090A",
"#34282C",
"#3B3131",
"#3A3B3C",
"#454545",
"#4D4D4F",
"#413839",
"#3D3C3A",
"#463E3F",
"#4C4646",
"#504A4B",
"#565051",
"#52595D",
"#5C5858",
"#625D5D",
"#666362",
"#696969",
"#686A6C",
"#6D6968",
# "#726E6D",
# "#736F6E",
# "#757575",
# "#797979",
# "#837E7C",
# "#808080",
# "#848482",
# "#888B90",
# "#8C8C8C",
# "#8D918D",
# "#9B9A96",
# "#99A3A3",
# "#A9A9A9",
# "#A8A9AD",
# "#B6B6B4",
# "#B6B6B6",
# "#C0C0C0",
# "#C9C1C1",
# "#C9C0BB",
# "#C0C6C7",
# "#D1D0CE",
# "#CECECE",
# "#D3D3D3",
# "#DADBDD",
# "#DCDCDC",
# "#E0E5E5",
# "#F5F5F5",
# "#EEEEEE",
# "#E5E4E2"
];

colors.reverse();

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
float frame[32*24];

#define FRAMERATE MLX90640_8_HZ
#define SCANMODE MLX90640_CHESS

// #define BAUD_RATE 921600
#define BAUD_RATE 2000000
// MLX90640_CHESS or MLX90640_INTERLEAVED

void setup() {
  while (!Serial) delay(10);
  Serial.begin(BAUD_RATE);
  delay(100);

  while (! mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire)) {
    Serial.println("MLX90640 not found retrying in 1 seconds!");
    delay(1000);
  }
  mlx.setMode(SCANMODE);

  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(FRAMERATE);
  Serial.println("Waiting for UI to send start");
  String goahead = "";
  goahead = Serial.readString();
  while(false == goahead.startsWith("start"))
  {
    goahead = Serial.readString();
  }

  Wire.setClock(1000000); // max 1 MHz

}

// #define DEBUG_FRAME_TIME

void loop() {
#ifdef DEBUG_FRAME_TIME
  uint32_t before;
#endif  
  memset(frame, 0, sizeof(frame));
#ifdef DEBUG_FRAME_TIME
  before = millis();
#endif
  if (mlx.getFrame(frame) != 0) {
    Serial.println("Failed");
    return;
  }
  else
  {
#ifdef DEBUG_FRAME_TIME
    Serial.print((millis()-before) / 2); Serial.println(" ms per frame (2 frames per display)");
#endif
    for (uint8_t h=0; h<24; h++) {
      for (uint8_t w=0; w<32; w++) {
        Serial.write(uint8_t(int(frame[h*32 + w])));
      }
    }
    Serial.flush();
  }
}

"""
