#include<Servo.h>

Servo head;
Servo l_hand;
Servo r_hand;
short but = 6;
short vcc = 7;
short grn = 8;
short buttonState;

// received data
byte val = "";
void setup() {
  // put your setup code here, to run once:
  head.attach(4);
  l_hand.attach(5);
  r_hand.attach(3);
  Serial.begin(9600); // for communicating via serial port with Python
  pinMode(but, INPUT);
  digitalWrite(vcc, HIGH);
  digitalWrite(grn, LOW);
  pinMode(vcc, OUTPUT);
  pinMode(grn, OUTPUT);
}
void standby() {
  // all motors to these positions
  head.write(87);
  int r_pos = 30;
  int l_pos = map(r_pos, 0, 180, 180, 0);
  l_hand.write(l_pos);
  r_hand.write(r_pos);
}
void hi() {
  // all motors to these positions
  head.write(87);
  int i = 0;
  for (i = 30; i <= 170; i++) {
    r_hand.write(i);
    delay(5);
  }
  for (i = 170; i >= 100; i--) {
    r_hand.write(i);
    delay(5);
  }
  for (i = 100; i <= 170; i++) {
    r_hand.write(i);
    delay(5);
  }
  for (i = 170; i >= 30; i--) {
    r_hand.write(i);
    delay(5);
  }
  standby();
}
void hands_up() {
  // do this on every command (nothing much just move hands a bit)
  //head.write(150);
  //delay(300);
  //head.write(90);
  int i = 0;
  for (i = 30; i <= 170; i++) {
    int r_pos = i;
    int l_pos = map(r_pos, 0, 180, 180, 0);
    l_hand.write(l_pos);
    r_hand.write(r_pos);
    delay(5);
  }
  delay(600);
  for (i = 170; i >= 30; i--) {
    int r_pos = i;
    int l_pos = map(r_pos, 0, 180, 180, 0);
    l_hand.write(l_pos);
    r_hand.write(r_pos);
    delay(5);
  }
}

void look_left() {
  // rotate hed to left
  head.write(180);
}
void confused() {
  for (int count = 0; count <= 2; count++) {
    head.write(30);
    r_hand.write(170);
    delay(700);
    r_hand.write(30);
    head.write(120);
    l_hand.write(30);
    delay(700);
    l_hand.write(160);
  }
  standby();
}

void r_upper_cut() {
  // make right upper-cut
  int i = 0;
  for (i = 30; i <= 170; i++) {
    int r_pos = i;
    int l_pos = map(r_pos, 0, 180, 180, 0);
    l_hand.write(l_pos);
    r_hand.write(r_pos);
    delay(5);
  }
  for (int count = 0; count <= 4; count++) {
    int i = 0;
    for (i = 170; i >= 60; i--) {
      r_hand.write(i);
      delay(1);
    }
    for (i = 60; i <= 170; i++) {
      r_hand.write(i);
      delay(1);
    }
  }
  standby();
  delay(100);
}


void loop() {
  // put your main code here, to run repeatedly:
  standby();
  buttonState = digitalRead(but);
  if (buttonState == HIGH)
  {
    Serial.println("on");
  }
  while (Serial.available() > 0) //look for serial data available or not
  {
    val = Serial.read();        //read the serial value
    if (val == 'h') {
      // do hi
      hi();
    }
    if (val == 'u') {
      hands_up();
      delay(2000);
    }
    if (val == 'l') {
      standby();
      look_left();
      delay(2000);
    }
    if (val == 'U') {
      r_upper_cut();
      delay(2000);
    }
    if (val == 'c') {
      confused();
      delay(2000);
    }
  }
  delay(180);
}
