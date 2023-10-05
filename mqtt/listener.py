import paho.mqtt.client as mqtt

LED_TOGGLE_STATUS = {}
LED_SWITCH_STATUS = {}
MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
Keep_Alive_Interval = 45
SWITCH_TOPIC = "led/switch/+"
TOGGLE_TOPIC = "led/toggle/+"

TOGGLE_FEEDBACK_TOPIC = "ledToggle/+"
SWITCH_FEEDBACK_TOPIC = "ledSwitch/+"

BASE_TOGGLE_PUBLISH_TOPIC = "led/toggle/room{}"
BASE_SWITCH_PUBLISH_TOPIC = "led/switch/room{}"

START_TOGGLE_STATUS = "starting to toggle"
END_TOGGLE_STATUS = "finished/not toggling"

SWITCH_ON = "ON"
SWITCH_OFF = "OFF"

TOGGLE_CODE_STATUS_MAP = {
    "1": START_TOGGLE_STATUS,
    "0": END_TOGGLE_STATUS,
    END_TOGGLE_STATUS: END_TOGGLE_STATUS,
    START_TOGGLE_STATUS: START_TOGGLE_STATUS,
}

SWITCH_CODE_STATUS_MAP = {
    "1": SWITCH_ON,
    "0": SWITCH_OFF,
    SWITCH_ON: SWITCH_ON,
    SWITCH_OFF: SWITCH_OFF,
}


def decode_toggle_led_feedback(led_status: dict):
    for room, status in led_status.items():
        decoded_status = TOGGLE_CODE_STATUS_MAP.get(status)
        led_status[room] = decoded_status
    return led_status


# the following function is not working as expected thus it has been hardcoded in the javascript on front end
def decode_switch_led_feedback(led_status: dict):
    for room, status in led_status.items():
        decoded_status = SWITCH_CODE_STATUS_MAP.get(status)
        led_status[room] = decoded_status
        return led_status


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe(SWITCH_FEEDBACK_TOPIC, 0)
    mqttc.subscribe(SWITCH_TOPIC, 0)
    mqttc.subscribe(TOGGLE_FEEDBACK_TOPIC, 0)
    mqttc.subscribe(TOGGLE_TOPIC, 0)
    # this is upon re-connection not first time connection
    for room, status in LED_TOGGLE_STATUS.items():
        mqttc.publish(BASE_TOGGLE_PUBLISH_TOPIC.format(room), status)
    for room, status in LED_SWITCH_STATUS.items():
        mqttc.publish(BASE_SWITCH_PUBLISH_TOPIC.format(room), status)


def on_message(client, userdata, msg):
    print("Topic: " + str(msg.topic))
    print("Qos: " + str(msg.qos))
    print("Payload: " + str(msg.payload))
    print(msg.topic + " " + str(msg.payload))
    if msg.topic.startswith("ledToggle/"):
        payload = msg.payload.decode("utf-8")
        room = payload[:-1]
        status = payload[-1]
        LED_TOGGLE_STATUS[room] = status
        print(f"Toggle status: {LED_TOGGLE_STATUS}")
        print("Payload in if: " + str(msg.payload))
    elif msg.topic.startswith("ledSwitch/"):
        payload = msg.payload.decode("utf-8")
        room = payload[:-1]
        status = payload[-1]
        LED_SWITCH_STATUS[room] = status
        print("Payload in elif: " + str(msg.payload))


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
    mqttc.publish(BASE_TOGGLE_PUBLISH_TOPIC.format(room), times)


def publish_to_switch(room: str, state: str):
    mqttc.publish(BASE_SWITCH_PUBLISH_TOPIC.format(room), state)
