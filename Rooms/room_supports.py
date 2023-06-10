import streamlit as st
import string

def check_phone(guest_phone):
    for temp in guest_phone:
        if temp.isalpha():
            return False
    return True

def check_name(guest_name):
    for temp in guest_name:
        if temp.isnumeric():
            return False
    return True

def guest_validation(guest_name, guest_phone, guest_address, guest_dob, stt_guest):
    isValid = True

    # check guest name 
    if len(guest_name) == 0 or check_name(guest_name) == False:
        isValid = False
        st.error(f"Check **name** of {stt_guest} guest again!")
        print(guest_name)

    # check guest phone
    if len(guest_phone) != 10 or check_phone(guest_phone) == False:
        isValid = False
        print(guest_phone)
        st.error(f"Check **phone number** of {stt_guest} guest again!")

    if len(guest_address) == 0:
        isValid = False
        st.error(f"Check **address** of {stt_guest} guest again!")

    return isValid
        
# guest_validation("le chi thinh beo","222f2222222","asdasf","asdfa","first")

def room_validation(list_of_room, room_name, floor, room_type, room_price, beds, people):
    isValid = True

    # if room_name not in list_of_room or room_name == "":
    #     isValid = False
    #     st.error("Check **room name** again!")

    # if floor == "" or room_type == "" or room_price == "" or beds == "" or people == "":
    #     isValid = False
    #     st.error("Check other again")
    
    return isValid
