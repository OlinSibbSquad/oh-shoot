from pyfirmata import Arduino, util
board = Arduino('/dev/ttyUSB0')
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[0].read()
