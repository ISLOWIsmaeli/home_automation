#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const int ledPin[]={D0,D1,D2,D3,D4,D5,D6};
const int delayTime=500;

const char *ssid = "Kembo Home"; 
const char *password = "KemboHome"; 

const char *mqttBroker = "broker.hivemq.com";

const char *switchTopic = "led/switch/+";
const char *baseSwitchTopic = "led/switch/";

const char *toggleTopic = "led/toggle/+";
const char *baseToggleTopic = "led/toggle/";

const char *toggleFeedbackTopic="ledToggle/feedback";
const char *switchFeedbackTopic="ledSwitch/feedback";

const char *mqttUsername = "Lennox";
const char *mqttPassword = "password";
const int mqttPort = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  for(int i=0;i<(sizeof(ledPin)/sizeof(ledPin[0]));i++){
    pinMode(ledPin[i],OUTPUT);
 }
  
  Serial.begin(9600);
  
  WiFi.begin(ssid,password);
  Serial.print("Connecting WiFi");
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to the WiFi network");
  

  client.setServer(mqttBroker,mqttPort);
  client.setCallback(callback);
  
  reconnectBroker();
  
  client.subscribe(switchTopic);
  client.subscribe(toggleTopic);
  client.subscribe(toggleFeedbackTopic);
  client.subscribe(switchFeedbackTopic);
  }
 
void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    String message; 
    for (int i = 0; i < length; i++) {
        message += (char) payload[i]; 
    }
    
    Serial.println(message);
    
    if((String(topic) == (String (baseSwitchTopic)+="room1"))){
      switchPublishLedFeedback(1,message.toInt());
    }else if ((String(topic) == (String (baseSwitchTopic)+="room2"))){
      switchPublishLedFeedback(2,message.toInt());
    }else if ((String(topic) == (String (baseToggleTopic)+="room1"))){
      togglePublishLedFeedback(message.toInt(),1);
    }else if ((String(topic) == (String (baseToggleTopic)+="room2"))){
      togglePublishLedFeedback(message.toInt(),2);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void reconnectBroker(){
  while (!client.connected()) {
      String client_id = "nodeMCU-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
      if (client.connect(client_id.c_str(), mqttUsername, mqttPassword)) {
          Serial.println("Public hiveMQ mqtt broker connected");
          for(int i=0 ;i<2;i++){
            char switchMessage[100];
            char toggleMessage[100];
            sprintf(switchMessage,"%d%d",i+1,digitalRead(ledPin[i]));
            sprintf(toggleMessage,"%d%d",i+1,digitalRead(ledPin[i]));
            client.publish(switchFeedbackTopic,switchMessage);
            client.publish(toggleFeedbackTopic,toggleMessage);
          }
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }}
}
void togglePublishLedFeedback(int times,int roomNo){
  char toggleMessage[100];
  char endingMessage[100];

  sprintf(toggleMessage, "%d1", roomNo);
  sprintf(endingMessage, "%d0",roomNo);
  client.publish(toggleFeedbackTopic, toggleMessage);
  for(int i=0;i<times;i++){
    digitalWrite(ledPin[roomNo], HIGH); 
    delay(delayTime); 
    digitalWrite(ledPin[roomNo], LOW);
    delay(delayTime); 
  }
  client.publish(toggleFeedbackTopic,endingMessage);
}
void switchPublishLedFeedback(int roomNo, int state){
  char ONMessage[100];
  char OFFMessage[100];

  sprintf(ONMessage,"%d1",roomNo);
  sprintf(OFFMessage,"%d0",roomNo);
  digitalWrite(ledPin[roomNo],state);
  if(state==1){
    client.publish(switchFeedbackTopic,ONMessage);
  }else if(state==0){
    client.publish(switchFeedbackTopic,OFFMessage);
  }
}
void loop() {
  
client.loop();
    delay(100);
    
}
