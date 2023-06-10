import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image, ImageDraw
from database import DataBase
from app import Owner_App, Manager_App, Staff_App
import time
import os

import base64
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


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

st.set_page_config(layout="wide")


#Authenticate 
#hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {"usernames":{}}
for user, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({user:user_dict})

authenticator = stauth.Authenticate(credentials, "HMS", "auth", cookie_expiry_days=0)

#Login Panel
#set sidebar color

# FFF0F5
with st.sidebar: 
    _ , col1,_, _, _ = st.columns(5)

    with col1:
        image = Image.open('assets/image_1.png')
        st.image(image, width=120)
    
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
        st.markdown(f'''
            <h3 style='text-align: center;  color: red;'>{name.upper()} - {staff_role.upper()}</h3>
            ''', unsafe_allow_html=True)
        authenticator.logout('Logout', 'sidebar')

       
        

elif st.session_state['authentication_status'] == False: 
    #Our demo image
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: 	#ffbd00a2;
        }
    </style>
    """, unsafe_allow_html=True)    
    set_background('./assets/background/image1.jpg')
    st.sidebar.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: 	#ffbd0095;
        }
    </style>
    """, unsafe_allow_html=True)
    set_background('./assets/background/image1.jpg')
    st.sidebar.warning('Please enter your username and password')