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
trigtime = 0.6
triggered_angle = 40
default_angle = 100
servo = board.get_pin('d:3:s')
light = board.get_pin('a:0:i')
led = board.get_pin('d:13:o')

for i in range(1000):
    servo.write(default_angle)
    led.write(False)
    print(light.read())
    #servo.write(i)
    sleep(0.01)
    if(light.read()) < 0.4:
        servo.write(triggered_angle)
        led.write(True)
        sleep(trigtime)
        servo.write(default_angle)
        led.write(False)
        while(light.read())<0.4:
            sleep(0.1)
            # if(light.read())>= 0.4:
            #     break

board.exit()


