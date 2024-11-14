#include <SPI.h>
#include <LoRa.h>

#define ss 5
#define rst 14
#define dio0 2


void setup() {
  Serial.begin(115200);
  while (!Serial);
  delay(500);
  Serial.println("LoRa Receiver");
  LoRa.setPins(ss, rst, dio0);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("Starting LoRa failed!");
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.println();
    Serial.print("Received packet ");

    // read packet
    while (LoRa.available()) {
     char incoming = (char)LoRa.read();
        Serial.print(incoming);
      
    }
  }
}
