from pyfirmata import Arduino, util
from time import sleep

# board = Arduino('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0') # Nano
board = Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55432333038351E0F022-if00') # Uno
print('Connected')

board.analog[0].enable_reporting()
it = util.Iterator(board)
it.start()
board.iterate()

LED_PIN = 13

servo = board.get_pin('d:3:s')
light = board.get_pin('a:0:i')
led = board.get_pin('d:13:o')

for i in range(100):
    print(light.read())
    led.write(i%2==0)
    servo.write(i)
    sleep(0.1)

board.exit()