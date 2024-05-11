# Simple script for plotting .cpp Kalman Filter results
import matplotlib.pyplot as plt
from pandas import read_csv
from numpy import linspace

rawData = read_csv("kf_result.csv")

Time = linspace(0,rawData.shape[0]-1,rawData.shape[0])
X_real = rawData.iloc[:,0]
X_measured = rawData.iloc[:,1]
result = rawData.iloc[:,2]

# Plots
plt.scatter(Time,X_real,color='r',label='Real')
plt.scatter(Time,X_measured,color='b',label='Measurement')
plt.scatter(Time,result,color='g',label='Kalman')

plt.xlabel("Time / s")
plt.ylabel("Position / m")

plt.legend()
plt.show()