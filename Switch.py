from pyfirmata import Arduino, util
from time import sleep

board = Arduino('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0') # Nano
#board = Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55432333038351E0F022-if00') # Uno
print('Connected')


value = board.get_pin('d:4:i')

it = util.Iterator(board)
it.start()
board.iterate()
# value.enable_reporting()

value.

while True:
    input = value.read()
    if input == True:
        print('Switch is High')
    else:
        print('Switch is Low')
# for i in range (1000):
#     print('Switch State: %s')% value.read()
#     if str(value.read()) == 'True':
#         print('High')
#     if str(value.read()) == 'False':
#         print('Low')
#print(value.read())
    # if(dig_pin.read()== 1):
    #     print('High')
    # if (dig_pin.read()== 0):
    #     print('Low')

board.exit()