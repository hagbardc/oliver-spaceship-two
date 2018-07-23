#include <Arduino.h>

unsigned long old_time, new_time;

void setup() {
    old_time = millis();

    Serial.begin(19200);

}

void loop() {
    new_time = millis();
    if((new_time - old_time) > 2000 ) { // 5 second timer
        old_time = new_time;

        Serial.print("Time on device 2 is ");
        Serial.println(new_time);
    }
}
