from pyfirmata import Arduino, util
from time import sleep

board = Arduino('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0')
print('Connected')

board.analog[0].enable_reporting()

it = util.Iterator(board)
it.start()
board.iterate()

print(board.analog[0].read())

LED_PIN = 13

for i in range(10):
    board.digital[LED_PIN].write(i%2==0)
    sleep(1)