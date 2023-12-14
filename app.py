import numpy as np
from sympy import *
from sympy.abc import x
from sympy.printing.latex import latex
from matplotlib import pyplot as plt
from colorsys import hsv_to_rgb

# Streamlit App
import streamlit as st
st.header("Fourier Series and Frequency Spectrum")

with st.sidebar:
    try:
        st.write('Define a function on period ' + r"$[-\pi, \pi]$")
        f = st.text_input(label=r'$f(x) := $', value='Piecewise((1, x > 0), (-1, True))')
        f = simplify(sympify(f))
    except Exception as e:
        st.error(e)
        st.write("Could not parse function. Please try again.")
        f = Piecewise((1, x > 0), (-1, True))

    h = st.slider("Number of **Harmonics**", min_value=1, max_value=30, value=7, step=1)
    s = fourier_series(f, (x, -pi, pi))

tabs = st.tabs(["Fourier Series Approximation", "Fourier Series Plotter", "Fourier Series Harmonics", "Frequency Spectrum"])

with tabs[0]:
    # st.header("Fourier Series Approximation")
    st.write("**Function:**")
    st.latex('f(x) = ' + latex(f))
    st.write("**Coefficients:**")
    st.latex('a_0 = ' + latex(s.a0)) 
    n = symbols('n', real=True, positive=True, integer=True)
    an = s.an.coeff(n).as_coefficient(cos(n*x))
    st.latex(f"a(n) = {latex(simplify(an)) if an else 0}")
    bn = s.bn.coeff(n).as_coefficient(sin(n*x))
    st.latex(f"b(n) = {latex(simplify(bn)) if bn else 0}")
    st.write("**Fourier Series:**")
    st.latex('f(x) = ' + latex(s))

with tabs[1]:
    # st.header("Fourier Series Plotter")
    p = plot(f, s.truncate(n=h), (x, -pi, pi), show=False, legend=True)
    p[0].line_color = 'black'
    p[0].label='f(x)'
    p[1].line_color = 'red'
    p[1].label=f'Fourier Series with {h} harmonics'
    p.show()
    st.pyplot(p._backend.fig)

with tabs[2]:
    # st.header("Fourier Series Harmonics")
    p = plot(f, (x, -pi, pi), legend=True, show=False, label='f(x)', line_color='black')
    for i in range(1, h + 1):
        p.append(plot(s[i - 1], (x, -pi, pi), line_color=hsv_to_rgb(i / h, 1, 1))[0])
    p.show()
    st.pyplot(p._backend.fig)

with tabs[3]:
    # st.header("Frequency Spectrum")
    an, bn, cn = [s.a0], [0], [s.a0]
    for i in range(1, h + 1):
        a = Abs(s.an.coeff(i).subs(x, 0))
        b = Abs(s.bn.coeff(i).subs(x, pi/(2*i)))
        c = sqrt(a*a + b*b)
        an.append(a)
        bn.append(b)
        cn.append(c)
    x = np.arange(h + 1)
    width = 0.25
    fig, ax = plt.subplots()
    ax.bar(x - width, an, width, label='$a_n$')
    ax.bar(x + width, bn, width, label='$b_n$')
    ax.bar(x, cn, width, label='$c_n = \sqrt{a_n^2 + b_n^2}$')
    ax.set_xlabel('n')
    ax.set_ylabel('Amplitude')
    ax.set_title('Frequency Spectrum')
    ax.legend()
    st.pyplot(fig)
