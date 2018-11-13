#include <ESP8266WiFi.h>

#define LED_RED   15
#define LED_GREEN 12
#define LED_BLUE  13

const char* ssid = "wagwan";
const char* password = "3035highway7";

WiFiServer server(80);

void setup() {
  pinMode(LED_RED, OUTPUT); 
  pinMode(LED_BLUE, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);

  Serial.begin(115200);
  delay(10);

  Serial.println();
  Serial.println();
  Serial.print("Connection to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Connected");

  server.begin();

  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

// the loop function runs over and over again forever
void loop() {

  int redState;
  int blueState;
  int greenState;
  
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  if (request.indexOf("cmd=TURN_ON_RED") != -1)
  {
    redState = LOW;
    digitalWrite(LED_RED, redState);
  }
  else if (request.indexOf("cmd=TURN_OFF_RED") != -1)
  {
    redState = HIGH;
    digitalWrite(LED_RED, redState);    
  }
  if (request.indexOf("cmd=TURN_ON_BLUE") != -1)
  {
    blueState = LOW;
    digitalWrite(LED_BLUE, blueState);
  }
  else if (request.indexOf("cmd=TURN_OFF_BLUE") != -1)
  {
    blueState = HIGH;
    digitalWrite(LED_BLUE, blueState);    
  }
  if (request.indexOf("cmd=TURN_ON_GREEN") != -1)
  {
    greenState = LOW;
    digitalWrite(LED_GREEN, greenState);
  }
  else if (request.indexOf("cmd=TURN_OFF_GREEN") != -1)
  {
    greenState = HIGH;
    digitalWrite(LED_GREEN, greenState);    
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("");
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
 
  client.print("Led pin is now: ");
 
  if(redState == LOW) {
    client.print("On");
  } else {
    client.print("Off");
  }
  
  client.println("<br><br>");
  client.println("<a href=\"?cmd=TURN_ON_RED\"><button>Turn On Red</button></a>");
  client.println("<a href=\"?cmd=TURN_OFF_RED\"><button>Turn Off Red</button></a>");
  client.println("<br><br>");
  client.println("<a href=\"?cmd=TURN_ON_BLUE\"><button>Turn On Blue</button></a>");
  client.println("<a href=\"?cmd=TURN_OFF_BLUE\"><button>Turn Off Blue</button></a>");
  client.println("<br><br>");
  client.println("<a href=\"?cmd=TURN_ON_GREEN\"><button>Turn On Green</button></a>");
  client.println("<a href=\"?cmd=TURN_OFF_GREEN\"><button>Turn Off Green</button></a>");

  client.println("</html>");
 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");

}
