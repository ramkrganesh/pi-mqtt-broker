import paho.mqtt.client as client
from dataclasses import dataclass, field
from json import loads

@dataclass
class MqttSubscriber:
    broker: str = "192.168.0.192"
    subscriber: client.Client = field(init=False)
    topic: str = 'steering_data'

    def __post_init__(self):
        self.subscriber = client.Client()
        self.subscriber.on_connect = self.on_connect
        self.subscriber.on_message = self.on_message
        self.subscriber.username_pw_set(username='pi_car',
                                        password='707070')
        self.subscriber.connect(host=self.broker)
        self.subscriber.loop_forever()
    #end def

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print("Unable to connect pi_car to the broker.")
        else:
            print("Connected pi_Car to the broker.")
            self.subscriber.subscribe(self.topic)
        #endif
    #end def

    def on_message(self,client, userdata, msg):
        steering_data = loads(msg.payload.decode("utf-8"))
        print(f"Received Steering Data- "
         f"T:{steering_data['throttle']:.2f}% "
         f"B:{steering_data['breaking']:.2f}% "
         f"SP:{'LEFT' if steering_data['steering_pos'] == 1 else 'RIGHT'} "
         f"SR:{steering_data['steering_rot']:.2f}\n"
         f"BTN_TRI:{'TRUE' if steering_data['btn_triangle'] else 'FALSE'} "
         f"BTN_CIR:{'TRUE' if steering_data['btn_circle'] else 'FALSE'} "
         f"BTN_X:{'TRUE' if steering_data['btn_x'] else 'FALSE'} "
         f"BTN_SQR:{'TRUE' if steering_data['btn_square'] else 'FALSE'} "
         f"PAD_R:{'TRUE' if steering_data['r_paddleshifter'] else 'FALSE'}"
         f"PAD_L:{'TRUE' if steering_data['l_paddleshifter'] else 'FALSE'}")

    def shutdown(self):
        self.subscriber.disconnect()

if __name__ == '__main__':
    try:
        subs = MqttSubscriber()
    except KeyboardInterrupt as e:
        subs.shutdown()