import streamlit as st

def DisplayTextCenter(TextContent):
    return st.markdown(f'''
            <h3 style='text-align: center;  color: black;'>{TextContent}</h3>
            ''', unsafe_allow_html=True)


def AddFourRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
    row_4_1, row_4_2 = st.columns(2)
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2], [row_4_1, row_4_2]]
    return rows_columns 

def AddThreeRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
  
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2]]
    return rows_columns 

def AddFiveRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
    row_4_1, row_4_2 = st.columns(2)
    row_5_1, row_5_2 = st.columns(2)
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2], [row_4_1, row_4_2], [row_5_1, row_5_2]]
    return rows_columns 