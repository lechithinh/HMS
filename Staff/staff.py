import streamlit as st
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime
import base64
import time
import streamlit_authenticator as stauth
from Staff.staff_helpers import display_table_staff, check_valid_phone, check_user_name, check_name_staff, check_password

# Global Helpers
from global_helpers import DisplayTextCenter, AddFourRows


class Staff_Module:
    def __init__(self, mydb):
        self.mydb = mydb

    def view_staff_infor(self, staff_id):
        staff_data = self.mydb.get_staff_table(staff_id)
        role_count = {'Manager': 0, 'Staff': 0, 'Owner': 0}
        for role in staff_data['Role']:
            if role == 'Manager':
                role_count[role] += 1
            elif role == 'Staff':
                role_count[role] += 1
            else:
                role_count[role] += 1

        manager_card, staff_card, desk_card = st.columns(3)
        manager_card.metric(label="Total Manager", value=role_count['Manager'])
        staff_card.metric(label="Total Staff", value=role_count['Staff'])
        desk_card.metric(label="Total Owner", value=role_count['Owner'])
        style_metric_cards(border_left_color='#F39D9D')

        # Show the table data
        table_staff = st.data_editor(staff_data, use_container_width=True, column_config={"Suspend at": None})

        count = 0
        for value in table_staff['Update']:
            if value:
                count += 1
        if count > 1:
            st.error("**Please select a single record.!**", icon="🚨")
        else:
            for value in table_staff['Update']:
                index = table_staff['Update'].index(value)

                if value and table_staff['Status'][index] == 'Active' :
                    staff_id = table_staff['Staff ID'][index]
                    username = table_staff['Username'][index]
                    # Show an expander for the selected room
                    with st.expander("", expanded=True):
                        column_card, column_infor = st.columns(2)
                        # card for the selected room
                        with column_card:
                            with open(f"assets/staff/staff_background.png", "rb") as f:
                                data = f.read()
                                encoded = base64.b64encode(data)
                            data = "data:image/png;base64," + \
                                encoded.decode("utf-8")

                            card(
                                title=table_staff['Name'][index],
                                text=table_staff['Role'][index],
                                image=data,
                                url="https://github.com/gamcoh/st-card")

                        # information for the selected room
                        with column_infor:

                            st.subheader(
                                f":blue[**STAFF ID**]: :blue[{table_staff['Staff ID'][index]}]")

                            with st.form("Update Staff Information"):
                                isUpdateSucess = False
                                isRemove = False

                                with st.container():
                                    row_1_1, row_1_2 = st.columns(2)
                                    row_2_1, row_2_2 = st.columns(2)
                                    row_3_1, row_3_2 = st.columns(2)
                                    with row_1_1:
                                        staff_name = st.text_input(
                                            ":blue[**Full Name**]", f"{table_staff['Name'][index]}")
                                    with row_1_2:
                                        staff_phone = st.text_input(
                                            ':blue[**Phone Number**]', f"{table_staff['Phone'][index]}")
                                    with row_2_1:
                                        staff_address = st.text_input(
                                            ":blue[**Address**]", f"{table_staff['Address'][index]}")
                                    with row_2_2:
                                        staff_role = st.selectbox(
                                            ":blue[**Role**]", ("Manager", "Staff", "Owner"))
                                    with row_3_1:
                                        Date_of_birth = st.date_input(
                                            ":blue[**Date Of Birth**]", value = table_staff['Date Of Birth'][index],  min_value=datetime(1950, 1, 1), max_value= datetime(2050,1,1)  )
                                        
                                     
                                    with row_3_2:
                                        staff_username = st.text_input(
                                            ":blue[**Username**]", f"{table_staff['Username'][index]}", disabled=True)

                                    col1_update_staff, _,_,_, col3_remove_staff = st.columns(5)
                                    with col3_remove_staff:
                                        remove_button = st.form_submit_button(":red[**Suspend**]")
                                        if remove_button:
                                            isRemove = True
                                            self.mydb.Hide_staff(staff_id)
                                        # Remove the user
                                    with col1_update_staff:
                                        updated_button = st.form_submit_button(
                                            "Update", type="primary")
                                        if updated_button:
                                            if check_valid_phone(staff_phone) == True and check_name_staff(staff_name) == True:
                                                isUpdateSucess = self.mydb.Update_One_Staff(
                                                    staff_name, staff_phone, staff_address, Date_of_birth, staff_username, staff_role, staff_id,
                                                )
                                            if check_valid_phone(staff_phone) == False:
                                                st.error("Phone number is invalid")
                                            if check_name_staff(staff_name) == False:
                                                st.error("Staff name must be alphabet")

                                if isUpdateSucess:
                                    st.success(
                                        "Staff information has been updated")
                                    time.sleep(1)
                                    st.experimental_rerun()
                                if isRemove:
                                    st.success("Suspend staff successful")
                                    time.sleep(1)
                                    st.experimental_rerun()
                if value and table_staff['Status'][index] == 'Suspend' :
                    active_button = st.button("Active this staff account",type="primary", key="active staff")
                    st.warning(f"**This account was suspended at {table_staff['Suspend at'][index]}**", icon="⚠️")

                    if active_button:
                        isActiveSuccess = self.mydb.Update_suspended_staff(table_staff['Staff ID'][index])
                        with st.spinner('Processing...'):
                            time.sleep(2)
                        if isActiveSuccess:
                            st.success(
                                "Staff account has been activated!")
                            time.sleep(2)
                            st.experimental_rerun()

    def Add_a_staff(self):
        Add_staff_message = False
        DisplayTextCenter("Add A New Staff")
        staff_data = self.mydb.get_all_staff_username()

        with st.form("Add Staff Information"):
            with st.container():
                rows_columns = AddFourRows()
                with rows_columns[0][0]:
                    Name = st.text_input(
                        ":blue[**Full Name**]",  placeholder="Enter staff name")
                with rows_columns[0][1]:
                    Phone = st.text_input(
                        ':blue[**Phone**]',  placeholder="Enter phone number")
                with rows_columns[1][0]:
                    username = st.text_input(
                        ":blue[**Username**]",  placeholder="Enter Username")
                with rows_columns[1][1]:
                    password = st.text_input(
                        ":blue[**Password**]", placeholder="Enter password", type="password")

                    if password:
                        hashed_password = stauth.Hasher([password]).generate()
                with rows_columns[2][0]:
                    Date_of_birth = st.date_input(
                            ":blue[**Date of birth**]", min_value=datetime(1950, 1, 1), max_value= datetime(2050,1,1), value=datetime(2004,1,1))
                with rows_columns[2][1]:
                    Role = st.selectbox(
                        ":blue[**Role**]", ("Manager", "Staff", "Owner"))
                with rows_columns[3][0]:
                    Address = st.text_input(
                        ":blue[**Address**]",  placeholder="Enter address")
                with rows_columns[3][1]:
                    salary = st.number_input(
                        ':blue[**Salary**]', 5000000
                    )

            add_button = st.form_submit_button("Create", type="primary")
            if add_button:
                with st.spinner('Processing...'):
                    time.sleep(2)
                if len(Name) == 0 or len(Phone) == 0 or len(username) == 0 or len(password) == 0 or len(Address) ==0:
                    st.error("Must enter full information!")
                else:
                    if check_password(password) == False:
                        st.error("Password must be at least 8 characters long and contain at least one number, and one special character")
                    if check_valid_phone(Phone) and check_user_name(username, staff_data) and check_name_staff(Name):
                        Add_staff_message = self.mydb.Add_New_Staff(
                                Name, Phone, username, hashed_password[0], Date_of_birth, Role, Address)
                    if check_valid_phone(Phone) == False:
                        st.error("Phone number is invalid")
                    if  check_user_name(username, staff_data) == False:
                        st.error("The username already exists! Please choose another one")
                    if check_name_staff(Name) == False:
                        st.error("Staff name must be alphabet")
                                
                                

        if Add_staff_message:
            st.success("You have added a new staff")
            time.sleep(1)
            st.experimental_rerun()


def Staff(mydb, staff_id):
    View_staff_infor, Add_a_staff = st.tabs(
        ["**View staff information**", "**Add a staff**"])
    # init instance
    Staff_instance = Staff_Module(mydb)
    with View_staff_infor:
        Staff_instance.view_staff_infor(staff_id)
    with Add_a_staff:

        Staff_instance.Add_a_staff()


