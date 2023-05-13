import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
import datetime


#SideBar
with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard", 'Rooms', 'Reservation', 'Guest', 'Inventory', 'Staff'], 
        icons=['kanban-fill', 'grid-1x2-fill', 'calendar-check-fill', 'people-fill', 'house-fill', 'person-lines-fill'], 
        menu_icon="cast", 
        default_index=0,    
        styles={
        "container": {"padding": "0!important", "background-color": "#f1f2f6"},
    })

if selected == "Dashboard":
    # create three columns for cards
    card1, card2, card3 = st.columns(3)
    card1.metric("Rooms Occupied ", "30", "-10%")
    card2.metric("Expected Arrivals", "9", "-8%")
    card3.metric("Expected Departure", "5", "4%")
    
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
elif selected == "Rooms":
    st.write("Rooms")
elif selected == "Reservation":
    st.write("Reservation")
elif selected == "Guest":
    st.write("Guest")
elif selected == "Inventory":
    tab1, tab2 = st.tabs(["**View inventory**", "**Add an item**"])
    with tab1:
        df = pd.DataFrame({'Item': ["Clothings", "Foods", "Bottle of water", "Pillows", "Shoes", "Towels"], 'Total': [60, 30, 20,60, 30, 20], 'Remaining': [30, 15, 10, 30, 15, 10]})
        grid_return = AgGrid(df, 
                             editable=True,
                             fit_columns_on_grid_load = True, 
                             enable_quicksearch = True,
                             reload_data = True)

    with tab2:
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>Add a new item</h3>
        ''', unsafe_allow_html=True)
        with st.expander('', expanded=True):
            item_name = st.text_input('Item name', 'Enter the item name')
            col1, col2 = st.columns(2)
            with col1:
                total = st.slider('Total', 0, 150, 25)
            with col2 :
                price = st.number_input("Price per item", 20000)
                _, _, _, _, _, col6 = st.columns(6)
                with col6:
                    st.button("Add") 
else:
    tab1, tab2 = st.tabs(["**View staff information**", "**Add a staff**"])
    with tab1:
        df = pd.DataFrame({'Name': ["Le Chi Thinh", "Huynh Cong Thien", "Nguyen Minh Tri"], 
                           'Phone': ["0822043153", "0822033134", "0822098123"], 
                           'Email': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com"],
                           "Date Of Birth": ["12/5/2003", "15/5/2003", "16/5/2002"], 
                           "Roles": ["FrontDesk", "Manager", "Staff"]})
        grid_return = AgGrid(df, 
                             editable=True,
                             fit_columns_on_grid_load = True, 
                             enable_quicksearch = True,
                             reload_data = True)

    with tab2:
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>Add a staff</h3>
        ''', unsafe_allow_html=True)
        with st.expander('', expanded=True):
            item_name = st.text_input('Staff Name', 'Enter the item name')
            d = st.date_input(
            "Date of birth",
            datetime.date(2003, 5, 12))
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input('Phone Number', 'Enter phone number')
            with col2 :
                email = st.text_input('Email', 'Enter email')
                _, _, _, _, _, col6 = st.columns(6)
                with col6:
                    st.button("Add") 
        
