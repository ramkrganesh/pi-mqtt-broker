import paho.mqtt.client as client
from dataclasses import dataclass, field

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
