#include <WiFi.h>
#include <WiFiUdp.h>

// This file is excluded from the git working tree for secuity reasons
#include "network_credentials.h"

#define PORT 8000
#define UDP_MAX 1478
#define BAUD 115200

WiFiUDP udp;
char packetBuffer[UDP_MAX];

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
}

void loop() {
  const int packetSize = udp.parsePacket();
  if (packetSize) {
    const int len = udp.read(packetBuffer, UDP_MAX);

    Serial.printf("Received %d bytes from %s, port %d\n",
                  packetSize,
                  udp.remoteIP().toString().c_str(),
                  udp.remotePort());
  }
}
