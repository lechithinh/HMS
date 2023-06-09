import streamlit as st
import time

def Inventory(mydb):
    tab1, tab2 = st.tabs(["**View inventory**", "**Add an item**"])
    with tab1:
        inventory_data = mydb.get_inventory_table()
        
        table_inventory = st.experimental_data_editor(inventory_data ,use_container_width= True)


    with tab2:
            st.markdown('''
            <h3 style='text-align: center;  color: black;'>Add a new item</h3>
            ''', unsafe_allow_html=True)
            
            with st.form("Add a new item"):
                isProductadded = False              
                with st.container():
                    item_name = st.selectbox("Product Name", table_inventory['item_name'])
                    col1, col2 = st.columns(2)
                    with col1:
                        total = st.slider('Total', 0, 150, 0)
                    with col2:
                        price = st.number_input("Price per item", 5000, step= 500)
                        _, _, _, _, _, col6 = st.columns(6)
                        with col6:
                            add_item = st.form_submit_button("Add", type = "primary")
                            if add_item:
                                isProductadded = mydb.add_inventory(item_name,total,price)
                    if isProductadded:
                        st.success("You have added a new product")
                        time.sleep(2)
                        st.experimental_rerun()
                        
                    