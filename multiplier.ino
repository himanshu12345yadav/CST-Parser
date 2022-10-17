
#define SIG_OUT 10
#define V_GND 9
#define LED_1 3
#define LED_2 4
#define LED_3 5
#define LED_4 6
#define LED_5 7
#define READ A5

int f = 2;
int fs = 500;
int scale = 1;

int* samples;

void setup(){
  	pinMode(SIG_OUT , OUTPUT);
    pinMode(V_GND , OUTPUT);
  	pinMode(LED_1 , OUTPUT);
  	pinMode(LED_2 , OUTPUT);
  	pinMode(LED_3 , OUTPUT);
  	pinMode(LED_4 , OUTPUT);
  	pinMode(LED_5 , OUTPUT);
  	pinMode(READ , INPUT);
    analogWrite(V_GND ,0);
    Serial.begin(9600);
  	samples = (int*)calloc(fs , sizeof(int));
  
  for(int i = 0 ; i < fs; i++){
    float ts = (float)i / fs;
    samples[i] = (int)(scale*(sin(2*3.14*f*ts) + 1));
  }
}

void display(int level){
  float val = abs((float)level * 5 / 1023);
  Serial.println(val);
  if(val >= 1){
    digitalWrite(LED_1 , HIGH);
  }
  else {
    digitalWrite(LED_1 , LOW);
  }
  
  if(val >=2){
	digitalWrite(LED_2 , HIGH);
  }
  else {
    digitalWrite(LED_2 , LOW);
  }
  
  if(val >= 3){
    digitalWrite(LED_3 , HIGH);
  }
  else {
    digitalWrite(LED_3 , LOW);
  }
  
  if(val >= 4){
    digitalWrite(LED_4 , HIGH);
  }
  else {
    digitalWrite(LED_4 , LOW);
  }
  
  if(val >= 5){
    digitalWrite(LED_5 , HIGH);
  }
  else {
    digitalWrite(LED_5 , LOW);
  }
}
void loop(){
  
  for(int i = 0 ; i < fs ; i++){
    analogWrite(SIG_OUT , samples[i]);
    delay(1*1000/(fs*f));
    int level = analogRead(READ);
    display(level);
  }
}