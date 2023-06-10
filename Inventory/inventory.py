import streamlit as st
import time
#Helpers
from global_helpers import DisplayTextCenter
from Inventory.inventory_helpers import check_duplicate_item
class Inventory_Module:
    def __init__(self, mydb):
        self.mydb = mydb
    def View_inventory_infor(self):
        inventory_data = self.mydb.get_inventory_table()
        self.table_inventory = st.data_editor(inventory_data ,use_container_width= True, hide_index=1, column_config={'item_id': None})

        count = 0
        for value in self.table_inventory['Update']:
            if value:
                count += 1
        if count > 1:
            st.error("**Please select a single record.!**", icon="🚨")
        else:
            for value in self.table_inventory['Update']:
                if value:
                    index = self.table_inventory['Update'].index(value)
                    item_id = self.table_inventory['item_id'][index]
                    item_name = self.table_inventory['item_name'][index]
                    with st.expander("", expanded=True):
                        st.subheader(f":blue[**ITEM ID**]: :blue[{self.table_inventory['item_id'][index]}]")
                        with st.form("Update item information"):
                            isUpdateSuccess = False
                            isRemove = False
                            with st.container():
                                row_1_1, row_1_2 = st.columns(2)
                                row_2_1, row_2_2 = st.columns(2)
                                with row_1_1:
                                    item_name = st.text_input(":blue[**Item name**]", f"{self.table_inventory['item_name'][index]}")
                                with row_1_2:
                                    item_price = st.text_input(":blue[**Item Price**]", f"{self.table_inventory['price'][index]}")
                                with row_2_1:
                                    item_total = st.text_input(":blue[**Total**]", f"{self.table_inventory['total'][index]}")
                                with row_2_2:
                                    item_remain = st.text_input(":blue[**Remain**]", f"{self.table_inventory['remain'][index]}")
                                col1_remove_item, _, col3_update_item = st.columns(3)
                                with col1_remove_item:
                                    remove_button = st.form_submit_button("**Remove**", type="primary")
                                    if remove_button:
                                        with st.spinner('Processing...'):
                                            time.sleep(2)
                                        isRemove = True
                                        isRemove = self.mydb.remove_item(item_id)
                                with col3_update_item:
                                    udpate_button = st.form_submit_button("**Update Item**", type="primary")
                                    if udpate_button:
                                        with st.spinner('Processing...'):
                                            time.sleep(2)
                                        
                                        #check if item is valid to add
                                        if item_name != "" and check_duplicate_item(item_name, self.table_inventory['item_name']) == True:
                                            isUpdateSuccess = self.mydb.update_item_inventory(item_id, item_name, int(item_price), int(item_total), int(item_remain))
                                        elif item_name == "":
                                            st.error("Item name must not be empty!")
                                        elif check_duplicate_item(item_name, self.table_inventory['item_name']) == False:
                                            st.error('The item is in stock!')
                            if isUpdateSuccess:
                                st.success("Item information has been updated")
                                time.sleep(2)
                                st.experimental_rerun()
                            if isRemove:
                                st.success("Remove item successful")
                                time.sleep(2)
                                st.experimental_rerun()
    def Add_an_item(self):
        
        DisplayTextCenter("Add a new item")
        with st.form("Add a new item"):
            isProductadded = False              
            with st.container():
              
                item_name = st.text_input(":blue[**Product Name**]",placeholder="Enter product name")
                col1, col2 = st.columns(2)
                with col1:
                    total = st.slider(':blue[**Number of products**]', 0, 150, 0)
                with col2:
                    price = st.number_input(":blue[**Price per item**]", 5000, step= 500)

                add_item = st.form_submit_button("Add an item", type = "primary")
                if add_item:
                    with st.spinner('Processing...'):
                        time.sleep(2)
                    
                    #check if item is valid to add
                    if item_name != "" and check_duplicate_item(item_name, self.table_inventory['item_name']):
                        isProductadded = self.mydb.add_inventory(item_name,total,price)
                    elif item_name == "":
                        st.error("Item name must not be empty!")
                    elif check_duplicate_item(item_name, self.table_inventory['item_name']) == False:
                        st.error('The item is in stock!')
                        
                            
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