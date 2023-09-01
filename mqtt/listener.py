import paho.mqtt.client as mqtt
import time

MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "led/switch/+"
MQTT_Topic1 = "ledToggle/+"
MQTT_Topic2 = "led/toggle/+"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe(MQTT_Topic, 0)
    mqttc.subscribe(MQTT_Topic1, 0)
    mqttc.subscribe(MQTT_Topic2,0)

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

mqttc.publish("led/toggle/room1", "7")
mqttc.publish("led/toggle/room2", "7")
mqttc.publish("led/switch/room1","1")
time.sleep(20)
mqttc.publish("led/switch/room2","1")
time.sleep(5)
mqttc.publish("led/switch/room1","0")
time.sleep(5)
mqttc.publish("led/switch/room2","0")
mqttc.on_publish = on_publish
time.sleep(60)  # Keep the loop running for 60 seconds
