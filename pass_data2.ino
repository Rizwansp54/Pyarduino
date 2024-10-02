int p1=A0;
int p2;
int d=1000;
void setup() {
  // put your setup code here, to run once:
  pinMode(p1,INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  p2=analogRead(p1);
  Serial.println(p2);
  delay(d);
}
