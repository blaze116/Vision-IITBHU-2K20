#include<Servo.h>
Servo servo;
int LmotorUp=13;
int LmotorDn=12;
int RmotorUp=11;
int RmotorDn=10;
int rspeed=5;
int lspeed=3;
int irl= 6;
char input;
int value1;
int angle=0;
void setup()
{
  Serial.begin(9600);
  servo.attach(8);
  
  servo.write(angle);
  
  pinMode(LmotorUp,OUTPUT);
  pinMode(LmotorDn,OUTPUT);
  pinMode(RmotorUp,OUTPUT);
  pinMode(RmotorDn,OUTPUT);
  pinMode(irl,INPUT);
  
}
void loop()
{
  
  
  analogWrite(rspeed,70);
  analogWrite(lspeed,60);
    if(Serial.available()>0)
  {
     input=Serial.read();
  }
   value1=digitalRead(irl);
    switch(input)
    {
      case 'f':
      {MoveF();
      break;}
      case 'r':{MoveR();
      break;}
      case 'l':{MoveL();
      break;}
      case 'b':{MoveB();
      break;}
      case 's':{Stop();
      break;}
      case 't':
      {MoveL();
      delay(250);
      break;}
      case 'r1':
      {Right90();
      break;}
      case 'r2':
      {Right180();
      break;}
      case 'l1':
      {Left90();
      break;}
      case 'l2':
      {Left180();
      break;}
      
   
      
  
 
   
   
      
  if(value1<400)
 {
  Stop();
    for(angle = 0; angle < 45; angle++)  
  {                                  
    servo.write(angle);               
                      
  } 
  
  
    
 }
 
 
 }
 



void MoveB()
{
  Serial.println("team kivi forward");
  digitalWrite(LmotorUp,HIGH);
  digitalWrite(LmotorDn,LOW);
  digitalWrite(RmotorUp,HIGH);
  digitalWrite(RmotorDn,LOW);
  delay(3000)
    

}
void MoveF()
{
  digitalWrite(LmotorUp,LOW);
  digitalWrite(LmotorDn,HIGH);
  digitalWrite(RmotorUp,LOW);
  digitalWrite(RmotorDn,HIGH);


  if (value1==1):
  {stop();
  }    
  }
   
 void MoveL()
 {
  digitalWrite(LmotorUp,HIGH);
  digitalWrite(LmotorDn,LOW);
  digitalWrite(RmotorUp,LOW);
  digitalWrite(RmotorDn,HIGH);
  
  
 }
 void MoveR()
 {
  digitalWrite(LmotorUp,LOW);
  digitalWrite(LmotorDn,HIGH);
  digitalWrite(RmotorUp,HIGH);
  digitalWrite(RmotorDn,LOW);
 
 }
 
void Stop()
{
  digitalWrite(LmotorUp,LOW);
  digitalWrite(LmotorDn,LOW);
  digitalWrite(RmotorUp,LOW);
  digitalWrite(RmotorDn,LOW);
  
}

void Release()
{
   for(angle =45; angle > 0; angle--)  
  {                                  
    servo.write(angle);               
                      
  } 
}

void Right90() 
{ Serial.turn(90);
  delay(3000);
}  
void Right180() 
{ Serial.turn(180);
  delay(3000);
}
void Left90() 
{ Serial.turn(-90);
  delay(3000);
}
void Left180() 
{ Serial.turn(-180);
  delay(3000);
}
