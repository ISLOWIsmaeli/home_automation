import paho.mqtt.client as mqtt
import time

MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
Keep_Alive_Interval = 45
SWITCH_TOPIC = "led/switch/+"
TOGGLE_FEEDBACK_TOPIC = "ledToggle/+"
TOGGLE_TOPIC = "led/toggle/+"

BASE_TOGGLE_PUBLISH_TOPIC = "led/toggle/room{}"
BASE_SWITCH_PUBLISH_TOPIC = "led/switch/room{}"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe(SWITCH_TOPIC, 0)
    mqttc.subscribe(TOGGLE_FEEDBACK_TOPIC, 0)
    mqttc.subscribe(TOGGLE_TOPIC,0)

def on_message(client, userdata, msg):
    print("Topic: " + str(msg.topic))
    print("Qos: " + str(msg.qos))
    print("Payload: " + str(msg.payload))
    print(msg.topic + " " + str(msg.payload))

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

def publish_to_toggle(room:str, times:str):
    mqttc.publish(BASE_TOGGLE_PUBLISH_TOPIC.format(room), times)
    print("toggle switching published")

def publish_to_switch(room:str, state:str):
    mqttc.publish(BASE_SWITCH_PUBLISH_TOPIC.format(room), state)
    print("switching on and off published")



