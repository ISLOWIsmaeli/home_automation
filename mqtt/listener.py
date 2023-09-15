import paho.mqtt.client as mqtt
import time

LED_STATUS = {}
TOGGLE_REQUESTED_ROOMS = set()
MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
Keep_Alive_Interval = 45
SWITCH_TOPIC = "led/switch/+"
TOGGLE_FEEDBACK_TOPIC = "ledToggle/+"
TOGGLE_TOPIC = "led/toggle/+"

BASE_TOGGLE_PUBLISH_TOPIC = "led/toggle/room{}"
BASE_SWITCH_PUBLISH_TOPIC = "led/switch/room{}"

START_TOGGLE_STATUS = "starting to toggle"
END_TOGGLE_STATUS = "finished toggling"

TOGGLE_CODE_STATUS_MAP = {
    "1": START_TOGGLE_STATUS,
    "0": END_TOGGLE_STATUS,
    END_TOGGLE_STATUS: END_TOGGLE_STATUS,
    START_TOGGLE_STATUS: START_TOGGLE_STATUS,
}


def decode_toggle_led_feedback(led_status: dict):
    for room, status in led_status.items():
        decoded_status = TOGGLE_CODE_STATUS_MAP.get(status)
        led_status[room] = decoded_status
        print(f"I am the returned led_status{led_status}")
    return led_status


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe(SWITCH_TOPIC, 0)
    mqttc.subscribe(TOGGLE_FEEDBACK_TOPIC, 0)
    mqttc.subscribe(TOGGLE_TOPIC, 0)


def on_message(client, userdata, msg):
    print("Topic: " + str(msg.topic))
    print("Qos: " + str(msg.qos))
    print("Payload: " + str(msg.payload))
    print(msg.topic + " " + str(msg.payload))
    if msg.topic.startswith("ledToggle/"):
        payload = msg.payload.decode("utf-8")
        room = payload[:-1]
        status = payload[-1]
        LED_STATUS[room] = status
        print(LED_STATUS)
        print("Payload in if: " + str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to Topic: ")


def on_publish(client, userdata, mid):
    print("Message published....")


# Initiate MQTT client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_publish = on_publish

mqttc.username_pw_set("Lennox", password="password")
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# a comment
mqttc.loop_start()


def publish_to_toggle(room: str, times: str):
    TOGGLE_REQUESTED_ROOMS.add(room)
    mqttc.publish(BASE_TOGGLE_PUBLISH_TOPIC.format(room), times)


def publish_to_switch(room: str, state: str):
    mqttc.publish(BASE_SWITCH_PUBLISH_TOPIC.format(room), state)
