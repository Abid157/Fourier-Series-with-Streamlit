import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

# Streamlit App
import streamlit as st
st.title("Fourier Series Plotter")
h = st.number_input("Number of Harmonics", min_value=1, max_value=100, value=10, step=1)

# Generate x values
N = 1000
x = np.linspace(-np.pi, np.pi, N)

# Define the function to be approximated with its Fourier series
original_function = lambda x: np.array([1 if 2 * abs(i) < np.pi else -1 for i in x])

# Fourier coefficients Definition
a0 = 0
a = lambda n: 4 * (1j ** n).imag / (n * np.pi)
b = lambda n: 0
coefficients = [a0] + [(a(n), b(n)) for n in range(1, h + 1)]

# Calculate Fourier series coefficients for the given function
def fourier_coefficients(func, n_terms=10):
    a0 = np.trapz(func, dx=2 * np.pi / N) / (2 * np.pi)
    coefficients = [a0]
    for n in range(1, n_terms + 1):
        an = np.trapz(func * np.cos(n * x), dx=2 * np.pi / N) / np.pi
        bn = np.trapz(func * np.sin(n * x), dx=2 * np.pi / N) / np.pi
        coefficients.append((an, bn))
    return coefficients

# coefficients = fourier_coefficients(original_function(x), n_terms=h)

# Reconstruct the function using its Fourier series expansion
def fourier_series(coefficients, x):
    series = coefficients[0]
    for n, (an, bn) in enumerate(coefficients[1:], start=1):
        series += an * np.cos(n * x) + bn * np.sin(n * x)
    return series

reconstructed_function = fourier_series(coefficients, x)

# Create a single figure and plot both the original function and Fourier series approximation
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the original function
ax.plot(x, original_function(x), label='Original Function', color='blue')

# Plot the Fourier series approximation on the same axes
ax.plot(x, reconstructed_function, label=f'Fourier Series with {h} harmonics', color='red')

ax.set_xlabel('$\omega_1$t')
ax.set_ylabel('f($\omega_1$t)')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda val, pos: f'${val / np.pi: .1f}\pi$' if val != 0 else '0')
)
ax.xaxis.set_major_locator(MultipleLocator(base=np.pi / 2))
ax.xaxis.set_major_locator(MultipleLocator(base=np.pi / 2))
ax.legend()

st.pyplot(fig)

st.title("Using sympy")
import sympy as sp
from sympy import fourier_series, pi, plot
from sympy.abc import x

# Define the function to be approximated with its Fourier series
f = sp.Piecewise((1, 2*x < pi and 2*x > -pi), (-1, True))

s = fourier_series(f, (x, -pi, pi))
s_i = [s.truncate(n=i) - s.truncate(n=i-1) for i in range(1, h + 1)]
p = plot(f, *s_i, (x, -pi, pi), line_color=lambda x: 2*x, show=False, legend=True)

for i in range(1, h + 1):
    p[i].label = f"n = {i}"

p.show()
st.pyplot(p._backend.fig)