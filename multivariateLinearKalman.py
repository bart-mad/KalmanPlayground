# MULTIVARIATE LINEAR KALMAN FILTERING TEST
# Tracking position and velcoity of an object along one axis
# -----------------------------------------------------------
# 2025/05/12
# BM
# V1.0
#------------------------------------------------------------
# Imports
from numpy import array
from math import sqrt
import matplotlib.pyplot as plt
from numpy.random import randn
from numpy import linspace
from numpy import matmul

# Global simulation settings
dt = 1.
N_sample = 500
T = linspace(0,N_sample*dt,N_sample)

# Object simulation model (True trajectory)
# True object initial position
True_x0 = 0.
True_v0 = 1.
Model_variance = 0.0005
Model_std = sqrt(Model_variance)

# Calculate true object trajectory
# Initialize true position and velocity vectors, start at initial conditions
X_True = []
X_True.append(True_x0)
V_True = []
V_True.append(True_v0)
# Loop over simulation steps
for i in range(1,N_sample,1):
    # Update position
    X_True.append(X_True[i-1] + V_True[i-1]*dt)
    # Update speed
    V_True.append(V_True[i-1] + randn()*Model_std)


# Position measurement model
Measurement_variance = 4000.
Measurement_std = sqrt(Measurement_variance)
X_Measured = []
# Calculate measurement samples
for i in range(N_sample):
    X_Measured.append(X_True[i] + randn()*Measurement_std)

# KALMAN FILTER IMPLEMENTATION
# STATE SPACE MODEL
# Initialization
x0 = 0.5
v0 = 0.5
# State matrix X [2X1]
X = array([[x0],
           [v0]])

# Covariance matrix P [2x2]
position_variance = 10.
velocity_variance = 10.
covariance = 0.
P = array([[position_variance, covariance],
           [covariance, velocity_variance]])


# State transition matrix F [2x2]
# Analyticaly solved for this specific problem
F = array([[1., dt],
           [0., 1]])


# PROCESS NOISE MATRIX
# Assumes the Discrete White Noise Model
Noise_Variance = 2.35

# Noise Matrix - Hard Coded for 1st order motion eq. - see derivative in math_helper.py
Q = array([[0.25*pow(dt,4)*Noise_Variance, 0.5*pow(dt,3)*Noise_Variance], 
            [0.5*pow(dt,3)*Noise_Variance, pow(dt,2)*Noise_Variance]])


print("debug")
X_pred = matmul(F,X)
X_pred = matmul(F,X_pred)
X_pred = matmul(F,X_pred)
X_pred = matmul(F,X_pred)


# Plotting/Debug/Test
#plt.plot(X_True)
#plt.show()
#plt.plot(V_True)
#plt.show()
plt.scatter(X_Measured,X_True)
plt.show()
plt.scatter(T,X_True)
plt.scatter(T,X_Measured)
plt.show()
