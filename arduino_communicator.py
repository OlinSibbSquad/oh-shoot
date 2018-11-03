from pyfirmata import Arduino, util
from time import sleep

board = Arduino('/dev/ttyUSB2')
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