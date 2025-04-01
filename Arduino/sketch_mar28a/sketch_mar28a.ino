#include "DataManager.h"

int id = 7;
int day = 0;
bool broken = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
    Data data;
    Data* data_ptr = &data;
    data_ptr->id = id;

    // Generate random number
    float random_number = random(0, 10000) / 10000.0; // Random number between 0 and 1;
    if (random_number < calculate_probability(day) || broken) {
        grab_random_bad(data_ptr);
        Serial.println("Bad data generated");
        broken = true;
    } else {
        grab_random_good(data_ptr);
        Serial.println("Good data generated");
    }

    Serial.print("Day: ");
    Serial.println(day);
    // Print the data
    Serial.print("ID: ");
    Serial.println(data_ptr->id);
    Serial.print("TP2: ");
    Serial.println(data_ptr->tp2);
    Serial.print("TP3: ");
    Serial.println(data_ptr->tp3);
    Serial.print("H1: ");
    Serial.println(data_ptr->h1);
    Serial.print("DV Pressure: ");
    Serial.println(data_ptr->dv_pressure);
    Serial.print("Reservoirs: ");
    Serial.println(data_ptr->resevoirs);
    Serial.print("Oil Temperature: ");
    Serial.println(data_ptr->oil_temperature);
    Serial.print("Motor Current: ");
    Serial.println(data_ptr->motor_current);
    Serial.print("COMP: ");
    Serial.println(data_ptr->COMP);
    Serial.print("DV Electric: ");
    Serial.println(data_ptr->dv_electric);
    Serial.print("Towers: ");
    Serial.println(data_ptr->towers);
    Serial.print("MPG: ");
    Serial.println(data_ptr->mpg);
    Serial.print("LPS: ");
    Serial.println(data_ptr->lps);
    Serial.print("Pressure Switch: ");
    Serial.println(data_ptr->pressure_switch);
    Serial.print("Oil Level: ");
    Serial.println(data_ptr->oil_level);
    Serial.print("Caudal Impulses: ");
    Serial.println(data_ptr->caudal_impulses);
    Serial.println();

    day++;
    delay(10000); // Delay for 1 second
}
