#define LEDPIN A0
#define FANPIN A1


void setup() {
  // put your setup code here, to run once:
  pinMode(LEDPIN,OUTPUT);
  pinMode(FANPIN,OUTPUT);
  Serial.begin(9600);
 // digitalWrite(op,HIGH);

}

void loop() {
  
  if(Serial.available()> 0){
    
    int a=Serial.read();
    if(a==97)
      digitalWrite(LEDPIN,HIGH);
     if(a==98)
      digitalWrite(LEDPIN,LOW);
    if(a==99)
      digitalWrite(FANPIN,HIGH);
     if(a==100)
      digitalWrite(FANPIN,LOW);
      
      
    }

}
