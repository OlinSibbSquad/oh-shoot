import paho.mqtt.client as mqtt
import random
from time import sleep

class Communicator(object):
    def __init__(self):
        self._channel = 'arming'
        self._client = mqtt.Client('whack-{}'.format(random.randint(0, 100000)))
        self.is_armed = True
        self.last_msg = None

        self._client.on_message = self._on_message
        self._client.username_pw_set('yctweqrz', '7exM74SXFRjX')
        self._client.connect("m15.cloudmqtt.com", 16481)
        sleep(1.0)
        self._client.subscribe(self._channel)

        self._client.loop_start()

        self._i = 0


    def _on_message(self, client, userdata, message):
        msg = str(message.payload.decode('utf-8'))
        self.last_msg = msg
        print("Message on MQTT", msg)
        if 'Armed' in msg:
            self.is_armed = True
        elif 'Disarmed' in msg:
            self.is_armed = False
        else:
            print("Unable to decipher message")

    def send_message(self, switch_on:bool, people_present:bool):
        msg = "{} {}".format('Armed' if (switch_on and people_present) else 'Disarmed', self._i)
        self._i += 1
        self._client.publish(self._channel, msg, qos=1)

if __name__ == '__main__':
    com = Communicator()

    import sys
    if sys.argv[1] == 'subscribe':
        print('subscribing')
        while True:
            print(com.is_armed, com.last_msg)
            sleep(1)
    else:
        print('publishing')
        while True:
            com.send_message(True, True)
            sleep(2)
            com.send_message(False, False)
            sleep(2)
