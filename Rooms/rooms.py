import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import time
# import datetime
from datetime import datetime, timedelta

#Helpers
from global_helpers import DisplayTextCenter

from Rooms.room_supports import guest_validation, room_validation, num_guest, get_max_people,update_room_validation


class Rooms_Module:
    def __init__(self, mydb):
        self.mydb = mydb
    def Update_room_infor(self, table, index):
        isUpdate = False 
        with st.form("Room inforamtion"):                                 
            with st.container():
                st.subheader(
                    f"ROOM NAME: :blue[{table['Room Name'][index]}]")
                current_room_name = table['Room Name'][index]
                current_room_status = table['Status'][index]
                row_1_1, row_1_2 = st.columns(2)
                row_2_1, row_2_2 = st.columns(2)
                row_3_1, _ = st.columns(2)
                # row_4_1, _ = st.columns(2)
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
                    room_price = st.number_input("Price (VND)", min_value=500000, step=50000, value=table["Room price"][index] )
                with row_3_1:
                    num_bed_values = [1,2]
                    if current_room_status == "Available":
                        disable = False
                    else:
                        disable = True
                    room_bed = st.selectbox("Number of bed",num_bed_values,num_bed_values.index(table["Room beds"][index]), disabled= disable)
    
  
                Update_Room_Button = st.form_submit_button("Update the room", type = "primary") 
                if Update_Room_Button:
                    with st.spinner('Processing...'):
                        time.sleep(2)
                    #check validation of information 
                    list_room_name = table['Room Name']
                    check_valid_info = update_room_validation(list_room_name,current_room_name,room_name,floor,room_type,room_price,room_bed)

                    if check_valid_info == False:
                        st.error("Please retype the information")
                    else:
                        isUpdate = True
                        #update room
                        max_pp = get_max_people(room_bed)
                        self.mydb.update_room(room_name,floor,room_type,room_price,room_bed,max_pp,table['Room ID'][index])

                if isUpdate:            
                    update_success_msg = st.success("You have updated the information of the room") 
                    time.sleep(1)
                    update_success_msg.empty()
                    st.experimental_rerun()
        
    def view_available_room(self, table, index):
        checkin_column, room_infor_column = st.columns(2)
        with checkin_column:
            with st.form("Room Checkin"):    
                st.subheader(
                f"INFORMATION: :blue[CHECKIN]")                                
                with st.container():
                    reservation_1_1, reservation_1_2 = st.columns(2)
                    reservation_2_1, reservation_2_2 = st.columns(2)
                    reservation_3_1, reservation_3_2 = st.columns(2)
                    reservation_4_1, reservation_4_2 = st.columns(2)
                    date_1, date_2 = st.columns(2)
                    num_guest_1, num_guest_2 = st.columns(2)

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
                        #dob có thể chỉnh từ 1/1/1950 -> 1/1/2050 ==> change to 2004
                        #muốn thay đổi thì chỉnh min và max value
                        first_guest_dob = st.date_input(
                            "Date of Birth",min_value=datetime(1950, 1, 1), max_value= datetime(2050,1,1), value=datetime(2004,1,1))

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
                                "Date of Birth", key="second guest dob",min_value=datetime(1950, 1, 1), max_value= datetime(2050,1,1), value=datetime(2004,1,1))

                    now = datetime.now()
                    with date_1:
                        checkin_date = st.date_input("Check-in date", max_value=datetime.now(), min_value=datetime.now())

                        checkin_time = st.time_input('Check-in time', value=datetime(now.year,now.month,now.day,hour=12))
                        checkin_datetime = datetime.combine(checkin_date, checkin_time)
                        
                    with date_2:
                        tomorrow =  now + timedelta(days=1)
                        #checkout date mặc định ngày hôm sau ngày checkin
                        checkout_date = st.date_input("Check-out date",value= tomorrow, min_value= tomorrow, max_value=datetime(2050,1,1))
                        checkout_time = st.time_input("Check-out time",datetime(now.year,now.month,now.day,hour=12 ), disabled=True )
                        checkout_datetime = datetime.combine(checkout_date, checkout_time)

                    #với mỗi phòng có số lượng bed khác nhau sẽ có số lượng max adult, max children khác nhau
                    # bed = 1: max adult = 2, max child = 1     min adult = 1, min child = 0
                    # bed = 2: max adult = 4, max child = 2     min adult = 2, min child = 0
                    
                    max_adult, max_child, default_value = num_guest(table["Room beds"][index])
                    
                    with num_guest_1:
                        num_adult = st.number_input("Num. adults", key="number adults", min_value=1, max_value= max_adult, value=default_value)
                    with num_guest_2:
                        num_child = st.number_input("Num. children", key="number children", min_value=0, max_value= max_child)

                    #get the current inventory table
                    inventory_table = self.mydb.get_inventory_table_in_room()
                    #list used to store slider (num slider = num item in inventory list)
                    slider_list = [""] * len(inventory_table["item name"])
                    
                    #create slider
                    with st.expander("**:blue[Hotel Services]**", expanded=False):
                        for idx,item_name  in enumerate(inventory_table["item name"]):
                            slider_list[idx] = st.slider(f"Number of {item_name}",0, inventory_table["remain"][idx])


                checkin_button = st.form_submit_button("Checkin", type = "primary")
                
                if checkin_button:
                    with st.spinner('Processing...'):
                        time.sleep(2)

                    # kiểm tra thông tin check-in
                    check_valid_info_1 = True
                    check_valid_info_2 = True

                    check_valid_info_1 = guest_validation(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob,"first")

                    if table['Room beds'][index] == 2:
                        check_valid_info_2 = guest_validation(second_guest_name,second_guest_phone,second_guest_address,second_guest_dob,"second")

                    
                    if check_valid_info_1 == False or check_valid_info_2 == False:
                        st.error("Please retype the information!")
                    else:
                        #update to guest infor to data
                        if(int(table['Max people'][index]) == 2):

                            self.mydb.add_a_guest(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob)
                            
                        else:
                            self.mydb.add_a_guest(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob)
                            self.mydb.add_a_guest(second_guest_name,second_guest_phone,second_guest_address,second_guest_dob)

                    
                        #change status to occupied
                        self.mydb.check_in_room(table['Room ID'][index])

                        
                        # add booking
                        self.mydb.add_a_booking(table['Room ID'][index], checkin_datetime, checkout_datetime,num_adult,num_child,'FALSE')

                        #get booking id
                        booking_id = self.mydb.get_booking_id(table['Room ID'][index])

                        # add booking-guest
                        num_pp = int(table['Max people'][index])/2
                        guest_id = self.mydb.get_guest_id(int(num_pp)) # list of guest id
                        self.mydb.add_a_booking_guest(booking_id, guest_id)

                        #item with order amount > 0 will be added
                        for idx,item_slider in enumerate(slider_list):
                            if item_slider > 0:

                                #update orders
                                self.mydb.insert_order(booking_id,inventory_table['item name'][idx],item_slider)

                                #update inventory 
                                self.mydb.update_inventory(inventory_table['item name'][idx],item_slider)
                        

                        #show sucessfully login message and rerun
                        with st.spinner('Processing...'):
                            time.sleep(4)
                        checkin_success_msg = st.success("The check-in process has been completed successfully") 
                        time.sleep(1)
                        checkin_success_msg.empty()
                        st.experimental_rerun()

                    
        with room_infor_column:
            self.Update_room_infor(table, index)
    
    


    def view_occupied_room(self, table,index, staff_id):
        #Lấy dữ liệu của guest view lên và dữ liệu của order và của inventory (số lượng còn lại)
        guest_room_data = self.mydb.get_guest_of_room(table['Room ID'][index], 'FALSE')
        booking_id = self.mydb.get_booking_id(table['Room ID'][index])
        
        #get the current inventory table
        inventory_table = self.mydb.get_inventory_table_in_room()

        #get the order table of room 
        order_table = self.mydb.get_order_of_room(booking_id)

        #list used to store slider
        slider_list = [""] * len(inventory_table["item name"])

        


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
                        first_guest_dob = st.date_input("Date of Birth",value=guest_room_data['date_of_birth'][0])
                        
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
                    

                    #ý tưởng: lấy 2 table là inventory table và order table (ds order của 1 phòng)
                        # nếu món item nào có trong inventory mà không có trong order => thì min_vl = 0
                        # nếu món item nào có trong invenotry và có trong order => thì min_vl = số lượng đã order
                    #min_val: order amount of an item   max_val: remaining amount of an item in inventory
                    with st.expander("**:blue[Hotel Services]**", expanded=False):
                        for idx, item_name in enumerate(inventory_table["item name"]):
                            if item_name not in order_table["item name"]:
                                slider_list[idx] = st.slider(f"Number of {item_name}",0, inventory_table["remain"][idx])
                            else:
                                slider_list[idx] = st.slider(f"Number of {item_name}", order_table["order amount"][order_table["item name"].index(item_name)], inventory_table["remain"][idx])
            
                
                    
                    #Checkout and update button
                    checkout_col,_ ,_, update_col = st.columns(4)
                    with checkout_col:
                        checkout_button = st.form_submit_button("Checkout", type = "primary")
                    with update_col:
                        updated_infor_button = st.form_submit_button("Update infor", type = "primary")
                    
                    if checkout_button:
                        #total charge = room price + service price
                        table_bill = self.mydb.finalize_a_bill(booking_id)
                        
                        isUpdateStatus = self.mydb.Update_room_status(table['Room ID'][index])

                        #update booking status --> after checkout, booking status change to 'isClose'
                        isUpdateBook = self.mydb.Update_isClose_booking(table['Room ID'][index])
                            #add to bill database
                        total_price = table_bill['bill_price'][0]
                        isAddbill = self.mydb.add_bill(booking_id, table['Room ID'][index], staff_id, total_price)
                       
                        with st.expander("**:blue[TOTAL SUMMARY]**", expanded= True):
                            st.divider()
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
                                st.write(f"**Checkout Date**")
                            with col2_2:
                                st.write(
                                    f"{table_bill['checkout_date'][0]}")
                            with col3_1:
                                st.write(f"**Room Type**")
                            with col3_2:
                                st.write(
                                    f"{table_bill['room_type'][0]}")
                            with col4_1:
                                st.write(
                                    f"**Room Beds**")
                            with col4_2:
                                st.write(
                                    f"{table_bill['room_beds'][0]}")
                            with col5_1:
                                st.write("**Room Charge**")
                            with col5_2:
                                st.write(
                                    f"**:red[{table_bill['room_price'][0]}]** VND")
                            with col6_1:
                                st.write(
                                    f"**Staying**")
                            with col6_2:
                                st.write(
                                    f"{table_bill['day_remain'][0]} Days")

                            with col7_1:
                                st.write("**Service Charge**")
                            with col7_2:
                                st.write(
                                    
                                    f"**:red[{table_bill['order_price'][0]}]** VND")
                            st.divider()
                            with col8_1:
                                st.write("**Total Charge**")
                            with col8_2:
                                st.write(
                                    f"**:red[{table_bill['bill_price'][0]}]** VND")
                            
                            if isUpdateStatus and isUpdateBook and isAddbill:
                                with st.spinner('Processing...'):
                                    time.sleep(3)
                                checkout_sucess_msg = st.success("The checkout process has been completed successfully")
                                time.sleep(3)
                                checkout_sucess_msg.empty()
                                
                            
                                

                                    
                    if updated_infor_button:
                        with st.spinner('Processing...'):
                            time.sleep(2)
                        check_valid_info_1 = True
                        check_valid_info_2 = True

                        check_valid_info_1 = guest_validation(first_guest_name,first_guest_phone,first_guest_address,first_guest_dob,"first")

                        if table['Room beds'][index] == 2:
                            check_valid_info_2 = guest_validation(second_guest_name,second_guest_phone,second_guest_address,second_guest_dob,"second")

                        if check_valid_info_1 == False or check_valid_info_2 == False:
                            st.error("Please retype the information!")
                        else:
                            if int(table['Max people'][index]) == 4:
                            #update guest infor
                            #trường hợp 1 người / trường hợp 2 người 
                            #1 bed 1 người / 2 beds 2 người
                            # lst_guest_id = guest_room_data['guest_id']
                                # first_dob_date = datetime.strptime(first_guest_dob, "%Y-%m-%d")
                                # second_dob_date = datetime.strptime(second_guest_dob, "%Y-%m-%d")

                                self.mydb.update_guest_info(int(guest_room_data['guest_id'][0]), first_guest_name, first_guest_phone, first_guest_address, first_guest_dob)
                                self.mydb.update_guest_info(int(guest_room_data['guest_id'][1]), second_guest_name, second_guest_phone, second_guest_address, second_guest_dob)
                            elif int(table['Max people'][index]) == 2:
                                # first_dob_date = datetime.strptime(first_guest_dob, "%Y-%m-%d")
                                self.mydb.update_guest_info(int(guest_room_data['guest_id'][0]), first_guest_name,first_guest_phone, first_guest_address, first_guest_dob)

                            #update order
                            #item có số lượng >0 mới được thêm vào
                            for idx,item_slider in enumerate(slider_list):
                                if item_slider > 0:
                                    self.mydb.update_order(booking_id, inventory_table['item name'][idx],item_slider)
                                    if inventory_table['item name'][idx] not in order_table['item name']:
                                        self.mydb.update_inventory(inventory_table['item name'][idx],item_slider)
                                    else:
                                        self.mydb.update_inventory(inventory_table['item name'][idx],item_slider - order_table['order amount'][order_table['item name'].index( inventory_table['item name'][idx])])
                                    
                            
                    
                            with st.spinner('Processing...'):
                                time.sleep(2)
                            checkin_success_msg = st.success("Update successfully") 
                            time.sleep(1)
                            checkin_success_msg.empty()
                            st.experimental_rerun()

                        

        with Room_Infor_Column:
            self.Update_room_infor(table, index)
    def View_room_infor(self, room_table, staff_id):
        #Cards 
        status_count = {'Available':0, 'Occupied':0}
        total_rooms = len(room_table['Room ID'])
        for role in room_table['Status']:
            if role == 'Available':
                status_count['Available'] +=1
            else:
                status_count['Occupied'] +=1
            
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Available", value=status_count['Available'])
        col2.metric(label="Occupied", value=status_count['Occupied'])
        col3.metric(label="Total Rooms", value=total_rooms)
        style_metric_cards(border_left_color='#F39D9D')



        table = st.data_editor(room_table, use_container_width=True, hide_index = 1, column_config={"Room ID": None, "is Active": None, "Created at": None, "Max people": None})

        # Only one room can be selected
        count = 0
        for row in table['View information']:
            if row == True:
                count +=1
        if count > 1:
            st.error("**Please select a single record.!**", icon="🚨")
        else:
            for value in table['View information']:
                if value:
                        index = table['View information'].index(value)
                        #Show an expander for the selected room
                        if table["Status"][index] == "Available":
                                self.view_available_room(table, index)
                        if table["Status"][index] == "Occupied":   
                                self.view_occupied_room(table, index, staff_id)
                               
    def Add_a_room(self, table):
        #init data
        isNoti = False
        list_room_name = table['Room Name']
        
        DisplayTextCenter("ADD A NEW ROOM")
        
        with st.form("Add new room"):                                 
            with st.container():
                row_1_1, row_1_2 = st.columns(2)
                row_2_1, row_2_2 = st.columns(2)
                row_3_1, _ = st.columns(2)
                with row_1_1:
                    room_name = st.text_input(':blue[**Room Name**]', placeholder='Enter the room name')
                with row_1_2:
                    room_type =   st.selectbox(
                        ':blue[**Select the type**]',
                        ('NORMAL', 'VIP'))
                with row_2_1:
                    floor = st.selectbox(
                        ':blue[**Select the floor**]',
                        ('1', '2'))
                with row_2_2:
                    room_price = st.number_input(':blue[**Room price**]', min_value=500000, step=50000 )
                
                with row_3_1:
                    beds = st.selectbox(':blue[**Select number of beds**]',
                        (1, 2))

                Add_room_button = st.form_submit_button("Add a room", type = "primary")
                if Add_room_button:
                    with st.spinner('Processing...'):
                        time.sleep(2)
                        
                    #UPDATED ROOM VALIDATION
                    check_valid_info = room_validation(list_room_name,room_name, floor, room_type,room_price, beds)

                    if check_valid_info == False:
                        st.error("Please retype the information")
                    else:
                        isNoti = True
                        max_people = get_max_people(beds)
                        self.mydb.add_a_room(room_name, floor, room_type, room_price, beds,max_people),
                        

        if isNoti:
            suscess_message = st.success("The room has been added")
            time.sleep(1)
            suscess_message.empty()
            room_name = ""
            st.experimental_rerun()



def Rooms(mydb, staff_id):
    room_information_tab, add_room_tab = st.tabs(["**VIEW ROOM INFORMATION**",
                            "**ADD A ROOM**"])
    
    #Init instance
    Rooms_instance = Rooms_Module(mydb)
    room_table = mydb.get_room_table()
    with room_information_tab:   
        Rooms_instance.View_room_infor(room_table, staff_id)

    with add_room_tab:
       Rooms_instance.Add_a_room(room_table)