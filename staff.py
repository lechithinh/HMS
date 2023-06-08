import streamlit as st
import datetime
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards
import datetime
from PIL import Image
import os
import base64

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
            desk_card.metric(label="Total Owner", value=role_count['Owner'])
            style_metric_cards(border_left_color='#F39D9D')
            
            #Show the table data
            table_staff = st.experimental_data_editor(staff_data, use_container_width = True)
            
            #If there are two selected rows, please show the second selected one.
            for value in table_staff['Update']:
                if value :
                        index = table_staff['Update'].index(value)
                        staff_id = table_staff['staff_id'][index]
                        username = table_staff['username'][index]
                        #Show an expander for the selected room
                        with st.expander("", expanded=True):
                            column_card, column_infor = st.columns(2)
                             #card for the selected room
                            with column_card:
                                if os.path.exists(f"assets/staff/username_{username}.png"):

                                    with open(f"assets/staff/username_{username}.png", "rb") as f:
                                        data = f.read()
                                        encoded = base64.b64encode(data)
                                    data = "data:image/png;base64," + encoded.decode("utf-8")
                                    
                                    card(
                                        title=table_staff['Name'][index],
                                        text=table_staff['Role'][index],
                                        image=data,
                                        url="https://github.com/gamcoh/st-card"
                                    )
                                else:
                                    with open(f"assets/staff/Unknown_person.jpg", "rb") as f:
                                        data = f.read()
                                        encoded = base64.b64encode(data)
                                    data = "data:image/png;base64," + encoded.decode("utf-8")
                                    
                                    card(
                                        title=table_staff['Name'][index],
                                        text=table_staff['Role'][index],
                                        image=data,
                                        url="https://github.com/gamcoh/st-card")
                                # card(
                                #     title=table_staff['Name'][index],
                                #     text=table_staff['Role'][index],
                                #     image="http://placekitten.com/300/250",
                                #     # url="https://www.google.com",
                                #     key= staff_id
                                # )   
                                
                            #information for the selected room    
                            with column_infor:
                             
                              
                                st.subheader(
                                        f"STAFF ID: :blue[{table_staff['staff_id'][index]}]")
                             
                                with st.form("Update Staff Information"):
                                    isUpdateSucess = False 
                                    isRemove = False
                                    
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
                                                "Address", f"{table_staff['Address'][index]}")
                                        with row_2_2:
                                            Role = st.selectbox(
                                                "Role", ("Manager", "Staff", "FrontDesk"))
                                        with row_3_1:
                                            date_obj = table_staff['Date Of Birth'][index]
                                            year = date_obj.year
                                            month = date_obj.month
                                            day = date_obj.day

                                            Date_of_birth = st.date_input(
                                                "Date Of Birth", datetime.date(year, month, day))
                                        with row_3_2:
                                            Username = st.text_input("Username", f"{table_staff['username'][index]}")

                                        col1_remove_staff,_,col3_update_staff = st.columns(3)
                                        with col1_remove_staff:
                                            remove_button = st.form_submit_button("Remove")
                                            if remove_button:
                                                isRemove = True
                                                mydb.Hide_staff(staff_id)
                                            #Remove the user
                                        with col3_update_staff:
                                            updated_button = st.form_submit_button("Update Staff Info", type = "primary")
                                            if updated_button:
                                                isUpdateSucess = mydb.Update_One_Staff(
                                                    staff_id, Name, Phone, Email, Date_of_birth, Role,Username
                                                )
                                                #After updated --> should refresh the whole page

                            
                                    if isUpdateSucess:          
                                            st.success("Staff information has been updated")      
                                    if isRemove:
                                        st.success("Remove staff successful")                                   

    with Add_a_staff:
            isNoti = False
            st.markdown('''
            <h3 style='text-align: center;  color: black;'>Add a staff</h3>
            ''', unsafe_allow_html=True)
            username = ""
            with st.form("Add Staff Information", clear_on_submit = True):           
                with st.container(): 
                    isUpdateSucess = False
                    row_1_1, row_1_2 = st.columns(2)
                    row_2_1, row_2_2 = st.columns(2)
                    row_3_1, row_3_2 = st.columns(2)
                    row_4_1, row_4_2 = st.columns(2)
                    with row_1_1:
                        Name = st.text_input(
                            "Full Name",  placeholder="Enter staff name")
                    with row_1_2:
                        Phone = st.text_input(
                            'Phone',  placeholder="Enter phone number")
                    with row_2_1:
                        username = st.text_input(
                            "Username",  placeholder="Enter Username")
                    with row_2_2:
                        password = st.text_input("Password", placeholder="Enter password")
                    with row_3_1:
                        Date_of_birth = st.date_input(
                            "Enter date of birth")
                    with row_3_2:
                        Role = st.selectbox(
                            "Role", ("Manager", "Staff", "Owner"))
                    with row_4_1:
                        Address = st.text_input(
                            "Address",  placeholder="Enter address")
                    with row_4_2:
                        
                        _, _, col3_button = st.columns(3)
                        with col3_button:   
                            
                            add_button = st.form_submit_button("Create the staff info", type = "primary")
                            if add_button:
                                isNoti = mydb.Add_New_Staff(Name,Phone,username,password,Date_of_birth,Role, Address)

            uploaded_file = st.file_uploader("Choose an image....", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded image', use_column_width=True)
            
            download_btn = st.button("Save image")
            if download_btn:
                file_name = f"username_{username}.png"
                image.save(file_name)

                with open(file_name, "rb") as f:
                    data = f.read()
                    st.download_button(
                            label="Save image staff",
                            data=data,
                            file_name=file_name,
                            mime="image/png",
                                    # Specify download path
                                 )
                download_dir = "assets/staff"
                os.makedirs(download_dir, exist_ok=True)
                os.rename(file_name, os.path.join(download_dir, file_name))
            
                                
                                
                                
            if isNoti:
                st.success("You have added a new staff")