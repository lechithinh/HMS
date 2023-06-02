import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
import datetime
from streamlit_extras.stateful_button import button
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards
import time


st.set_page_config(layout="wide")

# SideBar
with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard", 'Rooms', 'Reservation', 'Guest', 'Inventory', 'Staff'],
                           icons=['kanban-fill', 'grid-1x2-fill', 'calendar-check-fill',
                                  'people-fill', 'house-fill', 'person-lines-fill'],
                           menu_icon="cast",
                           default_index=0,
                           styles={
        "container": {"padding": "0!important", "background-color": "#f1f2f6"},
    })

if selected == "Dashboard":
    # create three columns for cards
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
elif selected == "Rooms":
    tab1, tab2 = st.tabs(["**VIEW ROOM INFORMATION**", "**ADD A ROOM**"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Gain", value=5000, delta=1000)
        col2.metric(label="Loss", value=5000, delta=-1000)
        col3.metric(label="No Change", value=5000, delta=0)
        style_metric_cards(border_left_color='#F39D9D')

        def updatedata():
            # Update the database
            pass

        seeding_data = {"Edit": [False, False, False, False, False, False, False],
                        'Room ID': ["101", "102", "103", "104", "105", "106", "107"],
                        'Room Name': ["VIP1", "VIP2", "VIP3", "VIP4", "VIP5", "VIP6", "VIP7"],
                        'Type': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        'Number of beds': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        'Floor': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        "Status": ["12/5/2003", "15/5/2003", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002"],
                        "Price": ["FrontDesk", "Manager", "Staff", "Staff", "Staff", "Staff", "Staff"]}

        # show the table
        key = st.experimental_data_editor(
            seeding_data, on_change=updatedata)  # cal function back

        # Display the detail data
        count = 0
        for value in key['Edit']:
            if value:
                count += 1
                if count == 1:
                    index = key['Edit'].index(value)
                    with st.expander("", expanded=True):
                        column1, column2 = st.columns(2)
                        with column1:
                            card(
                                title=key['Room ID'][index],
                                text=key['Floor'][index],
                                image="http://placekitten.com/300/250",
                                url="https://www.google.com",
                            )
                        with column2:

                            st.subheader(
                                f"ROOM ID: :blue[{key['Room ID'][index]}]")
                            row_1_1, row_1_2 = st.columns(2)
                            row_2_1, row_2_2 = st.columns(2)
                            row_3_1, row_3_2 = st.columns(2)
                            with row_1_1:
                                room_name = st.text_input(
                                    "Room name", f"{key['Room Name'][index]}")
                                # st.caption(
                                #     f"Room Name")
                            with row_1_2:
                                type_room = st.text_input(
                                    'Room type', f"{key['Type'][index]}")
                            with row_2_1:
                                floor = st.text_input(
                                    "Floor", f"{key['Floor'][index]}")
                            with row_2_2:
                                status = st.selectbox(
                                    "Status", ("Vacant", "Occupied"))
                            with row_3_1:
                                num_bed = st.text_input(
                                    "Number of bed", f"{key['Number of beds'][index]}")
                            with row_3_2:
                                price = st.text_input(
                                    "Price", f"{key['Price'][index]}")

                            # st.caption(f"Type: :blue[{key['Type'][index]}]")
                            # st.caption(
                            #     f"Number of beds: :blue[{key['Number of beds'][index]}]")
                            # st.caption(f"Price: :blue[{key['Price'][index]}]")
                else:
                    alert = st.error("You must select one room", icon="🚨")
                    time.sleep(3)
                    alert.empty()

    with tab2:
        isNoti = False
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>ADD A NEW ROOME</h3>
        ''', unsafe_allow_html=True)
        with st.expander('', expanded=True):
            row_1_1, row_1_2 = st.columns(2)
            row_2_1, row_2_2 = st.columns(2)
            row_3_1, row_3_2 = st.columns(2)
            with row_1_1:
                item_name = st.text_input('Staff Name', 'Enter the item name')
            with row_1_2:
                phone = st.text_input('Phone Number', 'Enter phone number')
            with row_2_1:
                option = st.selectbox(
                    'Select the role',
                    ('Staff', 'Manager', 'FrontDesk'))
            with row_2_2:
                d = st.date_input(
                    "Date of birth",
                    datetime.date(2003, 5, 12))

            with row_3_1:
                address = st.text_input('Address', 'Enter your address')
            with row_3_2:
                email = st.text_input('Email', 'Enter email')
                _, _, _, col_4 = st.columns(4)
                with col_4:
                    if button("Add a staff", key="button1"):
                        isNoti = True
                        # insert data to datbase

        if isNoti:
            st.success("You have added a new staff")

elif selected == "Reservation":
    st.write("Reservation")
elif selected == "Guest":
    tab1, tab2, tab3, tab4 = st.tabs(
        ["**VIEW GUEST INFORMATION**", "**ADD A GUEST**", "**UPDATE GUEST**", "**REMOVE GUEST**"])
    with tab1:
        seeding_data = {'Guest Id': ["101", "102", "103", "104", "105", "106", "107"],
                        'Guest name': ["Le Chi Thinh", "Huynh Cong thien", "Nguyen Minh Tri", "Tran Van A", "Tran Van B", "Tran Van C", "Tran Van D"],
                        'Day of birth': ["22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012"],
                        'Address': ["Ca Mau", "Long An", "Bien Hoa", "Quang Nam", "Quang Ngai", "Tien Giang", "Phu Yen"],
                        'Phone number': ['0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345']
                        }
        df = pd.DataFrame(seeding_data)
        grid_return = AgGrid(df,
                             editable=True,
                             fit_columns_on_grid_load=True,
                             enable_quicksearch=True,
                             reload_data=True)

    with tab2:
        isNoti = False
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>ADD A NEW ROOME</h3>
        ''', unsafe_allow_html=True)
        with st.expander('', expanded=True):
            row_1_1, row_1_2 = st.columns(2)
            row_2_1, row_2_2 = st.columns(2)
            row_3_1, row_3_2 = st.columns(2)
            with row_1_1:
                item_name = st.text_input('Guest ID', 'Enter the guest ID')
            with row_1_2:
                phone = st.text_input('Guest name', 'Enter guest name')
            with row_2_1:
                phone_number = st.text_input(
                    'Phone number', 'Enter guest phone number')
            with row_2_2:
                d = st.date_input(
                    "Date of birth",
                    datetime.date(2003, 5, 12))

            with row_3_1:
                address = st.text_input('Address', 'Enter guest\'s address')
            with row_3_2:
                #     email = st.text_input('Email', 'Enter email')
                _, _, _, col_4 = st.columns(4)
                with col_4:
                    if button("Add a staff", key="button1"):
                        isNoti = True
                    # insert data to datbase

        if isNoti:
            st.success("You have added a new staff")
    with tab3:
        seeding_data = {"Edit": [False, False, False, False, False, False, False],
                        'Room ID': ["101", "102", "103", "104", "105", "106", "107"],
                        'Room Name': ["VIP1", "VIP2", "VIP3", "VIP4", "VIP5", "VIP6", "VIP7"],
                        'Type': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        'Number of beds': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        'Floor': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        "Status": ["12/5/2003", "15/5/2003", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002"],
                        "Price": ["FrontDesk", "Manager", "Staff", "Staff", "Staff", "Staff", "Staff"]}

        # show the table
        def updatedata():
            pass
        key = st.experimental_data_editor(
            seeding_data, on_change=updatedata)  # cal function back

        # Display the detail data
        count = 0
        for value in key['Edit']:
            if value:
                count += 1
                if count == 1:
                    index = key['Edit'].index(value)
                    with st.expander("", expanded=True):
                        column1, column2 = st.columns(2)
                        with column1:
                            card(
                                title=key['Room ID'][index],
                                text=key['Floor'][index],
                                image="http://placekitten.com/300/250",
                                url="https://www.google.com",
                            )
                        with column2:
                            st.subheader(
                                f"ROOM ID: :blue[{key['Room ID'][index]}]")
                            st.caption(
                                f"Room Name: :blue[{key['Room Name'][index]}]")
                            st.caption(f"Type: :blue[{key['Type'][index]}]")
                            st.caption(
                                f"Number of beds: :blue[{key['Number of beds'][index]}]")
                            st.caption(f"Price: :blue[{key['Price'][index]}]")
                else:
                    alert = st.error("You must select one room", icon="🚨")
                    time.sleep(3)
                    alert.empty()
    with tab4:
        pass


elif selected == "Inventory":
    tab1, tab2 = st.tabs(["**View inventory**", "**Add an item**"])
    with tab1:
        df = pd.DataFrame({'Item': ["Clothings", "Foods", "Bottle of water", "Pillows", "Shoes", "Towels"], 'Total': [
                          60, 30, 20, 60, 30, 20], 'Remaining': [30, 15, 10, 30, 15, 10]})
        grid_return = AgGrid(df,
                             editable=True,
                             fit_columns_on_grid_load=True,
                             enable_quicksearch=True,
                             reload_data=True)

    with tab2:
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>Add a new item</h3>
        ''', unsafe_allow_html=True)
        with st.expander('', expanded=True):
            item_name = st.text_input('Item name', 'Enter the item name')
            col1, col2 = st.columns(2)
            with col1:
                total = st.slider('Total', 0, 150, 25)
            with col2:
                price = st.number_input("Price per item", 20000)
                _, _, _, _, _, col6 = st.columns(6)
                with col6:
                    st.button("Add")
else:
    tab1, tab2 = st.tabs(["**View staff information**", "**Add a staff**"])
    with tab1:
        card1, card2, card3 = st.columns(3)
        card1.metric("Rooms Occupied ", "30", "-10%")
        card2.metric("Expected Arrivals", "9", "-8%")
        card3.metric("Expected Departure", "5", "4%")
        st.divider()

        seeding_data = {'Name': ["Le Chi Thinh", "Huynh Cong Thien", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri"],
                        'Phone': ["0822043153", "0822033134", "0822098123", "0822098123", "0822098123", "0822098123", "0822098123"],
                        'Email': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                        "Date Of Birth": ["12/5/2003", "15/5/2003", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002"],
                        "Roles": ["FrontDesk", "Manager", "Staff", "Staff", "Staff", "Staff", "Staff"]}

        df = pd.DataFrame(seeding_data)
        st.dataframe(df)

    with tab2:
        isNoti = False
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
            with col2:
                email = st.text_input('Email', 'Enter email')
                _, _, col_3 = st.columns(3)
                with col_3:
                    if button("Add a staff", key="button1"):
                        isNoti = True
                        # insert data to datbase

        if isNoti:
            st.success("You have added a new staff")
