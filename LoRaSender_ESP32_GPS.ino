#include <SPI.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

#define ss 5
#define rst 14
#define dio0 2

TinyGPSPlus gps;
SoftwareSerial gpsSerial(16, 17);

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender");
  LoRa.setPins(ss, rst, dio0);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {

 while (gpsSerial.available() > 0)
 {
    if (gps.encode(gpsSerial.read()))
    {
        if (gps.location.isValid())
        { 
          delay(1000);          
          Serial.println("Sending to LoRa");
          LoRa.beginPacket();
          //LoRa.print("Lat: ");
          LoRa.print(gps.location.lat(), 6);
          //LoRa.print(" Long: ");
          LoRa.print(",");
          LoRa.print(gps.location.lng(), 6);
          Serial.println("Sent via LoRa");
          LoRa.endPacket();
        }
    }
 }
}