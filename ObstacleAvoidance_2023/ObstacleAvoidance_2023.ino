// Type de carte : Leonardo

// Site pour comprendre les interruptions Arduino (est-ce la meme chose pour arduino Leonardo ?) :
// https://www.electrosoftcloud.com/en/pcint-interrupts-on-arduino/

#define vitesse 100
#define tempo_recul 100
#define tempo_tourne 400

#define train_impulsions 24
#define nb_envois 20

#define EN1 6 // Broche pour contrôler le moteur droit
#define IN1 7 // Broche pour contrôler la direction du moteur droit
#define EN2 5 // Broche pour contrôler le moteur gauche
#define IN2 12 // Broche pour contrôler la direction du moteur gauche

#define FORW 0 // Aller en avant
#define BACK 1 // Aller en arrière

#define IR_IN 17 // Récepteur infrarouge (D17=A3 ?)
#define L_IR 13 // Émetteur infrarouge côté gauche
#define R_IR 8 // Émetteur infrarouge côté droit

int count; // Compteur de pulsations

// Fonction pour contrôler les moteurs
void Motor_Control(int M1_DIR, int M1_EN, int M2_DIR, int M2_EN)
{
  //////////M1////////////////////////
  if (M1_DIR == FORW)
    digitalWrite(IN1, FORW);
  else
    digitalWrite(IN1, BACK);
  if (M1_EN == 0)
    analogWrite(EN1, LOW);
  else
    analogWrite(EN1, M1_EN);
  ///////////M2//////////////////////
  if (M2_DIR == FORW)
    digitalWrite(IN2, FORW);
  else
    digitalWrite(IN2, BACK);
  if (M2_EN == 0)
    analogWrite(EN2, LOW);
  else
    analogWrite(EN2, M2_EN);
}

// Fonctions pour envoyer des pulsations de 40 kHz
void L_Send40KHZ(void) // Émetteur infrarouge gauche envoie des pulsations de 40 kHz
{
  int i;
  for (i = 0; i < train_impulsions; i++)
  {
    digitalWrite(L_IR, LOW); // Mettre la broche de l'émetteur infrarouge gauche à niveau bas
    delayMicroseconds(8);    // Délai
    digitalWrite(L_IR, HIGH); // Mettre la broche de l'émetteur infrarouge gauche à niveau haut
    delayMicroseconds(8);    // Délai
  }
}

void R_Send40KHZ(void) // Émetteur infrarouge droit envoie des pulsations de 40 kHz
{
  int i;
  for (i = 0; i < train_impulsions; i++)
  {
    digitalWrite(R_IR, LOW); // Mettre la broche de l'émetteur infrarouge droit à niveau bas
    delayMicroseconds(8);     // Délai
    digitalWrite(R_IR, HIGH); // Mettre la broche de l'émetteur infrarouge droit à niveau haut
    delayMicroseconds(8);     // Délai
  }
}

void pcint0_init(void) // Initialisation de l'interruption
{
  PCICR = 0X01; // Activation des interruptions du port PB
  // Le port PB correspond au groupe de broches
