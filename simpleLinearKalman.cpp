#include <iostream>
#include <cmath>
#include <vector>
#include <random> 
#include <fstream>

struct Gaussian{
    double mean;
    double variance;
};

Gaussian update(double x_prior, double prior_variance, double x_measured, double measurement_variance)
{
    Gaussian posterior;
    posterior.mean = (prior_variance * x_measured + measurement_variance * x_prior)/(prior_variance + measurement_variance);
    posterior.variance = (prior_variance * measurement_variance)/(prior_variance + measurement_variance);

    return posterior;
}

Gaussian predict(double x_prior,double prior_variance, double velocity,double dt, double model_variance)
{   
    Gaussian predicted;
    predicted.mean = x_prior + velocity*dt;
    predicted.variance = prior_variance + model_variance;

    return predicted;
}

int main()
{
    // SET THE RANDOM GENERATOR SEED
    // Use current time as seed for random generator 
    srand(time(0)); 

    // GLOBAL SIMULATION SETTINGS
    constexpr double SIMULATION_STEPS{500};
    constexpr double dt{0.5};

    // OBJECT MOTION MODEL SETTINGS
    constexpr double x0{0.};
    constexpr double v0{1.};
    constexpr double PROCESS_VARIANCE{0.01};

    // SIMULATION TIMESTAMP VECTOR
    // PLACEHOLDER, I dont think I need this

    // TRUE OBJECT POSITION
    constexpr double PROCESS_NOISE{sqrt(PROCESS_VARIANCE)};

    //std::cout << "Process noise estimated at: " << PROCESS_NOISE << std::endl;

    // CALCULATE TRUE POSITIONS BASED ON MOTION MODEL
    // Initialize the result vector
    std::vector<double> X_real(SIMULATION_STEPS);

    // Set the first position to x0
    X_real[0] = x0;
    // Assign all the other elements
    double v{v0};

    // Get random double in range of 1. to -1.
    // Courtesy of Alessandro Jacopson
    // STACKOVERFLOW Q. 2704521
    std::uniform_real_distribution<double> unif(-1.,1.);
    std::default_random_engine re;

    for (int i{1};i<=SIMULATION_STEPS;i++)
        {
            v = v + PROCESS_NOISE * unif(re) * dt;
            X_real[i] = X_real[i-1] + v * dt;

        }

    // MEASUREMENT MODEL
    constexpr double MEASUREMENT_VARIANCE{100.};
    constexpr double MEASUREMENT_NOISE{sqrt(MEASUREMENT_VARIANCE)};
    // VECTOR WITH MEASURED SAMPLES
    std::vector<double> X_measured(SIMULATION_STEPS);

    // GENERATE MEASUREMENT WITH NOISE
    for (int i{0};i<=SIMULATION_STEPS;i++)
    {
        X_measured[i] = X_real[i] + unif(re) * MEASUREMENT_NOISE;

    }

    // KALMAN FILTER IMPLEMENTATION
    // Initial state estimate
    double x_prior{1.};
    constexpr double V_MODEL{0.5};
    constexpr double MODEL_VARIANCE{3.};

    // Initialize the output vector
    std::vector<double> X_result(SIMULATION_STEPS);

    // Step 0 - Initial step as predicted value, update KF output
    Gaussian posterior;
    Gaussian prior;

    posterior = update(x_prior,MODEL_VARIANCE,X_measured[0],MEASUREMENT_VARIANCE);

    X_result[0] = posterior.mean;

    // SET THE PRIOR TO THE POSTERIOR FROM PREVIOUS STEP
    prior = posterior;

    for (int i{1};i<=SIMULATION_STEPS;i++)
    {
        prior = predict(prior.mean,prior.variance,V_MODEL,dt,MODEL_VARIANCE);
        posterior = update(prior.mean,prior.variance,X_measured[i],MEASUREMENT_VARIANCE);
        // Append the result
        X_result[i] = posterior.mean;
        // UPDATE NEW PRIOR
        prior = posterior;
    } 

    // CONSOLE FORMATTING
    std::cout<<" KALMAN FILTERING RESULT "<<std::endl;

    // Save the output for python plotting
    std::ofstream outputFile;
    outputFile.open ("kf_result.csv");

    for (int i{1};i<=SIMULATION_STEPS;i++)
        {
            std::cout << "Real position is: " << X_real[i] <<" | Measured: "<<X_measured[i]<<" | Predicted: "<<X_result[i]<<std::endl;
            outputFile << X_real[i] <<","<<X_measured[i]<<","<<X_result[i]<<"\n";
        }

    outputFile.close();

}