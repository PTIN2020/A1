
//Abrir teclado Ctrl+MAYUS+M
//analogWrite(13, 200);//subir potencia led
//Aquest script utilitza Arduino Uno i Raspberry pi 3 Model B V1.2 per comunicar-se

#include <Wire.h> //llibreria arduino que el connecta al bus
#include <LiquidCrystal_I2C.h> //llibreria pantalla
#include <Ultrasonic.h> //llibreria ultraso

LiquidCrystal_I2C lcd (0x3F, 16, 2); //inicialització pantalla
Ultrasonic sensordavant(12,11); //pin trig, pin echo
Ultrasonic sensorpost(8,9); //pin trig, pin echo 

int distsensordavant; // variable de distancia de l'ultraso de davant
int distsensorposterior; // variable de distancia de l'ultraso de darrere
const int ledPINrojoizq = 4; //pin del led vermell esquerre a la placa
const int ledPINrojoder = 5; //pin del led vermell dret a la placa
const int ledPINamaizq = 6; //pin del led groc esquerre a la placa
const int ledPINamader = 7; //pin del led groc dret a la placa
int Sensor1 = 0; //Sensor infraroig 1
int Sensor2 = 0; //Sensor infraroig 2

void setup(){
 Serial.begin(9600); //Estableix la velocitat de dades en bits/s del port serial
 pinMode(ledPINrojoizq , OUTPUT);  //definir pin com a sortida
 pinMode(ledPINrojoder , OUTPUT); //definir pin com a sortida
 pinMode(ledPINamaizq , OUTPUT);  //definir pin com a sortida
 pinMode(ledPINamader , OUTPUT); //definir pin com a sortida
 pinMode(Sensor1, OUTPUT); //definir sensor com a sortida
 pinMode(Sensor2, OUTPUT); //definir sensor com a sortida
 Wire.begin(); //inicialitza la llibreria Wire i connecta arduino al bus
 lcd.begin(16, 2); //dimensions pantalla lcd (amplada i altura)
 lcd.clear(); //neteja la pantalla lcd
 lcd.backlight(); //Encén la llum de la pantalla
}

void loop(){

 
  //Llegeix la distància del sensor de davant 
  distsensordavant = sensordavant.distanceRead();
  //Llegeix la distància del sensor de darrere
  distsensorposterior = sensorpost.distanceRead();
  //Espera 500 ms entre cada lectura
  delay(500);
  //Si la distància es menor a 20 cm els leds de darrere s'encendran i s'aturarà
  //el cotxe i mostrarà el següent missatge per la pantalla lcd
  if( distsensordavant <= 50 ){
    Serial.println("Obstacle davant");//Enviament informació Raspberry pi
    digitalWrite(ledPINrojoder , HIGH);
    digitalWrite(ledPINrojoizq , HIGH);
    digitalWrite(ledPINamader , LOW);
    digitalWrite(ledPINamaizq , LOW);
    lcd.clear();
    lcd.setCursor(5, 0);
    lcd.print("VEHICLE");
    lcd.setCursor(4, 1);
    lcd.print("EN SERVEI");
    delay(3000);
    lcd.clear();
    for(int c=0;c<20;c++){
      lcd.setCursor(1, 0);
      lcd.print("SI US PLAU, NO OBSTACULITZI LA VIA");
      lcd.scrollDisplayLeft(); // Movimiento a la Izquierda
      lcd.setCursor(8, 1);
      lcd.print("VEHICLE EN SERVEI");
      delay(400);
    }
  //Si la distància es menor a 20 cm els leds de darrere s'encendran i s'aturarà
  //el cotxe i mostrarà el següent missatge per la pantalla lcd
  }else if(distsensorposterior <= 50){
    Serial.println("Obstacle darrere");//Enviament informació Raspberry pi 
    digitalWrite(ledPINrojoder , HIGH);
    digitalWrite(ledPINrojoizq , HIGH);
    digitalWrite(ledPINamader , LOW);
    digitalWrite(ledPINamaizq , LOW);
    lcd.clear();
    lcd.setCursor(4, 0);
    lcd.print("OBSTACLE");
    lcd.setCursor(3, 1);
    lcd.print("AL DARRERE");
    delay(400);
  }
  else{
      //Si el cotxe no te cap obstacle ni davant ni darrere el cotxe anirà endavant 
    //seguint la línia negra i mostrarà el següent missatge per la pantalla lcd
    //amb els leds grocs encessos i els vermells apagats
      
      digitalWrite(ledPINrojoder , LOW);
      digitalWrite(ledPINrojoizq , LOW);
      lcd.clear();
      digitalWrite(ledPINamader , HIGH);
      digitalWrite(ledPINamaizq , HIGH);
      lcd.setCursor(1, 0);
      lcd.print("BENVINGUTS A LA");
      lcd.setCursor(3, 1);
      lcd.print("TERMINAL T1");
      delay(600);
    
      Sensor1 = digitalRead(2); //llegeix el valor del sensor i l'assigna al pin 2
      Sensor2 = digitalRead(3); //llegeix el valor del sensor i l'assigna al pin 3

// HIGH apagat(NEGRE) LOW ences(BLANC)
//Si el sensor 1 està encès i el sensor 2 apagat el cotxe anirà a l'esquerre 
//amb els leds esquerres encesos de forma intermitent
    if(Sensor1 == LOW && Sensor2 == HIGH){
      Serial.println("Linia blanca dreta");//Enviament informació Raspberry pi
      digitalWrite(ledPINrojoder , HIGH);
      digitalWrite(ledPINamader , HIGH);
      delay(3000);
      digitalWrite(ledPINrojoder , LOW);
      digitalWrite(ledPINamader , LOW);
    }
//Si el sensor 1 està apagat i el sensor 2 encès el cotxe anirà a la dreta 
//amb els leds drets encesos de forma intermitent 
  else if (Sensor1 == HIGH && Sensor2 == LOW){
    Serial.println("Linia blanca esquerre");//Enviament informació Raspberry pi
    digitalWrite(ledPINrojoizq , HIGH);
    digitalWrite(ledPINamaizq , HIGH);
    delay(3000);
    digitalWrite(ledPINrojoizq , LOW);
    digitalWrite(ledPINamaizq , LOW);
  }
  else if (Sensor1 == LOW && Sensor2 == LOW){
    Serial.println("Linia blanca"); //Enviament informació Raspberry pi
  }
  else{
    Serial.println("Via lliure");//Enviament informació Raspberry pi
    digitalWrite(ledPINrojoder , LOW);
    digitalWrite(ledPINrojoizq , LOW);
    lcd.clear();
    digitalWrite(ledPINamader , HIGH);
    digitalWrite(ledPINamaizq , HIGH);
    lcd.setCursor(1, 0);
    lcd.print("BENVINGUTS A LA");
    lcd.setCursor(3, 1);
    lcd.print("TERMINAL T1");
    delay(600);
  }
    
   
  }
}
