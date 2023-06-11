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

    
    if len(guest_phone) != 10 or check_phone(guest_phone) == False:
        isValid = False
        st.error(f"**Phone number** of {stt_guest} guest must be 10 digits!")

    if  check_phone(guest_phone) == False:
        isValid = False
        st.error(f"**Phone number** of {stt_guest} guest must be numeric!")

    if len(guest_address) == 0:
        isValid = False
        st.error(f"Check **address** of {stt_guest} guest again!")

    return isValid
        
# guest_validation("le chi thinh beo","222f2222222","asdasf","asdfa","first")

def room_validation(list_of_room, room_name, floor, room_type,room_price, beds ):
    isValid = True
    #room_name = room_name.casefold()
    #room_name = room_name.capitalize()
    if room_name in list_of_room or room_name == "":
        isValid = False
        st.error("**Room name** is not valid!")
    
    if floor == "" or room_type == "" or room_price == "" or beds == "":
        isValid = False
        st.error("Fields must not be empty!")
    
    return isValid

def update_room_validation(list_of_room,current_room_name,room_name, floor, room_type,room_price, beds):
    isValid = True
    list_of_room.remove(current_room_name)
    if room_name in list_of_room or room_name == "":
        isValid = False
        st.error("**Room name** is not valid!")
    
    if floor == "" or room_type == "" or room_price == "" or beds == "":
        isValid = False
        st.error("Fields must not be empty!")
    
    return isValid

def num_guest(num_bed):
    default_value = 1
    if num_bed == 1:
        return [2,1,default_value ]
    else:
        default_value = 2
        return [4,2,default_value]  #[num_adult, num_child] / số người mặc định 

def get_max_people(num_bed):
    max_pp = {
            1: 2,
            2: 4
        }
    return max_pp[num_bed]