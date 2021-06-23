import streamlit as st
import sympy
import math
import numpy as np
import antlr4
from sympy import symbols
from PIL import Image
import pandas as pd
from sympy.parsing.latex import parse_latex
from pandas import Series


def left_int(y, x1, x2, delta_x):
    x = symbols('x')
    tracker = x1
    expr = parse_latex(y)
    sum = 0
    while tracker < x2:
        sum += expr.evalf(subs={x: tracker}) * delta_x
        tracker += delta_x
    return sum
def right_int(y, x1, x2, delta_x):
    x = symbols('x')
    tracker = x1 + delta_x
    expr = parse_latex(y)
    sum = 0
    while tracker <= x2:
        sum += expr.evalf(subs={x: tracker}) * delta_x
        tracker += delta_x
    return sum


def mid_int(y, x1, x2, delta_x):
    x = symbols('x')
    expr = parse_latex(y)
    tracker = (2 * x1 + delta_x) / 2
    sum = 0
    while tracker < x2:
        sum += expr.evalf(subs={x: tracker}) * delta_x
        tracker += delta_x
    return sum


def trap_int(y, x1, x2, delta_x):
    x = symbols('x')
    expr = parse_latex(y)
    tracker = x1
    sum = 0
    while tracker < x2:
        y1 = expr.evalf(subs={x: tracker})
        tracker += delta_x
        y2 = expr.evalf(subs={x: tracker})
        sum += 1/2 * delta_x * (y1 + y2)
    return sum

def switcher(kind, y, x1, x2, delta_x):
    switch = {
        1: right_int(y, x1, x2, delta_x),
        2: left_int(y, x1, x2, delta_x),
        3: mid_int(y, x1, x2, delta_x),
        4: trap_int(y, x1, x2, delta_x)
    }
    st.text(switch.get(kind, "Invalid input."))


def num_int():
    y = input("Input the integrand.")
    x1 = float(input("Input the lower limit of integration"))
    x2 = float(input("Input the upper limit of integration"))
    intervals = int(input("Input desired number of intervals. \nThe more intervals, the more accurate the numerical approximation will be."))
    kind = int(input("Input desired kind of numerical integration. \n1 for a right hand sum, 2 for a left hand sum, 3 for a midpoint sum, 4 for a trapezoidal sum."))
    delta_x = (x2 - x1) / intervals
    switcher(kind, y, x1, x2, delta_x)

st.set_page_config(layout="wide")
st.title("Numerical Integrator")
col1, col2 = st.beta_columns([2, 3])
with col1:
    img = Image.open("Maxwell'sEquationsImage.jpg")
    st.write("Stuck on a tough integral? Turn to Sam's numerical integration calculator."
            + " Input the integrand in terms of the variable x. Any constants must be numerical (like 1.23), not variable (like 'a')."
              + " If you don't know LaTeX, visit [this](https://www.overleaf.com/learn/latex/Mathematical_expressions#Reference_guide) link for a brief introduction.")
    st.image(img, caption = "Not even this calculator is more beautiful than Maxwell's Equations.", width = None, use_column_width='always', clamp=False, channels = 'RGB', output_format = 'auto')


def UI():
    with col2:
        with st.form("Integrate"):
            y = st.text_input("Integrand (as it would be typed in LaTeX):")
            x1 = st.number_input("Lower limit of integration:")
            x2 = st.number_input("Upper limit of integration:")
            intervals = st.number_input("Number of intervals:")
            str_kind = st.selectbox("Approximation type:", options=["Right Hand", "Left Hand", "Midpoint", "Trapezoidal"])
            submitted1 = st.form_submit_button(label="Submit")
            if submitted1 and y != "" and x1 < x2 and intervals > 0 and str_kind != "":
                delta_x = (x2 - x1) / intervals
                if str_kind == "Right Hand":
                    result = right_int(y, x1, x2, delta_x)
                elif str_kind == "Left Hand":
                    result = left_int(y, x1, x2, delta_x)
                elif str_kind == "Midpoint":
                    result = mid_int(y, x1, x2, delta_x)
                else:
                    result = trap_int(y, x1, x2, delta_x)
                st.latex(r'''\int_{''' + str(x1) + r'''}^{'''+ str(x2) + r'''}{''' + y + r'''\,dx} \approx ''' + str(result))

    with st.form(key="Experiment"):
        st.header("Experiment with Approximation Quality")
        # insert statement about how to use this
        max_num_ints = st.number_input("Maximum number of intervals to test: ")
        delta_ints = st.number_input("Change in number of intervals between tests (this number must divide evenly into the maximum number of intervals): ")
        submitted2 = st.form_submit_button(label="Submit")
        if submitted2 and max_num_ints > 0 and delta_ints > 0 and y != "" and x1 < x2:
            num_ints = delta_ints
            interval_list = list()
            right_list = list()
            left_list = list()
            mid_list = list()
            trap_list = list()
            while num_ints <= max_num_ints:
                delx = (x2-x1)/num_ints
                interval_list.append(num_ints)
                right_list.append(right_int(y, x1, x2, delx))
                left_list.append(left_int(y, x1, x2, delx))
                mid_list.append(mid_int(y, x1, x2, delx))
                trap_list.append(trap_int(y, x1, x2, delx))
                num_ints += delta_ints
            df = pd.DataFrame()
            #df.insert(0, "Number of Intervals", interval_list)
            df["Number of Intervals"] = interval_list
            df["Left Hand"] = left_list
            df["Right Hand"] = right_list
            df["Midpoint"] = mid_list
            df["Trapezoidal"] = trap_list
            #df.insert(1, "Right Hand", right_list)
            #df.insert(2, "Left Hand", left_list)
            #df.insert(3, "Midpoint", mid_list)
            #df.insert(4, "Trapezoidal", trap_list)

            st.dataframe(df)
            st.line_chart(df)


UI()
