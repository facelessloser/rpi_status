#!/usr/bin/python
#!/usr/bin/env

import urllib2, json, os

# ---- BMP180 stuff ----
import Adafruit_BMP.BMP085 as BMP085
sensor = BMP085.BMP085()

# ---- ws2812 stuff ----
import time
from neopixel import *

# LED strip configuration:
LED_COUNT = 8 # Number of LED pixels.
LED_PIN = 12 # GPIO pin connected to the pixels (must support PWM!) 
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127 # Set to 0 for darkest and 255 for brightest
#LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()
# ---- ws2812 stuff ----


# ---- Screen stuff ----

import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
  
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
# ---- Screen stuff ----

class basicWeather(object):

    def __init__(self):
        #self.chesterWeather = 'http://api.wunderground.com/api/ADDKEYHERE/geolookup/conditions/q/UK/%s.json' % 'chester'
        self.chesterWeather = 'http://api.wunderground.com/api/080b28233d8a1a49/geolookup/conditions/q/UK/%s.json' % 'chester'

    def run(self):
        self.chesterRead()

    def chesterRead(self):
        ledNumber = 0
        f = urllib2.urlopen(self.chesterWeather)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        temp_c = parsed_json['current_observation']['temp_c']
        feels = parsed_json['current_observation']['feelslike_c']
        weather = parsed_json['current_observation']['weather']
        wind = parsed_json['current_observation']['wind_mph']
        wind_dir = parsed_json['current_observation']['wind_dir']
        rain = parsed_json['current_observation']['precip_1hr_metric']
        f.close()

#        print "----------------------------------"
#        print "Weather in %s" % location
#        print "----------------------------------"
#        print "Current weather - %s" % weather
#        print "Temp - %sC" % temp_c
#        print "Feels like - %sC" % feels
#        print "rain this hour - %s Cm" % rain
#        print "----------------------------------"
#        print "Chester wind"
#        print "----------------------------------"
#        print "wind - %s Mph" % wind
#        print "wind direction - %s " % wind_dir
#        print "----------------------------------"
#        print "Inside temp - %0.1fC" % sensor.read_temperature()
#        print "----------------------------------"
#        print "\n"

#        draw.text((0, 0),"Weather in %s" % location,  font=font, fill=255)
        draw.text((0, 0), "%s" % weather, font=font, fill=255)
        draw.text((0, 10), "Temp - %sC" % temp_c, font=font, fill=255)
        draw.text((0, 20), "Feels like - %sC" % feels, font=font, fill=255)
        draw.text((0, 30), "Inside temp - %0.1fC" % sensor.read_temperature(), font=font, fill=255)
        draw.text((0, 40), "wind - %s Mph %s" % (wind,wind_dir), font=font, fill=255)
        draw.text((0, 50), "Rain this hour -%sCM" % (rain), font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()

        if temp_c < 0:
            strip.setPixelColorRGB(0,0,0,255) # Blue    
            strip.show()

        elif 0.1 < temp_c <= 10:
        
            mappedTemp = temp_c / 1.25 
            print "Number of led's %d " % int(mappedTemp)
            
            while (ledNumber <= int(mappedTemp)):
                print ledNumber
                strip.setPixelColorRGB(ledNumber,0,255,255) # Aqua    
                ledNumber = ledNumber + 1
                strip.show()

        elif 10.1 < temp_c <= 20:
        
            convert_temp_c = temp_c - 10        
            mappedTemp = convert_temp_c / 1.25 
            print "Number of led's %d " % int(mappedTemp)
            
            while (ledNumber <= int(mappedTemp)):
                strip.setPixelColorRGB(ledNumber,255,255,0) # Yellow   
                ledNumber = ledNumber + 1
                strip.show()

        elif 20.1 < temp_c <= 30:
            convert_temp_c = temp_c - 20        
            mappedTemp = convert_temp_c / 1.25 
            print "Number of led's %d " % int(mappedTemp)
            
            while (ledNumber < int(mappedTemp)):
                strip.setPixelColorRGB(ledNumber,127,255,0) # orange   
#                strip.setPixelColorRGB(ledNumber,0,255,0) # red    
                ledNumber = ledNumber + 1
                strip.show()

        elif 30.1 < temp_c <= 40:
            convert_temp_c = temp_c -30        
            mappedTemp = convert_temp_c / 1.25 
            print "Number of led's %d " % int(mappedTemp)
            
            while (ledNumber < int(mappedTemp)):
                strip.setPixelColorRGB(ledNumber,0,255,0) # red    
                ledNumber = ledNumber + 1
                strip.show()

if __name__ == '__main__':
    start = basicWeather()
    start.run()
