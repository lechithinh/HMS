import streamlit as st
import streamlit_authenticator as stauth
from database import DataBase
from app import Owner_App, Manager_App, Staff_App
import time
import os

#Load variables
from dotenv import load_dotenv #pip install python-dotenv
load_dotenv()
PORT= os.getenv('PORT')
USERNAME= os.getenv('USER')
PASSWORD= os.getenv('PASSWORD')
DATABASE= os.getenv('DATABASE')

mydb = DataBase(PORT, USERNAME, PASSWORD, DATABASE)
    

staff_login = mydb.get_staff_login()
names = staff_login['staff_name']
usernames = staff_login['username']
hashed_passwords = staff_login['password']



#configure streamlit width
st.set_page_config(layout="wide")

#Authenticate 
#hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {"usernames":{}}
for user, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({user:user_dict})

authenticator = stauth.Authenticate(credentials, "HMS", "auth", cookie_expiry_days=0)

#Login Panel
with st.sidebar: 
    name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state['authentication_status']: #Login successfully
    time.sleep(1)
    #The app
    staff_id = mydb.get_staff_id(username)
    staff_role = mydb.get_staff_role(staff_id)
    if staff_role == "Owner":
        Owner_App(mydb, staff_id)
    elif staff_role == "Manager":
        Manager_App(mydb, staff_id)
    else:
        Staff_App(mydb, staff_id) 
    with st.sidebar:
        st.divider()
        authenticator.logout('Logout', 'sidebar')

elif st.session_state['authentication_status'] == False: 
    #Our demo image
    st.image('http://placekitten.com/300/250')
    st.sidebar.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    #Our demo image
    st.image('http://placekitten.com/300/250')
    st.sidebar.warning('Please enter your username and password')