import streamlit as st


def StaffProfile(mydb,staff_id):
    st.markdown('''
            <h3 style='text-align: center;  color: black;'>EDIT YOUR PROFILE</h3>
            ''', unsafe_allow_html=True)
    staff_data = mydb.get_a_staff(staff_id)
    with st.form("Add a new item"):
        isUpdatedSucess = False              
        with st.container():
                row_1_1, row_1_2 = st.columns(2)
                row_2_1, row_2_2 = st.columns(2)
                row_3_1, row_3_2 = st.columns(2)
                with row_1_1:
                    staff_name = st.text_input("Your Name", staff_data[0])
                with row_1_2:
                    staff_phone = st.text_input("Your Phone", staff_data[1])
                with row_2_1:
                    staff_address = st.text_input("Your Address", staff_data[2])
                with row_2_2:
                    staff_date = st.date_input("Your Date Of Birth",value=staff_data[3])
                with row_3_1:
                    staff_username = st.text_input("Your User Name", staff_data[4], disabled=True)
                with row_3_2:
                    staff_role = st.text_input("Your Role", staff_data[5], disabled=True)
                    _, _, _, _,_, col6 = st.columns(6)
                    with col6:
                        update_profile = st.form_submit_button("Save", type = "primary") 
                        if update_profile:
                            isUpdatedSucess = mydb.Update_One_Staff(staff_name,staff_phone,staff_address,staff_date,staff_username,staff_role,staff_id)
                            
                if isUpdatedSucess:
                    st.success("You update has been completed")