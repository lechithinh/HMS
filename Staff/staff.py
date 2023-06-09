import streamlit as st
import datetime
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards
import datetime
import base64
import streamlit_authenticator as stauth

#Global Helpers
from global_helpers import DisplayTextCenter, AddFourRows

class Staff_Module:
    def __init__(self, mydb):
        self.mydb = mydb
    def view_staff_infor(self):
        staff_data = self.mydb.get_staff_table()
        role_count = {'Manager':0, 'Staff':0,'Owner':0}
        for role in staff_data['Role']:
                if role == 'Manager':
                    role_count[role] += 1
                elif role == 'Staff':
                    role_count[role] += 1
                else:
                    role_count[role] +=1
        
        manager_card, staff_card, desk_card = st.columns(3)
        manager_card.metric(label="Total Manager", value=role_count['Manager'])
        staff_card.metric(label="Total Staf", value=role_count['Staff'])
        desk_card.metric(label="Total Owner", value=role_count['Owner'])
        style_metric_cards(border_left_color='#F39D9D')
        
        #Show the table data
        table_staff = st.experimental_data_editor(staff_data, use_container_width = True)
     
        for value in table_staff['Update']:
            if value :
                    index = table_staff['Update'].index(value)
                    staff_id = table_staff['Staff ID'][index]
                    username = table_staff['Username'][index]
                    #Show an expander for the selected room
                    with st.expander("", expanded=True):
                        column_card, column_infor = st.columns(2)
                            #card for the selected room
                        with column_card:
                            with open(f"assets/staff/Unknown_person.jpg", "rb") as f:
                                data = f.read()
                                encoded = base64.b64encode(data)
                            data = "data:image/png;base64," + encoded.decode("utf-8")
                            
                            card(
                                title=table_staff['Name'][index],
                                text=table_staff['Role'][index],
                                image=data,
                                url="https://github.com/gamcoh/st-card")

                            
                        #information for the selected room    
                        with column_infor:
                            
                            
                            st.subheader(
                                    f"STAFF ID: :blue[{table_staff['Staff ID'][index]}]")
                            
                            with st.form("Update Staff Information"):
                                isUpdateSucess = False 
                                isRemove = False
                                
                                with st.container():
                                    row_1_1, row_1_2 = st.columns(2)
                                    row_2_1, row_2_2 = st.columns(2)
                                    row_3_1, row_3_2 = st.columns(2)
                                    with row_1_1:
                                        staff_name = st.text_input(
                                            "Full Name", f"{table_staff['Name'][index]}")
                                    with row_1_2:
                                        staff_phone = st.text_input(
                                            'Phone Number', f"{table_staff['Phone'][index]}")
                                    with row_2_1:
                                        staff_address = st.text_input(
                                            "Address", f"{table_staff['Address'][index]}")
                                    with row_2_2:
                                        staff_role = st.selectbox(
                                            "Role", ("Manager", "Staff", "FrontDesk"))
                                    with row_3_1:
                                        date_obj = table_staff['Date Of Birth'][index]
                                        year = date_obj.year
                                        month = date_obj.month
                                        day = date_obj.day

                                        Date_of_birth = st.date_input(
                                            "Date Of Birth", datetime.date(year, month, day))
                                    with row_3_2:
                                        staff_username = st.text_input("Username", f"{table_staff['Username'][index]}", disabled=True)

                                    col1_remove_staff,_,col3_update_staff = st.columns(3)
                                    with col1_remove_staff:
                                        remove_button = st.form_submit_button("Remove")
                                        if remove_button:
                                            isRemove = True
                                            self.mydb.Hide_staff(staff_id)
                                        #Remove the user
                                    with col3_update_staff:
                                        updated_button = st.form_submit_button("Update Staff Info", type = "primary")
                                        if updated_button:
                                            isUpdateSucess = self.mydb.Update_One_Staff(
                                                staff_name, staff_phone, staff_address, Date_of_birth,staff_username,staff_role, staff_id, 
                                            )
                                        
                                if isUpdateSucess:          
                                        st.success("Staff information has been updated")      
                                if isRemove:
                                    st.success("Remove staff successful")    
    def Add_a_staff(self):
        Add_staff_message = False
        DisplayTextCenter("Add A New Staff")
            
        with st.form("Add Staff Information", clear_on_submit = True):           
            with st.container(): 
                rows_columns = AddFourRows()
                with rows_columns[0][0]:
                    Name = st.text_input(
                        "Full Name",  placeholder="Enter staff name")
                with rows_columns[0][1]:
                    Phone = st.text_input(
                        'Phone',  placeholder="Enter phone number")
                with rows_columns[1][0]:
                    username = st.text_input(
                        "Username",  placeholder="Enter Username")
                with rows_columns[1][1]:
                    password = st.text_input("Password", placeholder="Enter password")
                    if password:
                        hashed_password = stauth.Hasher([password]).generate()
                with rows_columns[2][0]:
                    Date_of_birth = st.date_input(
                        "Enter date of birth")
                with rows_columns[2][1]:
                    Role = st.selectbox(
                        "Role", ("Manager", "Staff", "Owner"))
                with rows_columns[3][0]:
                    Address = st.text_input(
                        "Address",  placeholder="Enter address")
                with rows_columns[3][1]:
                    salary = st.number_input(
                        'Salary', 5000000
                    )
                    _, _, col3_button = st.columns(3)
                    with col3_button:   
                        add_button = st.form_submit_button("Create the staff info", type = "primary")
                        if add_button:
                            Add_staff_message = self.mydb.Add_New_Staff(Name,Phone,username,hashed_password[0],Date_of_birth,Role, Address)

                    
        if Add_staff_message:
            st.success("You have added a new staff")



def Staff(mydb):
    View_staff_infor, Add_a_staff = st.tabs(["**View staff information**", "**Add a staff**"])
    #init instance   
    Staff_instance = Staff_Module(mydb)
    with View_staff_infor:
        Staff_instance.view_staff_infor()
    with Add_a_staff:
        Staff_instance.Add_a_staff()