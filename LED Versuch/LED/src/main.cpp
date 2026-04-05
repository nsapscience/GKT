#include <Arduino.h>

String eingang = "";
const int ledPin13 = 13; //GPIO Pin der LED Anschluss
const int ledPin11 = 11; //GPIO Pin der LED Anschluss
const int ledPin9 = 9; //GPIO Pin der LED Anschluss
const int ledPin3 = 3; //GPIO Pin der LED Anschluss

void setup() {
  Serial.begin(115200);
  pinMode(ledPin13, OUTPUT);
  pinMode(ledPin11, OUTPUT);
  pinMode(ledPin9, OUTPUT);
  pinMode(ledPin3, OUTPUT); 
  digitalWrite(ledPin13, LOW);
  digitalWrite(ledPin11, LOW);
  digitalWrite(ledPin9, LOW);
  digitalWrite(ledPin3, LOW);
}

void loop(){
  if(Serial.available()){
    eingang = Serial.readStringUntil('\n');
    eingang.trim(); //Entfernt führende und nachfolgende Leerzeichen
  }
  if(eingang == "1"){
    digitalWrite(ledPin9, HIGH);
    
    digitalWrite(ledPin9, LOW);
  }
  if(eingang == "2"){
    digitalWrite(ledPin13, HIGH);
    
    digitalWrite(ledPin13, LOW);
  }
  if(eingang == "3"){
    digitalWrite(ledPin3, HIGH);
    
    digitalWrite(ledPin3, LOW);
  }
  if(eingang == "4"){
    digitalWrite(ledPin11, HIGH);
    
    digitalWrite(ledPin11, LOW);
  }
}