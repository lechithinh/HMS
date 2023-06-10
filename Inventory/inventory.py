import streamlit as st
import time
#Helpers
from global_helpers import DisplayTextCenter

class Inventory_Module:
    def __init__(self, mydb):
        self.mydb = mydb
    def View_inventory_infor(self):
        inventory_data = self.mydb.get_inventory_table()
        self.table_inventory = st.experimental_data_editor(inventory_data ,use_container_width= True)
    def Add_an_item(self):
        DisplayTextCenter("Add a new item")
        with st.form("Add a new item"):
            isProductadded = False              
            with st.container():
                # item_name = st.selectbox("Product Name", self.table_inventory['item_name'])
                item_name = st.text_input("Product Name",placeholder="Enter product name")
                col1, col2 = st.columns(2)
                with col1:
                    total = st.slider('Total', 0, 150, 0)
                with col2:
                    price = st.number_input("Price per item", 5000, step= 500)
                    _, _, _, col4 = st.columns(4)
                    with col4:
                        add_item = st.form_submit_button("Add", type = "primary")
                        if add_item:
                            isProductadded = self.mydb.add_inventory(item_name,total,price)
                            with st.spinner('Processing...'):
                                time.sleep(2)
                            
            if isProductadded:
                st.success("You have added a new product")
                time.sleep(1)
                st.experimental_rerun()
                    

def Inventory(mydb):
    View_inventory_infor, Add_an_item = st.tabs(["**View inventory**", "**Add an item**"])
    #Init instance
    Inventory_instance = Inventory_Module(mydb)
    with View_inventory_infor:
        Inventory_instance.View_inventory_infor()
    with Add_an_item:
        Inventory_instance.Add_an_item()