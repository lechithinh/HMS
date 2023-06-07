import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import time
# import datetime
from datetime import datetime, timedelta



def Rooms(mydb, staff_id):
    room_information_tab, add_room_tab = st.tabs(["**VIEW ROOM INFORMATION**",
                            "**ADD A ROOM**"])
    with room_information_tab:   
        
        room_table = mydb.get_room_table()
        # print(room_table)
        #Cards 
        status_count = {'Available':0, 'Occupied':0}
        total_rooms = len(room_table['Room ID'])
        for role in room_table['Status']:
            if role == 'Available':
                status_count['Available'] +=1
            else:
                status_count['Occupied'] +=1
            
        print(status_count)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Available", value=status_count['Available'])
        col2.metric(label="Occupied", value=status_count['Occupied'])
        col3.metric(label="Total Rooms", value=total_rooms)
        style_metric_cards(border_left_color='#F39D9D')

    
        table = st.experimental_data_editor(room_table, use_container_width=True)
        #Get staff info and staff_id
        
        # Update a room
        guest_info = {"guest_1":[]}
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
                                    date_1, date_2 = st.columns(2)

                                    with reservation_1_1:
                                        first_guest_name = st.text_input(
                                            "Full Name", placeholder= "First guest name")
                                    with reservation_1_2:
                                        first_guest_phone = st.text_input(
                                            "Phone Number", placeholder = "First guest phone")
                                    with reservation_2_1:
                                        first_guest_address = st.text_input(
                                            "Address", placeholder= "Enter address")
                                    with reservation_2_2:
                                        first_guest_dob = st.date_input(
                                            "Date of Birth" )

                                    if int(table['Max people'][index]) == 4:
                                        with reservation_3_1:
                                            second_guest_name = st.text_input(
                                            "Full Name", placeholder= "Second guest name", key="second guest")
                                        with reservation_3_2:
                                            second_guest_phone = st.text_input(
                                                "Phone", placeholder="Second guest phone", key="second guest phone")
                                        with reservation_4_1:
                                            second_guest_address = st.text_input(
                                                "Address", placeholder= "Enter address", key="second guest address")
                                        with reservation_4_2:
                                            second_guest_dob = st.date_input(
                                                "Date of Birth", key="second guest dob")

                                    
                                    with date_1:
                                        checkin_date = st.date_input("Check-in date")
                                        checkin_time = st.time_input('Check-in time')
                                        checkin_datetime = datetime.combine(checkin_date, checkin_time)
                                        #print(checkin_datetime)
                                    with date_2:
                                        checkout_date = st.date_input("Check-out date")
                                        checkout_time = st.time_input("Check-out time")
                                        checkout_datetime = datetime.combine(checkout_date, checkout_time)

                                    remain_water = mydb.get_remain_item("water")
                                    remain_coca =  mydb.get_remain_item("coca")
                                    remain_pessi = mydb.get_remain_item("pessi")
                                    if (remain_water == 0):
                                        st.text("Water is not available")
                                    else:
                                        water_bottle = st.slider('Number of water bottles', 0,  remain_water, 0)

                                    if (remain_coca == 0):
                                        st.text("Coca is not available")
                                    else:
                                        coca_bottle = st.slider('Number of CoCa bottles', 0,  remain_coca, 0)

                                    if (remain_pessi == 0):
                                        st.text("Pessi is not available")
                                    else:
                                        pessi_bottle = st.slider('Number of CoCa bottles', 0,  remain_pessi, 0)

                                checkin_button = st.form_submit_button("Checkin", type = "primary")
                                
                                if checkin_button:
                                    

                                    #update to guest infor to data


                                    if(int(table['Max people'][index]) == 2):
                                        mydb.add_a_guest(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob)
                                        
                                    else:
                                        mydb.add_a_guest(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob)
                                        mydb.add_a_guest(second_guest_name,second_guest_phone,second_guest_address,second_guest_dob)

                                    
                                    #change status to occupied
                                    mydb.check_in_room(table['Room ID'][index])

                                    
                                    # add booking
                                    mydb.add_a_booking(table['Room ID'][index], checkin_datetime, checkout_datetime,False)

                                    #get booking id
                                    booking_id = mydb.get_booking_id(table['Room ID'][index])

                                    # add booking-guest
                                    num_pp = int(table['Max people'][index])/2
                                    guest_id = mydb.get_guest_id(int(num_pp)) # list of guest id
                                    mydb.add_a_booking_guest(booking_id, guest_id)

                                    #update orders
                                    mydb.insert_order(booking_id, 'water',water_bottle)
                                    mydb.insert_order(booking_id, 'coca',coca_bottle)
                                    mydb.insert_order(booking_id, 'pessi',pessi_bottle)

                                    #update inventory 
                                    mydb.update_inventory('water',water_bottle)
                                    mydb.update_inventory('coca',coca_bottle)
                                    mydb.update_inventory('pessi',pessi_bottle)


                                    
                        with Room_Infor_Column:
                            isUpdate = False 
                            with st.form("Room inforamtion"):                                 
                                with st.container():
                                    st.subheader(
                                        f"ROOM ID: :blue[{table['Room ID'][index]}]")
                                    row_1_1, row_1_2 = st.columns(2)
                                    row_2_1, row_2_2 = st.columns(2)
                                    row_3_1, row_3_2 = st.columns(2)
                                    row_4_1, row_4_2 = st.columns(2)
                                    with row_1_1:
                                        room_name = st.text_input(
                                            "Room name", f"{table['Room Name'][index]}")
                                    with row_1_2:
                                        floor_values = [1,2]
                                        floor = st.selectbox("Floor", floor_values,index= floor_values.index(table['Floor'][index]))
                                    with row_2_1:
                                        room_type_values = ["VIP","NORMAL"]
                                        room_type = st.selectbox("Room type",room_type_values, index = room_type_values.index(table["Room type"][index]))
                                            
                                    with row_2_2:
                                        room_price = st.text_input(
                                            "Price", f"{table['Room price'][index]}")
                                    with row_3_1:
                                        room_bed = st.text_input(
                                            "Number of bed", f"{table['Room beds'][index]}")
                                    with row_3_2:
                                        max_pp = st.text_input(
                                            "Max people", f"{table['Max people'][index]}")          
                                    with row_4_1:
                                        status_values = ["Available","Occupied"]
                                        status = st.selectbox(
                                            "Status", status_values, index = status_values.index(table["Status"][index]))
                                    with row_4_2:
                                        isActive = st.text_input(
                                            "Is active", f"{table['is Active'][index]}")
                                    _, _,col3_button = st.columns(3)
                                    
                                    with col3_button:   
                                        Update_Room_Button = st.form_submit_button("Update the room", type = "primary") 
                                        if Update_Room_Button:
                                            isUpdate = True
                                            #update room
                                            mydb.update_room(room_name,floor,room_type,room_price,room_bed,max_pp,status,isActive,table['Room ID'][index])
                                
                                    if isUpdate:          
                                        update_success_msg = st.success("You have updated the information of the room") 
                                        time.sleep(1)
                                        update_success_msg.empty()

                    if table["Status"][index] == "Occupied":   

                            #Lấy dữ liệu của guest view lên và dữ liệu của order và của inventory (số lượng còn lại)
                            guest_room_data = mydb.get_guest_of_room(table['Room ID'][index], False)
                            
                            #Take remain in inventory
                            water_remain = mydb.get_remain_item('water')
                            coca_remain = mydb.get_remain_item('coca')
                            pessi_remain = mydb.get_remain_item('pessi')

                            #Take amount order of room
                            water_order = mydb.get_order_amount(table['Room ID'][index], 'water')
                            coca_order = mydb.get_order_amount(table['Room ID'][index], 'coca')
                            pessi_order = mydb.get_order_amount(table['Room ID'][index], 'pessi')
                            #room and booking and book_guest => guest id and guest ==> guest infor (ok)
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
                                        "Full Name", f"{guest_room_data['guest_name'][0]}")
                                        with reservation_1_2:
                                            first_guest_phone = st.text_input(
                                        "Phone Number", f"{guest_room_data['phone_number'][0]}")
                                        with reservation_2_1:
                                            first_guest_address = st.text_input(
                                        "Address", f"{guest_room_data['address'][0]}")
                                        with reservation_2_2:
                                            first_guest_dob = st.text_input(
                                        "Date of Birth", f"{guest_room_data['date_of_birth'][0]}")
                                        if int(table['Max people'][index]) == 4:
                                            with reservation_3_1:
                                                second_guest_name = st.text_input(
                                            "Full Name", f"{guest_room_data['guest_name'][1]}", key="second guest")
                                            with reservation_3_2:
                                                second_guest_phone = st.text_input(
                                            "Phone", f"{guest_room_data['phone_number'][1]}", key="second guest phone")
                                            with reservation_4_1:
                                                second_guest_address = st.text_input(
                                            "Address", f"{guest_room_data['address'][1]}", key="second guest address")
                                            with reservation_4_2:
                                                second_guest_dob = st.text_input(
                                            "Date of Birth", f"{guest_room_data['date_of_birth'][1]}", key="second guest dob")
                                        #Update orders
                                        water_bottle = st.slider('Number of water bottles', 0, water_remain, water_order)
                                        coca_bottle = st.slider('Number of CoCa bottles', 0, coca_remain, coca_order)
                                        pessi_bottle = st.slider('Number of Pessi bottles', 0, pessi_remain, pessi_order)
                                
                                      
                                        
                                        #Checkout and update button
                                        checkout_col,_ ,_, update_col = st.columns(4)
                                        with checkout_col:
                                            checkout_button = st.form_submit_button("Checkout", type = "primary")
                                        with update_col:
                                            updated_infor_button = st.form_submit_button("Update infor", type = "primary")
                                        
                                        booking_id = mydb.get_booking_id(table['Room ID'][index])
                                        if checkout_button:
                                            
                                            #update trạng thái room sang available

                                            # mydb.Update_room_status(table['Room ID'][index])

                                            #update booking isClose = True

                                            #mydb.Update_isClose_booking(table['Room ID'][index])

                                            #get date, room price, order (item + soluong + giá), total price. 
                                            table_bill = mydb.finalize_a_bill(booking_id)
                                            total_price = total_price = table_bill['bill_price'][0]
                                            #add to bill
                                            mydb.add_bill(booking_id, table['Room ID'][index], staff_id, total_price)
                                            
                                            with st.expander("Total summary", expanded= True):
                                                st.write(
                                            "------------------------**The Bill**------------------------")
                                                col1_1, col1_2 = st.columns(2)
                                                col2_1, col2_2 = st.columns(2)
                                                col3_1, col3_2 = st.columns(2)
                                                col4_1, col4_2 = st.columns(2)
                                                col5_1, col5_2 = st.columns(2)
                                                col6_1, col6_2 = st.columns(2)
                                                col7_1, col7_2 = st.columns(2)
                                                col8_1, col8_2 = st.columns(2)
                                                with col1_1:
                                                    st.write(f"**Checkin date**")
                                                with col1_2:
                                                    st.write(
                                                        f"{table_bill['checkin_date'][0]}")
                                                with col2_1:
                                                    st.write(f"**Checkout date**")
                                                with col2_2:
                                                    st.write(
                                                        f"{table_bill['checkout_date'][0]}")
                                                with col3_1:
                                                    st.write(f"**Room type**")
                                                with col3_2:
                                                    st.write(
                                                        f"{table_bill['room_type'][0]}")
                                                with col4_1:
                                                    st.write(
                                                        f"**Room beds**")
                                                with col4_2:
                                                    st.write(
                                                        f"{table_bill['room_beds'][0]}")
                                                with col5_1:
                                                    st.write("**Room Price**")
                                                with col5_2:
                                                    st.write(
                                                        f"{table_bill['room_price'][0]}")
                                                with col6_1:
                                                    st.write(
                                                        f"**Day Remain**")
                                                with col6_2:
                                                    st.write(
                                                        f"{table_bill['day_remain'][0]}")

                                                with col7_1:
                                                    st.write("**Price Order Water**")
                                                with col7_2:
                                                    st.write(
                                                        f"{table_bill['total_price'][0]}")
                                                st.divider()
                                                with col8_1:
                                                    st.write("**Total Price**")
                                                with col8_2:
                                                    st.write(
                                                        f"{table_bill['bill_price'][0]}")
                                            
                                                    
                                        if updated_infor_button:
                                            if int(table['Max people'][index]) == 4:
                                            #update guest infor
                                            #trường hợp 1 người / trường hợp 2 người 
                                            #1 bed 1 người / 2 beds 2 người
                                            # lst_guest_id = guest_room_data['guest_id']
                                                first_dob_date = datetime.strptime(first_guest_dob, "%Y-%m-%d")
                                                second_dob_date = datetime.strptime(second_guest_dob, "%Y-%m-%d")

                                                mydb.update_guest_info(int(guest_room_data['guest_id'][0]), first_guest_name, int(first_guest_phone), first_guest_address, first_dob_date)
                                                mydb.update_guest_info(int(guest_room_data['guest_id'][1]), second_guest_name, int(second_guest_phone), second_guest_address, second_dob_date)
                                            elif int(table['Max people'][index]) == 2:
                                                first_dob_date = datetime.strptime(first_guest_dob, "%Y-%m-%d")
                                                mydb.update_guest_info(int(guest_room_data['guest_id'][0]), first_guest_name, int(first_guest_phone), first_guest_address, first_dob_date)

                                            #update order
                                            
                                            mydb.update_order(booking_id, 'water', water_bottle)
                                            mydb.update_order(booking_id, 'coca', coca_bottle)
                                            mydb.update_order(booking_id, 'pessi', pessi_bottle)

                                            #từ booking_id => update order
                                            #từ item_id => update inventory
                                            mydb.update_inventory('water', water_bottle - water_order)
                                            mydb.update_inventory('coca', coca_bottle - coca_order)
                                            mydb.update_inventory('pessi', pessi_bottle - pessi_order)




                            
                            with Room_Infor_Column:
                                isUpdate = False 
                                with st.form("Room inforamtion"):                                 
                                    with st.container():
                                        st.subheader(
                                            f"ROOM ID: :blue[{table['Room ID'][index]}]")
                                        row_1_1, row_1_2 = st.columns(2)
                                        row_2_1, row_2_2 = st.columns(2)
                                        row_3_1, row_3_2 = st.columns(2)
                                        row_4_1, row_4_2 = st.columns(2)
                                        with row_1_1:
                                            room_name = st.text_input(
                                                "Room name", f"{table['Room Name'][index]}")
                                        with row_1_2:
                                            floor_values = [1,2]
                                            floor = st.selectbox("Floor", floor_values,index= floor_values.index(table['Floor'][index]))
                                        with row_2_1:
                                            room_type_values = ["VIP","NORMAL"]
                                            room_type = st.selectbox("Room type",room_type_values, index = room_type_values.index(table["Room type"][index]))
                                                
                                        with row_2_2:
                                            room_price = st.text_input(
                                                "Price", f"{table['Room price'][index]}")
                                        with row_3_1:
                                            room_bed = st.text_input(
                                                "Number of bed", f"{table['Room beds'][index]}")
                                        with row_3_2:
                                            max_pp = st.text_input(
                                                "Max people", f"{table['Max people'][index]}")          
                                        with row_4_1:
                                            status_values = ["Available","Occupied"]
                                            status = st.selectbox(
                                                "Status", status_values, index = status_values.index(table["Status"][index]))
                                        with row_4_2:
                                            isActive = st.text_input(
                                                "Is active", f"{table['is Active'][index]}")
                                        _, _,col3_button = st.columns(3)
                                        
                                        with col3_button:   
                                            Update_Room_Button = st.form_submit_button("Update the room", type = "primary") 
                                            if Update_Room_Button:
                                                isUpdate = True
                                                #update room
                                                mydb.update_room(room_name,floor,room_type,room_price,room_bed,max_pp,status,isActive,table['Room ID'][index])
                                    
                                        if isUpdate:          
                                            update_success_msg = st.success("You have updated the information of the room") 
                                            time.sleep(1)
                                            update_success_msg.empty()

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
                            #insert a room
                        

        if isNoti:
            suscess_message = st.success("The room has been added")
            time.sleep(2)
            suscess_message.empty()