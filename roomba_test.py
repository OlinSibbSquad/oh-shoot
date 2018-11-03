from pycreate2 import Create2
from time import sleep

bot = Create2('/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN026EMT-if00-port0')

bot.start()

bot.full()

sensors = bot.get_sensors()

print(sensors)
print(sensors.battery_charge, sensors.battery_capacity)

bot.drive_distance(-.5, speed=40, stop=True)

# bot.drive_turn(40, 1)
# sleep(2)
#
# bot.drive_turn(40, -1)
# sleep(2)

# bot.turn_angle(70, speed=40)

bot.stop()