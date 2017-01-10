
void setup() {
  Serial.begin(230400);
//  UCSR0B |= 2; // Set U2Xn
//  UBRR0H = 0;
//  UBRR0L = 8;
  //analogReference(EXTERNAL);
  // At a clock rate of 125khz / 13ADChz, we get a sample rate of 9615.3hz
  ADMUX = 0x4; // Internal reference, no left shift, ADC4.
  ADCSRA = 0xAF; // ADC on, Auto trigger, intr enable, CLK/128 = 125khz
  ADCSRB = 0; // Free running mode
  ADCSRA = 0xEF; // Trigger start of free running mode
}

static volatile bool read = false;
static volatile uint16_t sample = 0;

ISR(ADC_vect) {
  read = true;
  uint8_t tmp = ADCL;
  uint8_t tmp2 = ADCH;
  sample = ADCH << 8  | tmp;
}

void loop() {
  while (true) {
    if (read) {
      read = false;
      Serial.write(sample & 0xFF);
      Serial.write(sample >> 8);
    }
  }
}
