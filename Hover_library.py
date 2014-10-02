#  ===========================================================================
#  This is the library for Hover. 
#  
#  Hover is a development kit that lets you control your hardware projects in a whole new way.  
#  Wave goodbye to physical buttons. Hover detects hand movements in the air for touch-less interaction.  
#  It also features five touch-sensitive regions for even more options.
#  Hover uses I2C and 2 digital pins. It is compatible with Arduino, Raspberry Pi and more.
#
#  Hover can be purchased here: http://www.justhover.com
#
#  Written by Emran Mahbub and Jonathan Li for Gearseven Studios.  
#  BSD license, all text above must be included in any redistribution
#  ===========================================================================
#
#  INSTALLATION
#  Place the Hover_library.py file and the /gpio folder in the same directory as the Hover_example.py file.
#  Then run Hover_example.py by typing:  python Hover_example.py
#
#  SUPPORT
#  For questions and comments, email us at support@gearseven.com
#  ===========================================================================

import smbus
import time
import gpio as GPIO

#pcDuino3 uses smbus.SMBus(2)
bus = smbus.SMBus(2)   

dict = {'00100010':'Right Swipe', '00100100':'Left Swipe', '00101000':'Up Swipe', '00110000':'Down Swipe', '01001000':'East Tap', '01000001':'South Tap', '01000010':'West Tap', '01000100':'North Tap', '01010000':'Center Tap'}

class Hover(object):

  def __init__(self, address, ts, reset):
    print "Initializing Hover...please wait."
    self.address = address
    self.ts = ts
    self.reset = reset

    self.GPIO = GPIO

    self.GPIO.pinMode(self.ts, GPIO.INPUT)	#ts
    self.GPIO.pinMode(self.reset, GPIO.OUTPUT)	#mclr
    self.GPIO.digitalWrite(self.reset, GPIO.LOW)

    time.sleep(3)

    self.GPIO.digitalWrite(self.reset, GPIO.HIGH)
    self.GPIO.pinMode(self.reset, GPIO.INPUT)

    time.sleep(2)

    print "Hover is ready! To exit the program, hit Ctrl+C"


  def getStatus(self):
    if (self.GPIO.digitalRead(self.ts)):
       return 1
    else:
      self.GPIO.pinMode(self.ts, self.GPIO.OUTPUT)	#ts
      self.GPIO.digitalWrite(self.ts, self.GPIO.LOW)
      return 0

  def getEvent(self):

    busData = bus.read_i2c_block_data(self.address,0)
    gestureEvent = busData[10]
    touchEvent = (((busData[14] & 0b11100000) >> 5) | ((busData[15] & 0b00000011) << 3))

    if gestureEvent > 1:
      event = "{:08b}".format((1<<(busData[10]-1)) | 0b00100000)
      return event
    elif touchEvent > 0:
      event = "{:08b}".format(touchEvent | 0b01000000)
      return event


  def setRelease(self):

    self.GPIO.digitalWrite(self.ts, self.GPIO.HIGH)
    self.GPIO.pinMode(self.ts, self.GPIO.INPUT)	#ts


  def end(self):

    self.GPIO.cleanup()

  def getEventString(self, event):
    return dict[event]
    