#include "DataManager.h"

// GOOD VALUES ARE NOT ACCURATE RIGHT NOW BECAUSE THERE ARE APPARENTLY TWO TYPES OF GOOD DATA

// Good :)
float tp2_mean_good = 1.231891;
float tp3_mean_good = 8.998642;
float h1_mean_good = 7.719864;
float dv_pressure_mean_good = 0.019612;
float resevoirs_mean_good = 8.999247;
float oil_temperature_mean_good = 62.383127;
float motor_current_mean_good = 1.990015;
float comp_mean_good = 0.853729;
float dv_electric_mean_good = 0.143803;
float towers_mean_good = 0.928267;
float mpg_mean_good = 0.849349;
float lps_mean_good = 0.002999;
float pressure_switch_mean_good = 0.991371;
float oil_level_mean_good = 0.902237;
float caudal_impulses_mean_good = 0.935852;

float tp2_std_good = 3.134697;
float tp3_std_good = 0.633844;
float h1_std_good = 3.187576;
float dv_pressure_std_good = 0.277235;
float resevoirs_std_good = 0.633054;
float oil_temperature_std_good = 6.300381;
float motor_current_std_good = 2.270312;
float comp_std_good = 0.353378;
float dv_electric_std_good = 0.350890;
float towers_std_good = 0.258045;
float mpg_std_good = 0.357708;
float lps_std_good = 0.054684;
float pressure_switch_std_good = 0.092490;
float oil_level_std_good = 0.296994;
float caudal_impulses_std_good = 0.245016;

// Bad :(
float tp2_mean_bad = 8.112334;
float tp3_mean_bad = 8.288455;
float h1_mean_bad = 0.041005;
float dv_pressure_mean_bad = 1.859191;
float resevoirs_mean_bad = 8.289944;
float oil_temperature_mean_bad = 75.596562;
float motor_current_mean_bad = 5.530975;
float comp_mean_bad = 0.004805;
float dv_electric_mean_bad = 0.994528;
float towers_mean_bad = 0.502135;
float mpg_mean_bad = 0.004805;
float lps_mean_bad = 0.024291;
float pressure_switch_mean_bad = 0.994695;
float oil_level_mean_bad = 0.999333;
float caudal_impulses_mean_bad = 0.999333;

float tp2_std_bad = 0.994385;
float tp3_std_bad = 0.495652;
float h1_std_bad = 0.651141;
float dv_pressure_std_bad = 0.520527;
float resevoirs_std_bad = 0.495597;
float oil_temperature_std_bad = 2.931860;
float motor_current_std_bad = 0.374257;
float comp_std_bad = 0.069151;
float dv_electric_std_bad = 0.073772;
float towers_std_bad = 0.500004;
float mpg_std_bad = 0.069151;
float lps_std_bad = 0.153954;
float pressure_switch_std_bad = 0.072645;
float oil_level_std_bad = 0.025825;
float caudal_impulses_std_bad = 0.025825;

// This is an implementation of cmath's erfc function
// https://www.johndcook.com/cpp_phi.html
float phi(float x)
{
    // constants
    float a1 =  0.254829592;
    float a2 = -0.284496736;
    float a3 =  1.421413741;
    float a4 = -1.453152027;
    float a5 =  1.061405429;
    float p  =  0.3275911;

    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);

    // A&S formula 7.1.26
    float t = 1.0/(1.0 + p*x);
    float y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

    return 0.5*(1.0 + sign*y);
}

// Box Muller Method - https://stackoverflow.com/a/28551411
float generate_random_value(float mean, float stddev) {
    static float n2 = 0.0;
    static int n2_cached = 0;
    if (!n2_cached)
    {
        float x, y, r;
        do
        {
            x = 2.0*rand()/RAND_MAX - 1;
            y = 2.0*rand()/RAND_MAX - 1;

            r = x*x + y*y;
        }
        while (r == 0.0 || r > 1.0);
        {
            float d = sqrt(-2.0*log(r)/r);
            float n1 = x*d;
            n2 = y*d;
            float result = n1*stddev + mean;
            n2_cached = 1;
            return result;
        }
    }
    else
    {
        n2_cached = 0;
        return n2*stddev + mean;
    }
}

float calculate_probability(int day) {
    // This data is usually provided by the component manufacturer and is used to calculate the probability of failure... we don't have that.
    int days_mean = 10;
    int days_std = 1;

    float standardized_std = (day - days_mean) / days_std;
    return phi(standardized_std / sqrt(2)) / 2;  // Cumulative distribution function for a normal distribution
}

void grab_random_good(Data *data) {
    data->tp2 = generate_random_value(tp2_mean_good, tp2_std_good);
    data->tp3 = generate_random_value(tp3_mean_good, tp3_std_good);
    data->h1 = generate_random_value(h1_mean_good, h1_std_good);
    data->dv_pressure = generate_random_value(dv_pressure_mean_good, dv_pressure_std_good);
    data->resevoirs = generate_random_value(resevoirs_mean_good, resevoirs_std_good);
    data->oil_temperature = generate_random_value(oil_temperature_mean_good, oil_temperature_std_good);
    data->motor_current = generate_random_value(motor_current_mean_good, motor_current_std_good);
    data->COMP = generate_random_value(comp_mean_good, comp_std_good);
    data->dv_electric = generate_random_value(dv_electric_mean_good, dv_electric_std_good);
    data->towers = generate_random_value(towers_mean_good, towers_std_good);
    data->mpg = generate_random_value(mpg_mean_good, mpg_std_good);
    data->lps = generate_random_value(lps_mean_good, lps_std_good);
    data->pressure_switch = generate_random_value(pressure_switch_mean_good, pressure_switch_std_good);
    data->oil_level = generate_random_value(oil_level_mean_good, oil_level_std_good);
    data->caudal_impulses = generate_random_value(caudal_impulses_mean_good, caudal_impulses_std_good);
}

void grab_random_bad(Data *data) {
    data->tp2 = generate_random_value(tp2_mean_bad, tp2_std_bad);
    data->tp3 = generate_random_value(tp3_mean_bad, tp3_std_bad);
    data->h1 = generate_random_value(h1_mean_bad, h1_std_bad);
    data->dv_pressure = generate_random_value(dv_pressure_mean_bad, dv_pressure_std_bad);
    data->resevoirs = generate_random_value(resevoirs_mean_bad, resevoirs_std_bad);
    data->oil_temperature = generate_random_value(oil_temperature_mean_bad, oil_temperature_std_bad);
    data->motor_current = generate_random_value(motor_current_mean_bad, motor_current_std_bad);
    data->COMP = generate_random_value(comp_mean_bad, comp_std_bad);
    data->dv_electric = generate_random_value(dv_electric_mean_bad, dv_electric_std_bad);
    data->towers = generate_random_value(towers_mean_bad, towers_std_bad);
    data->mpg = generate_random_value(mpg_mean_bad, mpg_std_bad);
    data->lps = generate_random_value(lps_mean_bad, lps_std_bad);
    data->pressure_switch = generate_random_value(pressure_switch_mean_bad, pressure_switch_std_bad);
    data->oil_level = generate_random_value(oil_level_mean_bad, oil_level_std_bad);
    data->caudal_impulses = generate_random_value(caudal_impulses_mean_bad, caudal_impulses_std_bad);
}