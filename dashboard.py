import streamlit as st
import pandas as pd
import numpy as np

def Dashboard(mydb):
    card_1, card_2, card_3 = st.columns(3)
    card_1.metric("Rooms Occupied ", "30", "-10%")
    card_2.metric("Expected Arrivals", "9", "-8%")
    card_3.metric("Expected Departure", "5", "4%")

    st.divider()
    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.line_chart(chart_data)

    with fig_col2:
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=["a", "b", "c"])
        st.bar_chart(chart_data)