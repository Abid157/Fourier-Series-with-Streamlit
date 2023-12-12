import sympy as sp
from colorsys import hsv_to_rgb
from sympy import fourier_series, pi, plot
from sympy.printing.latex import latex
from sympy.abc import x

# Streamlit App
import streamlit as st
st.title("Fourier Series Plotter")

try:
    st.write('Define a function on period ' + r'$[-\pi, \pi]$')
    f = st.text_input(label=r'$f(x) := $', value='1 - abs(x)/pi')
    f = sp.sympify(f)
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
a_n = sp.simplify(s.an.coeff(n))
st.latex('a(n) = ' + latex(a_n.as_coefficient(sp.cos(n*x))) if a_n else '0')
b_n = sp.simplify(s.bn.coeff(n))
st.latex('b(n) = ' + latex(b_n.as_coefficient(sp.sin(n*x)))if b_n else '0')

st.title("Fourier Series Approximation")
h = st.number_input("Number of Harmonics", min_value=1, max_value=100, value=3, step=1)
p = plot(f, s.truncate(n=h), (x, -pi, pi), show=False, legend=True)
p[0].line_color = 'black'
p[0].label='f(x)'
p[1].line_color = 'red'
p[1].label=f'Fourier Series with {h} harmonics'

p.show()
st.pyplot(p._backend.fig)

p = plot(*s[1:h+1], (x, -pi, pi), show=False, legend=True)
for i in range(h):
    r = i / h
    p[i].line_color = hsv_to_rgb(r, 1, 1)

st.write(f"{h} Harmonics:")
p.show()
st.pyplot(p._backend.fig)
