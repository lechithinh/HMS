import streamlit as st
import datetime
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards


def Staff(mydb):
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