import streamlit as st
from streamlit_option_menu import option_menu


from dashboard import Dashboard
from rooms import Rooms
from inventory import Inventory
from staff import Staff

#database
from database import DataBase

#Call only once
# mydb = DataBase("localhost", "root", "huynhcongthien", "HMS")



def MyWeb(authenticator, mydb, staff_id):
    # SideBar
    with st.sidebar:
        selected = option_menu(f"Welcome {st.session_state['name']}", ["Dashboard", 'Rooms', 'Inventory', 'Staff', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill',
                                     'house-fill', 'person-lines-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })

    if selected == "Dashboard":
        Dashboard(mydb)
    elif selected == "Rooms":
        Rooms(mydb, staff_id)
    elif selected == "Inventory":
        Inventory(mydb)
    elif selected == "Staff":
        Staff(mydb)
    else:
        st.markdown('''
            <h3 style='text-align: center;  color: black;'>EDIT YOUR PROFILE</h3>
            ''', unsafe_allow_html=True)
            
        with st.form("Add a new item"):              
            with st.container():
                    row_1_1, row_1_2 = st.columns(2)
                    row_2_1, row_2_2 = st.columns(2)
                    row_3_1, row_3_2 = st.columns(2)
                    with row_1_1:
                        staff_name = st.text_input("Your Name", "Le Chi Thinh")
                    with row_1_2:
                        staff_phone = st.text_input("Your Phone", "0822043153")
                    with row_2_1:
                        staff_address = st.text_input("Your Address", "Ca Mau")
                    with row_2_2:
                        staff_date = st.text_input("Your Date Of Birth", "12/05/2003")
                    with row_3_1:
                        staff_username = st.text_input("Your User Name", "lechithinh")
                    with row_3_2:
                        staff_role = st.text_input("Your Role", "Manager", disabled=True)
                        _, _, _, _,_, col6 = st.columns(6)
                        with col6:
                            update_profile = st.form_submit_button("Save", type = "primary")
                            if update_profile:
                                pass
    

      