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

#database
from database import DataBase

#Call only once
mydb = DataBase("localhost", "root", "root", "hms")



def MyWeb(authenticator):
    # SideBar
    with st.sidebar:
        selected = option_menu(f"Welcome {st.session_state['name']}", ["Dashboard", 'Rooms', 'Reservation', 'Inventory', 'Staff', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill', 'calendar-check-fill',
                                     'house-fill', 'person-lines-fill', 'person-fill'],
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

            seeding_data = {"Updated": [False, False, False, False, False, False, False],
                            'Room ID': ["101", "102", "103", "104", "105", "106", "107"],
                            'Room Name': ["VIP1", "VIP2", "VIP3", "VIP4", "VIP5", "VIP6", "VIP7"],
                            'Type': ["Couple", "King", "King", "King", "Couple", "Couple", "Couple"],
                            'Number of beds': ["1", "2", "2","2","1","1","1"],
                            'Floor': ["1", "2", "2","2","1","1","1"],
                            "Status": ["Available", "Occupied", "Reserved", "Occupied", "Available", "Available", "Available"],
                            "Price": ["1.000.000", "2.000.000", "2.000.000","2.000.000","1.000.000","1.000.000","1.000.000"]}

            # Show database into table
            table = st.experimental_data_editor(seeding_data, use_container_width=True)
            # Update a room
            for value in table['Updated']:
                if value:
                        index = table['Updated'].index(value)
                        #Show an expander for the selected room
                        if table["Status"][index] == "Available":
                            Reservation_column, Room_Infor_Column = st.columns(2)
                            with Reservation_column:
                                with st.form("Room Reservation"):    
                                    st.subheader(
                                    f"Information: :blue[Reservation]")                                
                                    with st.container():
                                        reservation_1_1, reservation_1_2 = st.columns(2)
                                        reservation_2_1, reservation_2_2 = st.columns(2)
                                        reservation_3_1, reservation_3_2 = st.columns(2)
                                        with reservation_1_1:
                                            first_guest_name = st.text_input(
                                                "Full Name", f"Enter the name of the first guest")
                                        with reservation_1_2:
                                            first_guest_phone = st.text_input(
                                                "Phone Number", f"Enter phone number")
                                        with reservation_2_1:
                                            first_guest_address = st.text_input(
                                                "Address", f"Enter address")
                                        with reservation_2_2:
                                            first_guest_email = st.text_input(
                                                "Email", f"Enter email")
                                        with reservation_3_1:
                                            second_guest_name = st.text_input(
                                                "Full Name", f"Enter the name of the second guest")
                                        with reservation_3_2:
                                            second_guest_phone = st.text_input(
                                                "Phone", f"Enter phone number")
                                        reservation_button = st.form_submit_button("Make a reservation", type = "primary")
                                        

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
                                        f"Information: :blue[Checkout]")                                
                                        with st.container():
                                            reservation_1_1, reservation_1_2 = st.columns(2)
                                            reservation_2_1, reservation_2_2 = st.columns(2)
                                            reservation_3_1, reservation_3_2 = st.columns(2)
                                            with reservation_1_1:
                                                first_guest_name = st.text_input(
                                                    "Full Name", f"Le Chi Guest")
                                            with reservation_1_2:
                                                first_guest_phone = st.text_input(
                                                    "Phone Number", f"12345678")
                                            with reservation_2_1:
                                                first_guest_address = st.text_input(
                                                    "Address", f"Ca Mau")
                                            with reservation_2_2:
                                                first_guest_email = st.text_input(
                                                    "Email", f"iamguest@gmail.com")
                                            with reservation_3_1:
                                                second_guest_name = st.text_input(
                                                    "Full Name", f"Le Chi Second")
                                            with reservation_3_2:
                                                second_guest_phone = st.text_input(
                                                    "Phone", f"112233444")
                                            checkout_button = st.form_submit_button("checkout", type = "primary")
                                            if checkout_button:
                                                pass
                                                #checkout process
                                            
                                
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
                        if table["Status"][index] == "Reserved":   
                                    guest_column, Room_Infor_Column = st.columns(2)
                                    with guest_column:
                                        with st.form("Checkin"):    
                                            st.subheader(
                                            f"Information: :blue[Checkin]")                                
                                            with st.container():
                                                reservation_1_1, reservation_1_2 = st.columns(2)
                                                reservation_2_1, reservation_2_2 = st.columns(2)
                                                reservation_3_1, reservation_3_2 = st.columns(2)
                                                with reservation_1_1:
                                                    first_guest_name = st.text_input(
                                                        "Full Name", f"Le Chi Guest")
                                                with reservation_1_2:
                                                    first_guest_phone = st.text_input(
                                                        "Phone Number", f"12345678")
                                                with reservation_2_1:
                                                    first_guest_address = st.text_input(
                                                        "Address", f"Ca Mau")
                                                with reservation_2_2:
                                                    first_guest_email = st.text_input(
                                                        "Email", f"iamguest@gmail.com")
                                                with reservation_3_1:
                                                    second_guest_name = st.text_input(
                                                        "Full Name", f"Le Chi Second")
                                                with reservation_3_2:
                                                    second_guest_phone = st.text_input(
                                                        "Phone", f"112233444")
                                                Checkin_button = st.form_submit_button("Checkin", type = "primary")
                                                
                                    
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
        Reservation_infor_tab, Add_a_reservation= st.tabs(
            ["**VIEW RESERVATION**", "**ADD RESERVATION**"])
        with Reservation_infor_tab:
            seeding_data = {"Edit": [False, False, False, False, False, False, False],
                            'Room Id': ["101", "102", "103", "104", "105", "106", "107"],
                            'Guest name': ["Le Chi Thinh", "Huynh Cong thien", "Nguyen Minh Tri", "Tran Van A", "Tran Van B", "Tran Van C", "Tran Van D"],
                            'Date of birth': ["22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012", "22/10/2012"],
                            'Address': ["Ca Mau", "Long An", "Bien Hoa", "Quang Nam", "Quang Ngai", "Tien Giang", "Phu Yen"],
                            'Phone number': ['0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345', '0945678345'],
                            'Number of people': ["2", "2", "3", "4", "5", "3", "2"],
                            }


            table_guest = st.experimental_data_editor(
                seeding_data, use_container_width=True )  

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

        with Add_a_reservation:
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
            
            table_inventory = st.experimental_data_editor(seeding_inventory ,use_container_width= True)

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
        View_staff_infor, Add_a_staff = st.tabs(["**View staff information**", "**Add a staff**"])
        #get database from staff table
        staff_data = mydb.get_staff_table()
        with View_staff_infor:

            #handle data for cards
            role_count = {}
            for role in staff_data['Role']:
                if role in role_count:
                    role_count[role] += 1
                else:
                    role_count[role] = 1
            
            manager_card, staff_card, desk_card = st.columns(3)
            manager_card.metric(label="Total Manager", value=role_count['Manager'])
            staff_card.metric(label="Total Staf", value=role_count['Staff'])
            desk_card.metric(label="Total FrontDesk", value=role_count['FrontDesk'])
            style_metric_cards(border_left_color='#F39D9D')
            
            #Show the table data
            table_staff = st.experimental_data_editor(staff_data, use_container_width = True)
            
            #If there are two selected rows, please show the second selected one.
            for value in table_staff['Update']:
                if value :
                        index = table_staff['Update'].index(value)
                        staff_id = table_staff['staff_id'][index]
                        #Show an expander for the selected room
                        with st.expander("", expanded=True):
                            column_card, column_infor = st.columns(2)
                             #card for the selected room
                            with column_card:
                                card(
                                    title=table_staff['Name'][index],
                                    text=table_staff['Role'][index],
                                    image="http://placekitten.com/300/250",
                                    url="https://www.google.com",
                                    key= staff_id
                                )   
                                
                            #information for the selected room    
                            with column_infor:
                             
                              
                                st.subheader(
                                        f"ROOM ID: :blue[{table_staff['Name'][index]}]")
                             
                                with st.form("Update Staff Information"):
                                    isUpdateSucess = False 
                                    
                                    with st.container():
                                        row_1_1, row_1_2 = st.columns(2)
                                        row_2_1, row_2_2 = st.columns(2)
                                        row_3_1, row_3_2 = st.columns(2)
                                        with row_1_1:
                                            Name = st.text_input(
                                                "Full Name", f"{table_staff['Name'][index]}")
                                        with row_1_2:
                                            Phone = st.text_input(
                                                'Phone Number', f"{table_staff['Phone'][index]}")
                                        with row_2_1:
                                            Email = st.text_input(
                                                "Email", f"{table_staff['Email'][index]}")
                                        with row_2_2:
                                            Role = st.selectbox(
                                                "Role", ("Manager", "Staff", "FrontDesk"))
                                        with row_3_1:
                                            Date_of_birth = st.text_input(
                                                "Date Of Birth", f"{table_staff['Date Of Birth'][index]}")
                                        with row_3_2:
                                            staff_id = st.text_input(
                                                "staff_id", f"{table_staff['staff_id'][index]}")

                                        col1_remove_staff,_,col3_update_staff = st.columns(3)
                                        with col1_remove_staff:
                                            remove_button = st.form_submit_button("Remove")
                                            #Remove the user
                                        with col3_update_staff:
                                            updated_button = st.form_submit_button("Update Staff Info", type = "primary")
                                            if updated_button:
                                                isUpdateSucess = mydb.Update_One_Staff(
                                                    staff_id, Name, Phone, Email, Date_of_birth, Role
                                                )
                                                #After updated --> should refresh the whole page
                            
                                    if isUpdateSucess:          
                                            st.success("Staff information has been updated") 
                                            

        with Add_a_staff:
            isNoti = False
            st.markdown('''
            <h3 style='text-align: center;  color: black;'>Add a staff</h3>
            ''', unsafe_allow_html=True)
        
            with st.form("Add Staff Information", clear_on_submit = True):           
                with st.container(): 
                    isUpdateSucess = False
                    row_1_1, row_1_2 = st.columns(2)
                    row_2_1, row_2_2 = st.columns(2)
                    row_3_1, row_3_2 = st.columns(2)
                    with row_1_1:
                        Name = st.text_input(
                            "Full Name", f"Enter staff name")
                    with row_1_2:
                        Phone = st.text_input(
                            'Phone', f"Enter phone number")
                    with row_2_1:
                        Email = st.text_input(
                            "Email", f"Enter Email")
                    with row_2_2:
                        Role = st.selectbox(
                            "Role", ("Manager", "Staff", "FrontDesk"))
                    with row_3_1:
                        Date_of_birth = st.date_input(
                            "Enter date of birth",
                            datetime.date(2003, 7, 6))
                    with row_3_2:
                        Address = st.text_input(
                            "Address", f"Enter address")
                        
                        _, _, col3_button = st.columns(3)
                        
                        with col3_button:    
                            add_button = st.form_submit_button("Create the staff info", type = "primary")
                            if add_button:
                                isNoti = mydb.Add_New_Staff(Name,Phone,Email,Date_of_birth,Role)

            if isNoti:
                st.success("You have added a new staff")
    else:
        st.write("edit profile")
    

      