import paho.mqtt.client as client
from dataclasses import dataclass, field
from random import randrange
from json import dumps

@dataclass
class MqttSteeringBroker:
    broker: str = 'localhost'
    pi_client: client.Client = field(init=False)
    topic:str = 'steering_data'

    def __post_init__(self):
        self.pi_client = client.Client()
        self.pi_client.username_pw_set(username='pi_steering',
                                       password='707070')
        self.pi_client.on_connect = MqttSteeringBroker.on_connect
        self.pi_client.connect(host=self.broker)
        self.pi_client.loop_start()
    #end def

    @staticmethod
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print("pi_steering is Unable to connect to MQTT broker.")
        else:
            print("pi_steering is connected to MQTT broker.")
    #end def

    def mqtt_publish(self, msg:str):
        pub = self.pi_client.publish(topic=self.topic, payload=msg)
        pub.wait_for_publish(timeout=2.0)  # blocking call

    def mqtt_shutdown(self):
        self.pi_client.loop_stop()
        self.pi_client.disconnect()

if __name__ == '__main__':
    mqtt_pub = MqttSteeringBroker()
    try:
        while True:
            steering_data = {
                "throttle": randrange(1,100) / 1.1,
                "breaking": randrange(1,100) / 1.1,
                "steering_pos": randrange(1,3),
                "steering_rot": randrange(1,100) / 1.1,
                "btn_triangle": randrange(0,2),
                "btn_circle": randrange(0,2),
                "btn_x": randrange(0,2),
                "btn_square": randrange(0, 2),
                "r_paddleshifter": randrange(0,2),
                "l_paddleshifter": randrange(0,2)
            }
            msg = dumps(steering_data)
            mqtt_pub.mqtt_publish(msg=msg)
    except KeyboardInterrupt as e:
        mqtt_pub.mqtt_shutdown()
    #end try
