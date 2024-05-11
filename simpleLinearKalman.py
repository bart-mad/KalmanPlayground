# Simple Linear Kalman Filter
# Python implementation -> For .cpp version training
#--------------------------------------------------------------
# V 1.0
# BM
# 2024/05/11
#--------------------------------------------------------------
# Imports
from numpy.random import randn
from math import sqrt
import matplotlib.pyplot as plt
from numpy import linspace

# Global simulation settings
simulation_steps = 500
dt = 0.5

# "True" object model data
x0 = 0.
v = 1.
process_variance = 0.01 # Variability in the speed of tracked object

# Simulation timestamp vector
Time = linspace(0,(simulation_steps-1) * dt,simulation_steps)

# Calculate process noise 
process_noise = sqrt(process_variance)

# Calculate true position based on the motion model
X_real = [x0]
for i in range(simulation_steps-1):
    v = v + process_noise * randn() * dt
    x0 = X_real[i] + v * dt
    X_real.append(x0)

# Measurement model
measurement_variance = 100.
measurement_noise = sqrt(measurement_variance)

X_measured = []

# Append measurement samples with noise
for i in range(simulation_steps):
    X_measured.append(X_real[i] + randn()*measurement_noise)

# KALMAN FILTER IMPLEMENTATION
# Initial state estimate
x0 = 1.
v_model = 0.6
model_variance = 3

# KF Update function
def update(x_prior,prior_variance,x_measured,measurement_variance):
    x_posterior = (prior_variance * x_measured + measurement_variance * x_prior)/(prior_variance + measurement_variance)
    posterior_variance = (prior_variance * measurement_variance)/(prior_variance + measurement_variance)
    return x_posterior, posterior_variance

# KF Predict function
def predict(x_prior,prior_variance,velocity,dt,model_variance):
    x_predicted = x_prior + velocity*dt
    prediction_variance = prior_variance + model_variance
    return x_predicted, prediction_variance

# Calculate the estimates
result = []
#Update step 0 - initialize the KF
x_predict, x_variance = update(x0,model_variance,X_measured[0],measurement_variance)
result.append(x_predict)

#Main loop
for i in range(1,simulation_steps):
    # Predict
    x_prior, prior_variance = predict(x_predict, x_variance,v_model,dt,model_variance)
    # Update
    x_predict, x_variance = update(x_prior,prior_variance,X_measured[i],measurement_variance)
    #Append result
    result.append(x_predict)

# Plots
plt.scatter(Time,X_real,color='r',label='Real')
plt.scatter(Time,X_measured,color='b',label='Measurement')
plt.scatter(Time,result,color='g',label='Kalman')

plt.xlabel("Time / s")
plt.ylabel("Position / m")

plt.legend()
plt.show()