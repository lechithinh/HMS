import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image
from datetime import datetime, timedelta
import altair as alt
import json


def Dashboard(mydb):

    
    #get room table
    room_table = mydb.get_room_table()
        #get inventory table
    inventory_table = mydb.get_inventory_table()
    staff_table = mydb.get_staff_table()
    status_count = {'Available':0, 'Occupied':0}
    
    #total rooms
    total_rooms = len(room_table['Room ID'])
    count_item = len(inventory_table['item_id'])
    count_staff = len(staff_table['Staff ID'])


    for status in room_table['Status']:
        if status == 'Available':
            status_count['Available'] +=1
        else:
            status_count['Occupied'] +=1
            


    manager_card, staff_card, desk_card = st.columns(3)
    manager_card.metric(label="Room Available", value=status_count["Available"])
    staff_card.metric(label="Total Inventory", value=count_item)
    desk_card.metric(label="Total Staff", value=count_staff)
    style_metric_cards(border_left_color='#F39D9D')
    
    
    #select bill
    table_bill = mydb.get_table_bill()
    price = table_bill['total_price']   
    created = table_bill['created_at']
    dt = datetime.now()
    dt = dt.date()
    # print(dt)
    monday = dt - timedelta(days=dt.weekday())
    monday_previous = dt - timedelta(days=dt.weekday()+7)
    sunday = monday + timedelta(days=6)
    
    #take list previous week
    previous_week_dates = []
    for i in range(7):
        date = monday_previous + timedelta(days=i)
        previous_week_dates.append(date)
    #take list now week
    now_week_dates = []
    for i in range(7):
        date = monday + timedelta(days=i)
        now_week_dates.append(date)
    data = {
    'Previous': [],
    'Now': []
}
    for i in range(7):
        data["Now"].append(0)
        data["Previous"].append(0)
    
    i = 0
    for item in created:
        if item >= monday_previous and item < monday:
            for index, value in enumerate(previous_week_dates):
                if value == item:
                    data["Previous"][index] = price[i]
        elif item >= monday and item <= sunday:
            for index, value in enumerate(now_week_dates):
                if value == item:
                    data["Now"][index] = price[i]
        i += 1
    
    week_day = ["2. Monday", "3. Tuesday", "4. Wednesday", "5. Thursday", "6. Friday", "7. Saturday", "8. Sunday"]



    st.divider()
    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown(f'''<h4 style = 'color: #0068c9; text-align: center; font-weight: bold;'>Chart of the revenue comparison <br> between two consecutive week</h4>''', unsafe_allow_html=True)
        chart_data = pd.DataFrame(data, index=week_day)

        
        st.line_chart(chart_data, height=400)

    with fig_col2:
        st.markdown(f'''<h4 style = 'color: #0068c9; text-align: center; font-weight: bold;'>Chart of the number of guests in the past 7 days  </h4>''', unsafe_allow_html=True)
        guest_char_Table = mydb.guest_chart()
        temp = []
        for item in guest_char_Table["check_in date"]:
            item = json.dumps(item, default=str)
            temp.append(item[1:-1])

        data = pd.DataFrame( {
            "Date": temp,
            "Total guest": guest_char_Table["num_guest"],
        })
        chart = alt.Chart(data, height=400).mark_bar().encode(x=alt.X("Date", sort=None),y="Total guest",)
        st.altair_chart(chart, use_container_width=True, theme="streamlit")
        
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
        st.write("📨 :blue[hms@gmail.com]")
        
    st.divider()
    image_map = Image.open('assets\map.png')
    st.image(image_map)