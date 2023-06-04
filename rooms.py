import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import time


def Rooms():
    room_information_tab, add_room_tab = st.tabs(["**VIEW ROOM INFORMATION**",
                            "**ADD A ROOM**"])
    with room_information_tab:   
        
        seeding_data = {"View information": [False, False, False, False, False, False, False],
                        'Room ID': ["101", "102", "103", "104", "105", "106", "107"],
                        'Room Name': ["N1", "V2", "V3", "V4", "N5", "N6", "N7"],
                        'Type': ["Normal", "VIP", "VIP", "VIP", "Normal", "Normal", "Normal"],
                        'Number of beds': ["1", "2", "2","2","1","1","1"],
                        'Max People': ["2", "4", "4","4","2","2","2"],
                        'Floor': ["1", "2", "2","2","1","1","1"],
                        "Status": ["Available", "Available", "Occupied", "Occupied", "Available", "Occupied", "Available"],
                        "Price": ["1.000.000", "2.000.000", "2.000.000","2.000.000","1.000.000","1.000.000","1.000.000"]}     
        #Cards 
        status_count = {}
        total_rooms = len(seeding_data['Room ID'])
        for role in seeding_data['Status']:
            if role in status_count:
                status_count[role] += 1
            else:
                status_count[role] = 1
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Available", value=status_count['Available'])
        col2.metric(label="Occupied", value=status_count['Occupied'])
        col3.metric(label="Total Rooms", value=total_rooms)
        style_metric_cards(border_left_color='#F39D9D')

        


        
    
        table = st.experimental_data_editor(seeding_data, use_container_width=True)
        # Update a room
        for value in table['View information']:
            if value:
                    index = table['View information'].index(value)
                    #Show an expander for the selected room
                    if table["Status"][index] == "Available":
                        Reservation_column, Room_Infor_Column = st.columns(2)
                        with Reservation_column:
                            with st.form("Room Checkin"):    
                                st.subheader(
                                f"INFORMATION: :blue[CHECKIN]")                                
                                with st.container():
                                    reservation_1_1, reservation_1_2 = st.columns(2)
                                    reservation_2_1, reservation_2_2 = st.columns(2)
                                    reservation_3_1, reservation_3_2 = st.columns(2)
                                    reservation_4_1, reservation_4_2 = st.columns(2)
                                    with reservation_1_1:
                                        first_guest_name = st.text_input(
                                            "Full Name", f"First guest name")
                                    with reservation_1_2:
                                        first_guest_phone = st.text_input(
                                            "Phone Number", f"First guest phone")
                                    with reservation_2_1:
                                        first_guest_address = st.text_input(
                                            "Address", f"Enter address")
                                    with reservation_2_2:
                                        first_guest_dob = st.text_input(
                                            "Date of Birth", f"Enter Date of Birth")
                                    if int(table['Max People'][index]) == 4:
                                        with reservation_3_1:
                                            second_guest_name = st.text_input(
                                            "Full Name", f"Second guest name", key="second guest")
                                        with reservation_3_2:
                                            second_guest_phone = st.text_input(
                                                "Phone", f"Second guest phone", key="second guest phone")
                                        with reservation_4_1:
                                            second_guest_address = st.text_input(
                                                "Address", f"Enter address", key="second guest address")
                                        with reservation_4_2:
                                            second_guest_dob = st.text_input(
                                                "Date of Birth", f"Enter Date of Birth", key="second guest dob")
                                        
                                checkin_button = st.form_submit_button("Checkin", type = "primary")
                                    

                        with Room_Infor_Column:
                            isUpdate = False 
                            with st.form("Room inforamtion"):                                 
                                with st.container():
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
                                        Update_Room_Button = st.form_submit_button("Update the room", type = "primary") 
                                        if Update_Room_Button:
                                            isUpdate = True
                                
                                    if isUpdate:          
                                        st.success("You have updated the information of the room")    
                    if table["Status"][index] == "Occupied":   
                            guest_column, Room_Infor_Column = st.columns(2)
                            with guest_column:
                                with st.form("Checkout"):    
                                    st.subheader(
                                    f"INFORMATION: :blue[CHECKOUT]")                                
                                    with st.container():
                                        reservation_1_1, reservation_1_2 = st.columns(2)
                                        reservation_2_1, reservation_2_2 = st.columns(2)
                                        reservation_3_1, reservation_3_2 = st.columns(2)
                                        reservation_4_1, reservation_4_2 = st.columns(2)
                                        with reservation_1_1:
                                            first_guest_name = st.text_input(
                                                "Full Name", f"")
                                        with reservation_1_2:
                                            first_guest_phone = st.text_input(
                                                "Phone Number", f"")
                                        with reservation_2_1:
                                            first_guest_address = st.text_input(
                                                "Address", f"")
                                        with reservation_2_2:
                                            first_guest_dob = st.text_input(
                                                "Date of Birth", f"")
                                        if int(table['Max People'][index]) == 4:
                                            with reservation_3_1:
                                                second_guest_name = st.text_input(
                                                "Full Name", f"", key="second guest")
                                            with reservation_3_2:
                                                second_guest_phone = st.text_input(
                                                    "Phone", f"", key="second guest phone")
                                            with reservation_4_1:
                                                second_guest_address = st.text_input(
                                                    "Address", f"", key="second guest address")
                                            with reservation_4_2:
                                                second_guest_dob = st.text_input(
                                                    "Date of Birth", f"", key="second guest dob")
                                        #Orders
                                        water_bottle = st.slider('Number of water bottles', 0, 10, 1)
                                        coca_bottle = st.slider('Number of CoCa bottles', 0, 10, 1)
                                        pessi_bottle = st.slider('Number of Pessi bottles', 0, 10, 1)
                                        
                                        #Checkout and update button
                                        checkout_col,_ ,_, update_col = st.columns(4)
                                        with checkout_col:
                                            checkout_button = st.form_submit_button("checkout", type = "primary")
                                        with update_col:
                                            updated_infor_button = st.form_submit_button("Update infor", type = "primary")
                                        if checkout_button:
                                            pass
                                            #checkout process
                                        if updated_infor_button:
                                            pass
                                        
                            
                            with Room_Infor_Column:
                                isUpdate = False 
                                with st.form("Room inforamtion"):                                 
                                    with st.container():
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
                                            Update_Room_Button = st.form_submit_button("Update the room", type = "primary") 
                                            if Update_Room_Button:
                                                isUpdate = True
                                    
                                        if isUpdate:          
                                            st.success("You have updated the information of the room") 
                    
    with add_room_tab:
        isNoti = False
        st.markdown('''
        <h3 style='text-align: center;  color: black;'>ADD A NEW ROOM</h3>
        ''', unsafe_allow_html=True)
        with st.form("Add new room"):                                 
            with st.container():
                row_1_1, row_1_2 = st.columns(2)
                row_2_1, row_2_2 = st.columns(2)
                row_3_1, row_3_2 = st.columns(2)
                with row_1_1:
                    room_name = st.text_input('Room Name', 'Enter the room name')
                with row_1_2:
                    room_type =   st.selectbox(
                        'Select the type',
                        ('Normal', 'VIP'))
                with row_2_1:
                    floor = st.selectbox(
                        'Select the floor',
                        ('1', '2'))
                with row_2_2:
                    room_price = st.text_input('Room Price', 'Enter the price')
                with row_3_1:
                    beds = st.text_input('Number of beds', 'Enter number of beds')
                with row_3_2:
                    people = st.text_input('Total people', 'Enter total people')
                    _, _, _, col_4 = st.columns(4)
                    with col_4:
                        Add_room_button = st.form_submit_button("Add a room", type = "primary")
                        if Add_room_button:
                            isNoti = True
                        

        if isNoti:
            suscess_message = st.success("The room has been added")
            time.sleep(2)
            suscess_message.empty()