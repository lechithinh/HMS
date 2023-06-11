import streamlit as st
import time

import streamlit_authenticator as stauth

#Helpers
from global_helpers import DisplayTextCenter
from Staff.staff_helpers import check_valid_phone, check_name_staff, check_password


    
def Profile(mydb, staff_id):
    #Show the title
    DisplayTextCenter("Edit Your Profile")
    
    staff_data = mydb.get_a_staff(staff_id)
    with st.form("Add a new item"):
        isUpdatedSucess = False              
        with st.container():
                row_1_1, row_1_2 = st.columns(2)
                row_2_1, row_2_2 = st.columns(2)
                row_3_1, row_3_2 = st.columns(2)

                row_4_1, row_4_2= st.columns(2)
                with row_1_1:
                    staff_name = st.text_input(":blue[**Your Name**]", staff_data[0])
                with row_1_2:
                    staff_phone = st.text_input(":blue[**Your Phone**]", staff_data[1])
                with row_2_1:
                    staff_address = st.text_input(":blue[**Your Address**]", staff_data[2])
                with row_2_2:
                    staff_date = st.date_input(":blue[**Your Date Of Birth**]",value=staff_data[3])
                with row_3_1:
                    staff_username = st.text_input(":blue[**Your User Name**]", staff_data[4], disabled=True)
                with row_3_2:
                    staff_role = st.text_input(":blue[**Your Role**]", staff_data[5], disabled=True)
                with row_4_1:
                    staff_password = st.text_input(":blue[**Your password**]", type="password")
                    if staff_password:
                        hashed_password = stauth.Hasher([staff_password]).generate()
                with row_4_2:
                    staff_note = st.text_input(":blue[**Your Note**]")
                    _, _, _, col4 = st.columns(4)
                   
                    with col4:
                        
                        update_profile = st.form_submit_button("Save settings", type = "primary") 
                        if update_profile:
                            with st.spinner('Processing...'):
                                time.sleep(2)
                            if check_password(staff_password) == False:
                                st.error("Password must have at least number, character and special character")
                            elif check_valid_phone(staff_phone) and check_name_staff(staff_name):
                                if staff_password: #update password
                                    isUpdatedSucess =  mydb.Update_Profile_Staff(staff_name,staff_phone,staff_address,staff_date,staff_username,staff_role, hashed_password[0], staff_id)
                                else: 
                                    isUpdatedSucess = mydb.Update_One_Staff(staff_name, staff_phone, staff_address, staff_date, staff_username, staff_role, staff_id)
                            elif check_valid_phone(staff_phone) == False:
                                st.error("Phone number unvalid")
                            elif check_name_staff(staff_name) == False:
                                st.error("Name must be alphabet")
                            
                if isUpdatedSucess:
                    st.success("You update has been completed")
                    time.sleep(1)
                    st.experimental_rerun()

