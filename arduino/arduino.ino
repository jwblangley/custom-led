#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// Generated proto
#include <led.pb.h>
#include <pb_decode.h>

// This file is excluded from the git working tree for secuity reasons
#include "src/network_credentials.h"

#include "src/led_manager.h"


#define PORT 8000
#define UDP_MAX 1478
#define BAUD 115200

WiFiUDP udp;
unsigned char packetBuffer[UDP_MAX];

LEDManager ledManager;

void setup() {
  Serial.begin(BAUD);

  WiFi.disconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.printf("WiFi attempting to connect. status=%d\n", WiFi.status());
  }
  Serial.printf("WiFi connected. IP address: %s\n", WiFi.localIP().toString().c_str());

  udp.begin(PORT);
  Serial.printf("UDP server started on port %d\n", PORT);

  Serial.println("Initialising LED Manager");
  ledManager.init();
}

void loop() {
  const int packetSize = udp.parsePacket();
  if (packetSize > 0) {
    const int len = udp.read(packetBuffer, UDP_MAX);

    Serial.printf("Received %d bytes from %s, port %d\n",
                  packetSize,
                  udp.remoteIP().toString().c_str(),
                  udp.remotePort());

    CustomLEDMessage request;
    pb_istream_t stream = pb_istream_from_buffer(packetBuffer, len);
    if (pb_decode(&stream, CustomLEDMessage_fields, &request))
    {
      switch (request.which_choice)
      {
        case CustomLEDMessage_set_leds_tag:
          ledManager.setLEDs(request.choice.set_leds);
          break;
        case CustomLEDMessage_clear_tag:
          ledManager.clear(request.choice.clear);
          break;
      }
    }
    else
    {
      Serial.printf("Decode error: %s\n", PB_GET_ERROR(&stream));
    }
  }
}
