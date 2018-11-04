import paho.mqtt.client as mqtt
import random
from time import sleep

CHANNEL = 'whack/arm'

client = mqtt.Client('whack-switch')
client.connect('broker.hivemq.com')

def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))

client.on_message = on_message
client.loop_start()

client.subscribe(CHANNEL, qos=2)
sleep(1)

client.publish(CHANNEL, "Armed {}".format(random.randint(0,1000)), qos=1)

sleep(5)
client.loop_stop()
