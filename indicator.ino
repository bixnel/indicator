int reset = 2;
int count = 3;
String inputString = "";
void setup() {
  pinMode(reset,OUTPUT);
  pinMode(count,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
  delay(10); 
}

void serialEvent() {
  char inChar;
  String inputString = "";
  do  {
    inChar =(char)Serial.read();
    inputString += inChar;
  } while (Serial.available() && inChar!='\n');
//  digitalWrite(reset, 0);
  digitalWrite(reset, 1);
  digitalWrite(reset, 0);
  for (int i = 0; i<inputString.toInt(); i++) {
    digitalWrite(count, 1);
    digitalWrite(count, 0);
//    Serial.println(i);
  }
  Serial.println(inputString.toInt());
}
