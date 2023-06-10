import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
def LoginPageInfor():
    st.markdown(f'''
            <h2 style='text-align: center;  color: black;'>HMSpro | HOTEL MANAGEMENT SYSTEM </h2>
            ''', unsafe_allow_html=True)
    st.write(f"**HMSpro** is a cutting-edge, cloud-based solution that empowers small hoteliers to manage their property more effectively and achieve greater success.")
    col1, col2, col3 = st.columns(3)
    with col1: 
        image1 = Image.open('assets/data_centralization.png')
        st.image(image1, width=300, caption="Data centralization")
        image7 = Image.open('assets/configuration.png')
        st.image(image7, width=300, caption="Easy Configuration")
    with col2:
        image3 = Image.open('assets/data_statistics.png')
        st.image(image3, width=305, caption="Data statistics")
        image5 = Image.open('assets/room_management.png')
        st.image(image5, width=305, caption="Room Management")
    with col3: 
        image3 = Image.open('assets/staff_management.png')
        st.image(image3, width=305, caption="Staff Management")
        image4 = Image.open('assets/inventory_management.png')
        st.image(image4, width=305, caption="Inventory Management")


def DisplayTextCenter(TextContent):
    return st.markdown(f'''
            <h3 style='text-align: center;  color: #1E90FF;'>{TextContent}</h3>
            ''', unsafe_allow_html=True)


def AddFourRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
    row_4_1, row_4_2 = st.columns(2)
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2], [row_4_1, row_4_2]]
    return rows_columns 

def AddThreeRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
  
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2]]
    return rows_columns 

def AddFiveRows():
    row_1_1, row_1_2 = st.columns(2)
    row_2_1, row_2_2 = st.columns(2)
    row_3_1, row_3_2 = st.columns(2)
    row_4_1, row_4_2 = st.columns(2)
    row_5_1, row_5_2 = st.columns(2)
    rows_columns = [[row_1_1, row_1_2], [row_2_1, row_2_2],[row_3_1, row_3_2], [row_4_1, row_4_2], [row_5_1, row_5_2]]
    return rows_columns 


#Side bar
def Owner_sidebar():
    selected = option_menu(f"HMS System", ["Dashboard", 'Rooms', 'Inventory', 'Staff', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill',
                                     'house-fill', 'person-lines-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected

def Manager_sidebar():
    selected = option_menu(f"HMS System", ["Dashboard", 'Rooms', 'Inventory', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill',
                                     'house-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected

def Staff_sidebar():
    selected = option_menu(f"HMS System", ['Rooms', 'Inventory', 'Edit Profile'],
                            icons=['grid-1x2-fill',
                                     'house-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected