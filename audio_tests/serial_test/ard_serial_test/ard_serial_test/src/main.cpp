#include <Arduino.h>

unsigned long old_time, new_time;
int button_state;

void setup() {
    old_time = millis();
    button_state = 0;

    Serial.begin(19200);



}

void loop() {
    new_time = millis();
    if((new_time - old_time) > 5000 ) { // 5 second timer
        old_time = new_time;

        if(button_state) {
            button_state = 0;
            Serial.println("{\"action\": \"button_down\", \"name\": \"arduino_2\"}");
        } else {
            Serial.println("{\"action\": \"button_up\", \"name\": \"arduino_2\"}");
            button_state = 1;
        }

    }
}
