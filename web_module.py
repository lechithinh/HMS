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

def MyWeb(authenticator):
    # SideBar
    with st.sidebar:
        selected = option_menu(f"Welcome {st.session_state['name']}", ["Dashboard", 'Rooms', 'Reservation', 'Guest', 'Inventory', 'Staff', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill', 'calendar-check-fill',
                                    'people-fill', 'house-fill', 'person-lines-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })

    #DASHBOARD SECTION
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
            
    #DASHBOARD SECTION
    elif selected == "Rooms":
        room_information_tab, add_room_tab = st.tabs(["**VIEW ROOM INFORMATION**",
                            "**ADD A ROOM**"])
        with room_information_tab:
            
            #Cards 
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Gain", value=5000, delta=1000)
            col2.metric(label="Loss", value=5000, delta=-1000)
            col3.metric(label="No Change", value=5000, delta=0)
            style_metric_cards(border_left_color='#F39D9D')

            #Functions to update information to database
            def UpdateRecord():
                pass

            seeding_data = {"Edit": [False, False, False, False, False, False, False],
                            'Room ID': ["101", "102", "103", "104", "105", "106", "107"],
                            'Room Name': ["VIP1", "VIP2", "VIP3", "VIP4", "VIP5", "VIP6", "VIP7"],
                            'Type': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                            'Number of beds': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                            'Floor': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                            "Status": ["12/5/2003", "15/5/2003", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002"],
                            "Price": ["FrontDesk", "Manager", "Staff", "Staff", "Staff", "Staff", "Staff"]}

            # Show database into table
            table = st.experimental_data_editor(seeding_data, on_change=UpdateRecord)  

        # Update a room
            count = 0
            for value in table['Edit']:
                if value:
                    count += 1
                    if count == 1:
                        index = table['Edit'].index(value)
                        
                        #Show an expander for the selected room
                        with st.expander("", expanded=True):
                            column_card, column_infor = st.columns(2)
                            
                            #card for the selected room
                            with column_card:
                                card(
                                    title=table['Room ID'][index],
                                    text=table['Floor'][index],
                                    image="http://placekitten.com/300/250",
                                    url="https://www.google.com",
                                )
                                
                            #information for the selected room    
                            with column_infor:
                                isUpdate = False 
                                st.subheader(
                                    f"ROOM ID: :blue[{table['Room ID'][index]}]")
                                row_1_1, row_1_2 = st.columns(2)
                                row_2_1, row_2_2 = st.columns(2)
                                row_3_1, row_3_2 = st.columns(2)
                                with row_1_1:
                                    room_name = st.text_input(
                                        "Room name", f"{table['Room Name'][index]}")
                                with row_1_2:
                                    type_room = st.text_input(
                                        'Room type', f"{table['Type'][index]}")
                                with row_2_1:
                                    floor = st.text_input(
                                        "Floor", f"{table['Floor'][index]}")
                                with row_2_2:
                                    status = st.selectbox(
                                        "Status", ("Vacant", "Occupied"))
                                with row_3_1:
                                    num_bed = st.text_input(
                                        "Number of bed", f"{table['Number of beds'][index]}")
                                with row_3_2:
                                    price = st.text_input(
                                        "Price", f"{table['Price'][index]}")
                                    
                                _, _,col3_button = st.columns(3)
                                
                                with col3_button:    
                                    if button("Update the room", key="updateRoom"):
                                        isUpdate = True
                            
                            if isUpdate:          
                                st.success("You have updated the information of the room")    
                                
                                
                    else:
                        alert = st.error("You must select one room", icon="🚨")
                        time.sleep(3)
                        alert.empty()

        with add_room_tab:
            
            #Insert a new room to database
            def AddRoom():
                pass
            
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
                suscess_message = st.success("You have added a new staff")
                time.sleep(2)
                suscess_message.empty()
                
    #RESERVATION SECTION
    elif selected == "Reservation":
        st.write("Reservation")
        
    #GUEST SECTION
    elif selected == "Guest":
        Guest_Infor_Tab, Add_Guest_Tab= st.tabs(
            ["**VIEW GUEST INFORMATION**", "**ADD A GUEST**"])
        with Guest_Infor_Tab:
            seeding_data = {"Edit": [False, False, False, False, False, False, False],
                            'Guest Id': ["101", "102", "103", "104", "105", "106", "107"],
                            'Guest name': ["Le Chi Thinh", "Huynh Cong thien", "Nguyen Minh Tri", "Tran Van A", "Tran Van B", "Tran Van C", "Tran Van D"],
                            'Date of birth': ["22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012"],
                            'Address': ["Ca Mau", "Long An", "Bien Hoa", "Quang Nam", "Quang Ngai", "Tien Giang", "Phu Yen"],
                            'Phone number': ['0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345']
                            }

            # show the table
            def UpdateRecord():
                pass
            table_guest = st.experimental_data_editor(
                seeding_data, on_change=UpdateRecord)  

            # Display the detail data
            count = 0
            for value in table_guest['Edit']:
                if value:
                    count += 1
                    if count == 1:
                        index = table_guest['Edit'].index(value)
                        with st.expander("", expanded=True):
                            column1, column2 = st.columns(2)
                            with column1:
                                card(
                                    title=table_guest['Guest Id'][index],
                                    text=table_guest['Guest name'][index],
                                    image="http://placekitten.com/300/250",
                                    url="https://www.google.com",
                                )
                            with column2:
                                isUpdateGuest = False
                                st.subheader(
                                    f"GUEST ID: :blue[{table_guest['Guest Id'][index]}]")
                                row_1_1, row_1_2 = st.columns(2)
                                row_2_1, row_2_2 = st.columns(2)
                                row_3_1, row_3_2 = st.columns(2)
                                with row_1_1:
                                    guest_id = st.text_input(
                                        "Guest ID", f"{table_guest['Guest Id'][index]}")
                                with row_1_2:
                                    guest_name = st.text_input(
                                        "Guest name", f"{table_guest['Guest name'][index]}")
                                with row_2_1:
                                    date_of_birth = st.date_input(
                                        "Date of birth", datetime.date(2003, 5, 28))
                                with row_2_2:
                                    address = st.text_input(
                                        "Address", f"{table_guest['Address'][index]}")
                                with row_3_1:
                                    phone = st.text_input(
                                        "Phone number", f"{table_guest['Phone number'][index]}")
                                with row_3_2:
                                    phone_test = st.text_input(
                                        "Phone number test", f"{table_guest['Phone number'][index]}")
                                
                                _, _,_,col2_remove,col3_updated = st.columns(5)
                                
                                with col2_remove:
                                    if button("Remove", key="Remove guest infor"):
                                        pass
                                with col3_updated:    
                                    if button("Update", key="Update guest infor"):
                                        isUpdateGuest = True
                            
                            if isUpdateGuest:          
                                st.success("You have updated the information of the guest")    

                    else:
                        alert = st.error("You must select one record", icon="🚨")
                        time.sleep(3)
                        alert.empty()

        with Add_Guest_Tab:
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
                    email_test = st.text_input('Email Test', 'Enter email')
                    _, _, _, col_4 = st.columns(4)
                    with col_4:
                        if button("Add a staff", key="button1"):
                            isNoti = True
                        # insert data to datbase

            if isNoti:
                add_message = st.success("You have added a new staff")
                time.sleep(2)
                add_message.empty()
            
    #INVENTORY SECTION
    elif selected == "Inventory":
        tab1, tab2 = st.tabs(["**View inventory**", "**Add an item**"])
        with tab1:
            seeding_inventory = {'Update': [False, False,  False, False, False, False,],
                                'Item': ["Clothings", "Foods", "Bottle of water", "Pillows", "Shoes", "Towels"], 'Total': [
                            60, 30, 20, 60, 30, 20], 'Remaining': [30, 15, 10, 30, 15, 10]}
            
            table_inventory = st.experimental_data_editor(seeding_inventory)

        with tab2:
            st.markdown('''
            <h3 style='text-align: center;  color: black;'>Add a new item</h3>
            ''', unsafe_allow_html=True)
            with st.expander('', expanded=True):
                item_name = st.selectbox("Item name", seeding_inventory['Item'])
                col1, col2 = st.columns(2)
                with col1:
                    total = st.slider('Total', 0, 150, 25)
                with col2:
                    price = st.number_input("Price per item", 20000)
                    _, _, _, _, _, col6 = st.columns(6)
                    with col6:
                        st.button("Add")
    elif selected == "Staff":
        tab1, tab2 = st.tabs(["**View staff information**", "**Add a staff**"])
        with tab1:
            card1, card2, card3 = st.columns(3)
            card1.metric("Rooms Occupied ", "30", "-10%")
            card2.metric("Expected Arrivals", "9", "-8%")
            card3.metric("Expected Departure", "5", "4%")
            st.divider()

            seeding_staff = { "Update": [ False, False, False, False, False, False, False],
                            'Name': ["Le Chi Thinh", "Huynh Cong Thien", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri", "Nguyen Minh Tri"],
                            'Phone': ["0822043153", "0822033134", "0822098123", "0822098123", "0822098123", "0822098123", "0822098123"],
                            'Email': ["lechithinh@gmail.com", "huynhcongthien@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com", "nguyenminhtri@gmail.com"],
                            "Date Of Birth": ["12/5/2003", "15/5/2003", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002", "16/5/2002"],
                            "Roles": ["FrontDesk", "Manager", "Staff", "Staff", "Staff", "Staff", "Staff"]}

            table_staff = st.experimental_data_editor(seeding_staff)

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
    else:
        st.write("edit profile")
    

      