#include <SoftwareSerial.h>
SoftwareSerial s(11,12);

void setup() {
  // put your setup code here, to run once:
  s.begin(57600);
  Serial.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:
  s.println("lorawan join otaa");
//  s.listen();
  Serial.print(s.read());
  delay(10000);
}
