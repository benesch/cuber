const int LATCH_PIN = 9;
const int CLOCK_PIN = 10;
const int DATA_PIN = 8;

const int LAYERS = 4;
const int COLUMNS = 16;
const int BYTES_PER_LAYER = COLUMNS / 8;

char layerMatrix[LAYERS][BYTES_PER_LAYER];
char layerPins[LAYERS] = { 7, 4, 5, 6 };

void setup() {
      pinMode(LATCH_PIN, OUTPUT);
        pinMode(CLOCK_PIN, OUTPUT);
          pinMode(DATA_PIN, OUTPUT);

            for (int i = 0; i < LAYERS; i++) {
                    pinMode(layerPins[i], OUTPUT);
                      }

              Serial.begin(115200);
                Serial.setTimeout(60000);
                  Serial.print("reset");
                    Serial.print("ready");
}

void loop() {
      if (Serial.available() >= 2) {
              for (int i = 0; i < LAYERS; i++) {
                        Serial.readBytes(layerMatrix[i], BYTES_PER_LAYER);
                              Serial.print("ready");
                                  }
                }
        for (int i = 0; i < LAYERS; i++) {
                writeLayer(i, layerMatrix[i]); 
                  }
}

/* write layer to leds
    * layer: int representing which layer
     * matrix: array of BYTES_PER_LAYER length where
      each bit represents one LED's state */

void writeLayer(int layer, char matrix[]) {
      toggleLayer(layer, true);
        for (int i = BYTES_PER_LAYER - 1; i >= 0; i--) {
                shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, matrix[i]);
                  }
          toggleLayer(layer, false);
}

/* turn a layer on or off
    * layer: int representing which layer
     * state: boolean representing on (true) or off (false) */

void toggleLayer(int layer, boolean state) {
      digitalWrite(layerPins[layer], !state);
        digitalWrite(LATCH_PIN, !state);  
}

