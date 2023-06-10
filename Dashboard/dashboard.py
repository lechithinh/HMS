import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image


def Dashboard(mydb):

    
    #get room table
    room_table = mydb.get_room_table()
    status_count = {'Available':0, 'Occupied':0}
    
    #total rooms
    total_rooms = len(room_table['Room ID'])
    for status in room_table['Status']:
        if status == 'Available':
            status_count['Available'] +=1
        else:
            status_count['Occupied'] +=1
            
    #get inventory table
    inventory_table = mydb.get_inventory_table()
    item_name = inventory_table['item_name']
    
    manager_card, staff_card, desk_card = st.columns(3)
    manager_card.metric(label="Total rooms", value=total_rooms)
    staff_card.metric(label="Total Inventory", value=5)
    desk_card.metric(label="Total Staff", value=5)
    style_metric_cards(border_left_color='#F39D9D')
 

    st.divider()
    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        chart_data = pd.DataFrame(
            [inventory_table['remain']],
            item_name)

        st.line_chart(chart_data)

    with fig_col2:
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=["a", "b", "c"])

        st.bar_chart(chart_data)
    st.divider()
    row_1_1,  row_1_2, row_1_3 = st.columns(3)
    with row_1_1:
        image = Image.open('assets/image_1.png')
        st.image(image, width=120)
        
    with row_1_2:
        st.write(":blue[**Hotel information**]")
        st.write(":blue[Hotel Management System]")
    with row_1_3:
        st.write(":blue[**Contact with**]")
        st.write("📱 :blue[+84-974-02038]")
        st.write("📨 :blue[hotelvipro@gmail.com]")
        
    st.divider()
    image_map = Image.open('assets\map.png')
    st.image(image_map)