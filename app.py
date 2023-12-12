import sympy as sp
from sympy import fourier_series, pi, plot, S
from sympy.printing.latex import latex
from sympy.abc import x

# Streamlit App
import streamlit as st
st.title("Fourier Series Plotter")
h = st.number_input("Number of Harmonics", min_value=1, max_value=100, value=10, step=1)

f =  S(1)/2 - sp.Abs(x)/pi
s = fourier_series(f, (x, -pi, pi))

st.write("Function:")
st.latex('f(x) = ' + latex(f))
st.write("Fourier Series:")
st.latex('f(x) = ' + latex(s))
st.write("Coefficients:")
st.latex('a_0 = ' + latex(s.a0)) 
n = sp.symbols('n', real=True, positive=True, integer=True)
a_n = sp.simplify(s.an.coeff(n))
st.latex('a(n) = ' + latex(a_n.as_coefficient(sp.cos(n*x))))
b_n = sp.simplify(s.bn.coeff(n))
st.latex('b(n) = ' + latex(b_n.as_coefficient(sp.sin(n*x))))

p = plot(f, *s[:h], (x, -pi, pi), line_color=lambda x: 2*x, show=False, legend=True)
for i in range(h):
    p[i].label = f"n = {i}"

p.show()
st.pyplot(p._backend.fig)
