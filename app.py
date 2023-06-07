import streamlit as st
from streamlit_option_menu import option_menu


from dashboard import Dashboard
from rooms import Rooms
from inventory import Inventory
from staff import Staff
from staff_profile import StaffProfile
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
        StaffProfile(mydb, staff_id)

      