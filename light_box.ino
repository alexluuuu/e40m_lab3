/* Simple LED Code Controller
 *
 * ENGR 40M
 * July 2018
 */

#define ANODE_OFF HIGH
#define ANODE_ON LOW
#define CATHODE_OFF HIGH
#define CATHODE_ON LOW

// Define arrays for the anode (+) and cathode (-) wire pins.
// Your pins will probably be different.
// Remember that analog pins (A0, A1, ...) can also act as digital.
const byte CATHODE_PINS [8] = {A3, A2 , A1 , A0 , 5, 4, 3, 2};
const byte ANODE_PINS [8] = {13, 12, 11, 10, 9, 8, 7, 6};
                    
void setup() {
  // In this function, you need to do two things:
  //  1. Configure all 8 anode (+) and all 8 cathode (-) pins to outputs
  //  2. Turn all 16 pins "off" (does this mean HIGH or LOW?)

  // Here's part 1, as an example (you can use this):
  for (byte i = 0; i < 8; i++) {
    pinMode(ANODE_PINS[i], OUTPUT);
    digitalWrite (ANODE_PINS[i],ANODE_OFF);
    
    pinMode(CATHODE_PINS[i], OUTPUT);
    digitalWrite (CATHODE_PINS[i],CATHODE_OFF);
  }

  Serial.begin(115200);
}

void loop() { 
  static byte frame[8][8];
  
  if (Serial.available()){
    //Builds the board from bit by bit communication through the python interface.
    String str1 = Serial.readStringUntil('\n');
    for (int i = 0; i < 64; i++) {
      frame[i/8][i%8] = str1[i] == '1' ? 1 : 0;
    }
  }
  display(frame);
}

/* Displays a single Frame: */
void display ( byte pattern [8][8]) {
  for (byte anode = 0; anode < 8; anode++){
    for (byte cathode = 0; cathode < 8; cathode++){
      if (pattern[anode][cathode] == 1) digitalWrite (CATHODE_PINS[cathode],CATHODE_ON);
      else digitalWrite (CATHODE_PINS[cathode],CATHODE_OFF);
    }
    digitalWrite (ANODE_PINS[anode],ANODE_ON);
    delay(1);
    digitalWrite (ANODE_PINS[anode],ANODE_OFF);
  } 
}
