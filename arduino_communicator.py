from pyfirmata import Arduino, util
from time import sleep

# board = Arduino('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0') # Nano
board = Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55432333038351E0F022-if00') # Uno
print('Connected')

board.analog[0].enable_reporting()

LED_PIN = 13

for i in range(10):
    board.iterate()
    print(board.analog[0].read())
    board.digital[LED_PIN].write(i%2==0)
    sleep(0.5)