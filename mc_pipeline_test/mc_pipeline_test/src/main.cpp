#include <Arduino.h>
#include <Button.h>


uint8_t button_array[] = { 8 };

Button *button;

char component_name_1[] = {"arduino_1"};
char component_name_2[] = {"arduino_2"};
char *component_name = &component_name_1[0];



void setup() {

    #if defined(__AVR_ATmega328P__)
    component_name = &component_name_2[0];
    #endif

    button = new Button(button_array[0]);
    button->begin();
    Serial.begin(19200);
}

void loop() {

    if(button->pressed()) {
        Serial.print("{\"action\": \"button_down\", \"name\": \"");
        Serial.print(component_name);
        Serial.println("\"}");
    } else if(button->released()) {
        Serial.print("{\"action\": \"button_up\", \"name\": \"");
        Serial.print(component_name);
        Serial.println("\"}");
    }

}
