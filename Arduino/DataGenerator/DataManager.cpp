#include "DataManager.h"

float tp2_mean_good = -0.012789;
float tp3_mean_good = 9.004420;
float h1_mean_good = 8.976129;
float dv_pressure_mean_good = -0.020247;
float resevoirs_mean_good = 9.005358;
float oil_temperature_mean_good = 61.941475;
float motor_current_mean_good = 1.348828;
float comp_mean_good = 1.000000;
float dv_electric_mean_good = 0.000000;
float towers_mean_good = 1.000000;
float mpg_mean_good = 1.000000;
float lps_mean_good = 0.000000;
float pressure_switch_mean_good = 1.000000;
float oil_level_mean_good = 1.000000;
float caudal_impulses_mean_good = 1.000000;

float tp2_mean_bad = 8.295938;
float tp3_mean_bad = 8.441677;
float h1_mean_bad = -0.007271;
float dv_pressure_mean_bad = 1.848049;
float resevoirs_mean_bad = 8.442984;
float oil_temperature_mean_bad = 75.447403;
float motor_current_mean_bad = 5.587233;
float comp_mean_bad = 0.000000;
float dv_electric_mean_bad = 1.000000;
float towers_mean_bad = 0.500000; // 50/50 chance of 1 or 0
float mpg_mean_bad = 0.000000;
float lps_mean_bad = 0.000000;
float pressure_switch_mean_bad = 1.000000;
float oil_level_mean_bad = 1.000000;
float caudal_impulses_mean_bad = 1.000000;

float tp2_std_good = 0.002873;
float tp3_std_good = 0.578056;
float h1_std_good = 0.710397;
float dv_pressure_std_good = 0.003325;
float resevoirs_std_good = 0.577210;
float oil_temperature_std_good = 5.968513;
float motor_current_std_good = 1.783266;
float comp_std_good = 0.000000;
float dv_electric_std_good = 0.000000;
float towers_std_good = 0.000000;
float mpg_std_good = 0.000000;
float lps_std_good = 0.000000;
float pressure_switch_std_good = 0.000000;
float oil_level_std_good = 0.000000;
float caudal_impulses_std_good = 0.000000;

float tp2_std_bad = 0.863746;
float tp3_std_bad = 0.596259;
float h1_std_bad = 0.003422;
float dv_pressure_std_bad = 0.481578;
float resevoirs_std_bad = 0.595944;
float oil_temperature_std_bad = 2.496217;
float motor_current_std_bad = 0.204016;
float comp_std_bad = 0.000000;
float dv_electric_std_bad = 0.000000;
float towers_std_bad = 0.500000; // 50/50 chance of 1 or 0
float mpg_std_bad = 0.000000;
float lps_std_bad = 0.000000;
float pressure_switch_std_bad = 0.000000;
float oil_level_std_bad = 0.000000;
float caudal_impulses_std_bad = 0.000000;

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

float calculate_probability(int iteration) {
    // This data is usually provided by the component manufacturer and is used to calculate the probability of failure... we don't have that.
    int iterations_mean = 864; // 864 iterations is 3 days of data (Data is generated every 5 minutes)
    int iterations_std = 12; // 3 days +/- 1 hour.

    float standardized_std = (iteration - iterations_mean) / iterations_std;
    return phi(standardized_std / sqrt(2)) / 2;  // Cumulative distribution function for a normal distribution
}

// This function is used to clamp the towers value to 0 or 1.
// If the value is less than 0.5, it will be clamped to 0. Otherwise, it will be clamped to 1.
float clamp_towers(float towers) {
    if (towers < 0.5) {
        return 0.0;
    }

    return 1.0;
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
    data->towers = clamp_towers(generate_random_value(towers_mean_bad, towers_std_bad));
    data->mpg = generate_random_value(mpg_mean_bad, mpg_std_bad);
    data->lps = generate_random_value(lps_mean_bad, lps_std_bad);
    data->pressure_switch = generate_random_value(pressure_switch_mean_bad, pressure_switch_std_bad);
    data->oil_level = generate_random_value(oil_level_mean_bad, oil_level_std_bad);
    data->caudal_impulses = generate_random_value(caudal_impulses_mean_bad, caudal_impulses_std_bad);
}