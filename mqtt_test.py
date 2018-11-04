import paho.mqtt.client as mqtt
import random
from time import sleep

CHANNEL = 'whack/switcharm'

client = mqtt.Client('whack-switch-{}'.format(random.randint(0, 1000)))
# client.connect('broker.hivemq.com')

def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))

# def on_connect(client, userdata, rc):
#     print('Connected')
#     client.subscribe(CHANNEL)

client.on_message = on_message
# client.on_connect = on_connect

client.username_pw_set('yctweqrz', '7exM74SXFRjX')
# client.connect("broker.hivemq.com")
client.connect("m15.cloudmqtt.com", 16481)

sleep(1)
client.subscribe(CHANNEL)

import sys
if len(sys.argv)>1 and sys.argv[1] == 'subscribe':
    print('subscribing')
    client.loop_forever()
else:
    print('publishing')
    msg = "Armed {}".format(random.randint(0,1000))
    print(msg)
    client.publish(CHANNEL, msg, qos=1)

    client.loop_start()
    sleep(2)
    client.loop_stop()