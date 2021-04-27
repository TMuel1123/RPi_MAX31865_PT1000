# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
# Simple demo of the MAX31865 thermocouple amplifier.
# Will print the temperature every second.
import time
 
import socket
import fcntl
import struct
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_max31865
import adafruit_ssd1306

# Initialize SPI bus and sensor.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs1 = digitalio.DigitalInOut(board.D7)  # Chip select of the MAX31865 board.
cs2 = digitalio.DigitalInOut(board.D22)  # Chip select of the MAX31865 board.
#sensor = adafruit_max31865.MAX31865(spi, cs)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
sensor1 = adafruit_max31865.MAX31865(spi, cs1, rtd_nominal=1000, ref_resistor=4220.0, wires=4)
sensor2 = adafruit_max31865.MAX31865(spi, cs2, rtd_nominal=1000, ref_resistor=4220.0, wires=4)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)#, reset=RESET_PIN)

# set up inputs
in24 = digitalio.DigitalInOut(board.D24)
in24.direction = digitalio.Direction.INPUT
in24.pull = digitalio.Pull.UP

in25 = digitalio.DigitalInOut(board.D25)
in25.direction = digitalio.Direction.INPUT
in25.pull = digitalio.Pull.UP

# set up outputs
out18 = digitalio.DigitalInOut(board.D18)
out18.direction = digitalio.Direction.OUTPUT

out4 = digitalio.DigitalInOut(board.D4)
out4.direction = digitalio.Direction.OUTPUT


# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)


FileTimeStamp = "none"
InitDone = False

# Main loop to print the temperature every second.
while True:

  # Read temperature.
  temp1 = sensor1.temperature
  temp2 = sensor2.temperature

  # Print the value.
  string1 = "Temperature: {:.1f}C {:.1f}C"
  #print(string1.format(temp1, temp2))
  #print("Temperature: {:.1f}C {:.1f}C".format(temp1, temp2))

  #TEXT = "Hallo"
  TEXT = "{:.1f}°C"

  # Draw a black background
  draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

  # Draw the text
  draw.text((5, 0),  TEXT.format(temp1), font=font, fill=255)
  draw.text((5, 30), TEXT.format(temp2), font=font, fill=255)

  # Display image
  oled.image(image)
  oled.show()

  if not in24.value:
  
    if not InitDone: # get the timestamp for the filename
      secondsSinceEpoch = time.time()
            # Convert seconds since epoch to struct_time
      timeObj = time.localtime(secondsSinceEpoch)
      FileTimeStamp = ('%d-%d-%d_%d-%d-%d' % (timeObj.tm_year, timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))
      
      print("Start Temperature Log " + FileTimeStamp)
      
      InitDone = True


    # set LEDs
    out4.value = True
    out18.value = False

    secondsSinceEpoch = time.time()
    
    # Convert seconds since epoch to struct_time
    timeObj = time.localtime(secondsSinceEpoch)
    TimeStamp = ('%d-%d-%d_%d-%d-%d' % (timeObj.tm_year, timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))
    #print (TimeStamp)

    LogString = "{:.2f}; {:.2f}; \n"

    # Write values to a log file
    f = open("/home/pi/templog/templog_" + FileTimeStamp + ".csv", "a") # -a- Append - will create a file if the specified file does not exist
    # get the current timestamp elements from struct_time object i.e.
    f.write(TimeStamp + "; ")
    f.write(LogString.format(temp1, temp2))
    f.close()


  elif not in25.value:
    # set LEDs
    out4.value = False
    out18.value = True
    
    InitDone = False

  # Delay for a second.
  time.sleep(1.0)












