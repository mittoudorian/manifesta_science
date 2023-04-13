//Type de carte : Leonardo

// Site pour comprendre les interruptions Arduino (est-ce la meme chose pour arduino Leonardo ?) :
// https://www.electrosoftcloud.com/en/pcint-interrupts-on-arduino/


# define vitesse 100
# define tempo_recul 100
# define tempo_tourne 400

# define train_impulsions 24
# define nb_envois 20

#define EN1 6//pin to run the right motor 
#define IN1 7//pin to control right motor direction
#define EN2 5//pin to run the left motor 
#define IN2 12//pin to control left motor direction

#define FORW 0//go forward
#define BACK 1//go backward

#define IR_IN  17//Infrared receiver (D17=A3 ?)
#define L_IR 13//Infrared transmitter on the left side
#define R_IR 8//Infrared transmitter on the right side

int   count;//counts the pulses


//控制电机转动
void Motor_Control(int M1_DIR,int M1_EN,int M2_DIR,int M2_EN)
{
  //////////M1////////////////////////
  if(M1_DIR==FORW)  digitalWrite(IN1,FORW); else digitalWrite(IN1,BACK);
  if(M1_EN==0)       analogWrite(EN1,LOW);  else analogWrite(EN1,M1_EN);
  ///////////M2//////////////////////
  if(M2_DIR==FORW) digitalWrite(IN2,FORW);  else digitalWrite(IN2,BACK);
  if(M2_EN==0)     analogWrite(EN2,LOW);    else analogWrite(EN2,M2_EN);
}


//Functions to send pulse of 40KHz
void L_Send40KHZ(void)//left ir transmitter sends 40kHZ pulses
{
  int i;
  for(i=0;i<train_impulsions;i++)
  {
    digitalWrite(L_IR,LOW);//设置左发射管为高电平
    delayMicroseconds(8);//延时
    digitalWrite(L_IR,HIGH);//设置左发射管为低电平
    delayMicroseconds(8);//延时
  }
}

void R_Send40KHZ(void)//right ir transmitter sends 40kHZ pulses
{
  int i;
  for(i=0;i<train_impulsions;i++)
  {
    digitalWrite(R_IR,LOW);//设置右发射管为高电平
    delayMicroseconds(8);//延时
    digitalWrite(R_IR,HIGH);//设置右发射管为低电平
    delayMicroseconds(8);//延时
  }
}

void pcint0_init(void)//init the interrupt (AG : je ne comprends pas comment récupère D17...???)
{
  PCICR = 0X01;// We activate the interrupts of the PB port
  // PB port corresponds to the group of pins PCINT0 to PCINT5 and which are pins D8 to D13
  // (2 : PC port, 4 : PD port)
  
  PCMSK0 = 0X01;//PCMSK0 -> PB -> D8 to D13 pins (PCMSK1 -> PC -> A0 to A5 pins, PCMSK2 -> PD -> D0 to D7 pins)
  // Here activate the interrupts on pin D8
}
ISR(PCINT0_vect)//ISR(PCINT0_vect)  est une « interrupt service routine », qui s’éxécute lorsque PCINT0_vect  se déclenche : Pin Change Interrupt Request 0 (pins D8 to D13).
// (PCINT1_vect -> PC -> Pins A0 to A5, PCINT2_vect-> PD -> Pins D0 to D7)
{
  count++;//   every 32 count of freqCounter ~1ms ?????????????
  Serial.print ("interrupt");
}


void Obstacle_Avoidance(void)//避障子函数
{   
  char i;
  count=0;
  for(i=0;i<nb_envois;i++)//left transmitter sends pulses
  {
    L_Send40KHZ();
    delayMicroseconds(600);    
  }
  if(count>nb_envois)//if many pulses received, it means there's an obstacle
  {
      Motor_Control(BACK,vitesse,BACK,vitesse);//后退
      delay(tempo_recul);//延时
      Motor_Control(BACK,vitesse,FORW,vitesse);//右转
      delay(tempo_tourne);//延时
  }
  else
  {
      Motor_Control(FORW,vitesse,FORW,vitesse);//前进
  }
  count=0;
  for(i=0;i<nb_envois;i++)//right transmitter sends pulses
  {
    R_Send40KHZ(); 
    delayMicroseconds(600);        
  }
  if(count>20)
  {
      Motor_Control(BACK,vitesse,BACK,vitesse);//后退
      delay(tempo_recul);//延时
      Motor_Control(FORW,vitesse,BACK,vitesse);//左转
      delay(tempo_tourne);//延时
  }
  else
  {
      Motor_Control(FORW,vitesse,FORW,vitesse);//前进
  }
}


void setup()
{
  pinMode(EN2,OUTPUT);
  pinMode(EN1,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  pinMode(R_IR,OUTPUT);
  pinMode(L_IR,OUTPUT);
  pinMode(IR_IN,INPUT);

  pcint0_init();
  
  // ajouté par Alain (vu sur le site http://gammon.com.au/interrupts)
  // (should be useless : the default in the Arduino is for interrupts to be enabled ???)
  
  Serial.print ("debut");
interrupts ();  // or ...
//sei ();         // set interrupts flag
}


void loop()
{
  Obstacle_Avoidance();
}
