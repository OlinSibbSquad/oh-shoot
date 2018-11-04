from pyfirmata import Arduino, util
import pyfirmata
from time import sleep

from mqtt_lib import Communicator

board = Arduino('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0') # Nano
#board = Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55432333038351E0F022-if00') # Uno
print('Connected')


value = board.get_pin('d:4:i')  # type: pyfirmata.Pin

it = util.Iterator(board)
it.start()
board.iterate()

PIN_MODE_PULLUP = 0x0B

msg = bytearray([pyfirmata.SET_PIN_MODE, value.pin_number, PIN_MODE_PULLUP])
value.board.sp.write(msg)

c = Communicator()

while True:
    input = value.read()
    if input == True:
        print('Switch is High')
        c.send_message(True, True)
    else:
        print('Switch is Low')
        c.send_message(False, False)
    sleep(0.1)
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