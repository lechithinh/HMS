import streamlit as st
from streamlit_option_menu import option_menu


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
    selected = option_menu(f"Welcome {st.session_state['name']}", ["Dashboard", 'Rooms', 'Inventory', 'Staff', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill',
                                     'house-fill', 'person-lines-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected

def Manager_sidebar():
    selected = option_menu(f"Welcome {st.session_state['name']}", ["Dashboard", 'Rooms', 'Inventory', 'Edit Profile'],
                            icons=['kanban-fill', 'grid-1x2-fill',
                                     'house-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected

def Staff_sidebar():
    selected = option_menu(f"Welcome {st.session_state['name']}", ['Rooms', 'Inventory', 'Edit Profile'],
                            icons=['grid-1x2-fill',
                                     'house-fill', 'person-fill'],
                            menu_icon="cast",
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#f1f2f6"},
        })
    return selected