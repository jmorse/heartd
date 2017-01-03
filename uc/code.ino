
void setup() {
  Serial.begin(115200);
  analogReference(EXTERNAL);
}

void loop() {  
  // print labels
  unsigned long t = millis();
  while (true) {
    //Serial.print("Hello world\n");       // prints a label
    int val = analogRead(A4);
    Serial.write(val & 0xFF);
    Serial.write(val >> 8);
    Serial.write(0xAA);
    Serial.write(0xAA);
    Serial.write(t & 0xFF);
    Serial.write(t >> 8);
    Serial.write(0x55);
    Serial.write(0x55);

    // Poor mans timer
    while (t == millis())
      ;
    t = millis();
  }
}
