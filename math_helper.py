# Helper scripts for symbolic calculations
from sympy import (init_printing, Matrix, MatMul, 
                   integrate, symbols)
# Initialize output formating
init_printing(use_latex='mathjax')
# Get dt and Phi symbols
dt, phi = symbols('\Delta{t} \Phi_s')
# dt - Time step
# Phi - white noise

# Symbolic state matrix
F = Matrix([[1, dt],
            [0, 1]])
# Continous White Noise matrix
Q_c = Matrix([[0, 0],
              [0, 1]]) * phi

Q_continous = integrate(F * Q_c * F.T, (dt, 0, dt))

# Discrete Noise Matrix
Theta = Matrix([[0.5 * dt**2], [dt]])
# Variance std**2
var = symbols('sigma^2_v')

Q_discrete = Theta * var * Theta.T

print(Q_discrete)