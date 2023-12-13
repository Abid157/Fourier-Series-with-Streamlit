import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from colorsys import hsv_to_rgb
from sympy import fourier_series, pi, plot
from sympy.printing.latex import latex
from sympy.abc import x

# Streamlit App
import streamlit as st
st.title("Fourier Series Approximation")

try:
    st.write('Define a function on period ' + r'$[-\pi, \pi]$')
    f = st.text_input(label=r'$f(x) := $', value='1 - abs(x)/pi')
    f = sp.simplify(sp.sympify(f))
except Exception as e:
    st.error(e)
    st.write("Could not parse function. Please try again.")
    f = 1 - sp.Abs(x)/pi

s = fourier_series(f, (x, -pi, pi))

st.write("Function:")
st.latex('f(x) = ' + latex(f))
st.write("Fourier Series:")
st.latex('f(x) = ' + latex(s))
st.write("Coefficients:")
st.latex('a_0 = ' + latex(s.a0)) 
n = sp.symbols('n', real=True, positive=True, integer=True)
an = sp.simplify(s.an.coeff(n)).as_coefficient(sp.cos(n*x))
st.latex(f"a(n) = {latex(an) or 0}")
bn = sp.simplify(s.bn.coeff(n)).as_coefficient(sp.sin(n*x))
st.latex(f"b(n) = {latex(bn) or 0}")

st.title("Fourier Series Plotter")
h = st.number_input("Number of Harmonics", min_value=1, max_value=100, value=3, step=1)
p = plot(f, s.truncate(n=h), (x, -pi, pi), show=False, legend=True)
p[0].line_color = 'black'
p[0].label='f(x)'
p[1].line_color = 'red'
p[1].label=f'Fourier Series with {h} harmonics'

p.show()
st.pyplot(p._backend.fig)

st.title("Fourier Series Harmonics")
p = plot(f, (x, -pi, pi), show=False, legend=True, label='f(x)', line_color='black')
i = 0
while i < h:
    if s[i]:
        p.append(plot(s[i], (x, -pi, pi), line_color=hsv_to_rgb(i / h, 1, 1))[0])
    else:
        continue
    i += 1

p.show()
st.pyplot(p._backend.fig)

an, bn, cn = [], [], []
for i in range(1, h + 1):
    a = abs(s.an.coeff(i).subs(x, 0))
    b = s.bn.coeff(i).subs(x, pi/(2*i))
    c = sp.sqrt(a*a + b*b)
    an.append(a)
    bn.append(b)
    cn.append(c)

x = np.arange(h)
width = 0.3
multiplier = 0

fig, ax = plt.subplots()

ax.bar(x - width, an, width, label='$a_n$')
ax.bar(x, bn, width, label='$b_n$')
ax.bar(x + width, cn, width, label='$c_n$')

ax.set_ylabel('Amplitude')
ax.set_title('Frequency Spectrum')
ax.legend()

st.title("Frequency Spectrum")
st.pyplot(fig)
