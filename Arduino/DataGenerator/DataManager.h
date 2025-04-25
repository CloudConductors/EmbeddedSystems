#ifndef DATAMANAGER_H
#define DATAMANAGER_H

#pragma once
#include <math.h>
#include <Arduino.h>

typedef struct {
    int id;
    char timestamp[20];
    float tp2;
    float tp3;
    float h1;
    float dv_pressure;
    float resevoirs;
    float oil_temperature;
    float motor_current;
    float COMP;
    float dv_electric;
    float towers;
    float mpg;
    float lps;
    float pressure_switch;
    float oil_level;
    float caudal_impulses;
} Data;

// Function prototypes
void grab_random_good(Data* data);
void grab_random_bad(Data* data);
float generate_random_value(float mean, float std);
float calculate_probability(int day);
float phi(float x);
float clamp_towers(float towers);

#endif // DATAMANAGER_H

