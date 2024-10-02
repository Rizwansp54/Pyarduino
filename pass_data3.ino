#include"DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11
DHT th(DHTPIN,DHTTYPE);
float tempf;
float tempc;
float humid;
void setup() {

  // put your setup code here, to run once:
  Serial.begin(9600);
  th.begin();
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  tempc=th.readTemperature();
  tempf=th.readTemperature(true);
  humid=th.readHumidity();
  Serial.print(tempf);
  Serial.print(',');
  Serial.println(humid);
  delay(500);
}
