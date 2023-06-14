import streamlit as st

from global_helpers import Owner_sidebar, Manager_sidebar, Staff_sidebar

#Module
from Dashboard.dashboard import Dashboard
from Rooms.rooms import Rooms
from Inventory.inventory import Inventory
from Staff.staff import Staff
from Profile.profile import Profile



def Owner_App(mydb, staff_id):
    # SideBar
    with st.sidebar:
        selected = Owner_sidebar()

    if selected == "Dashboard":
        Dashboard(mydb)
    elif selected == "Rooms":
        Rooms(mydb, staff_id)
    elif selected == "Inventory":
        Inventory(mydb)
    elif selected == "Staff":
        Staff(mydb, staff_id)
    else:
        Profile(mydb, staff_id)
        
def Manager_App(mydb, staff_id):
        # SideBar
    with st.sidebar:
        selected = Manager_sidebar()
    if selected == "Dashboard":
        Dashboard(mydb)
    elif selected == "Rooms":
        Rooms(mydb, staff_id)
    elif selected == "Inventory":
        Inventory(mydb)
    else:
        Profile(mydb, staff_id)

def Staff_App(mydb, staff_id):
    with st.sidebar:
        selected = Staff_sidebar()
    if selected == "Rooms":
        Rooms(mydb, staff_id)
    elif selected == "Inventory":
        Inventory(mydb)
    else:
        Profile(mydb, staff_id)

      