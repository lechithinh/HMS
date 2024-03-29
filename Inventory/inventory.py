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
        self.table_inventory = st.data_editor(inventory_data ,use_container_width= True, hide_index=1, column_config={'item_id': None,'item_name':'Item name',  'price':'Price', 'total':'Total' , 'remain':'Remain', 'updated_at':'Updated at'})

        count = 0
        for value in self.table_inventory['Update']:
            if value:
                count += 1
        if count > 1:
            st.error("**Please select a single record!**", icon="🚨")
        else:
            for value in self.table_inventory['Update']:
                if value:
                    index = self.table_inventory['Update'].index(value)
                    item_id = self.table_inventory['item_id'][index]
                    item_name = self.table_inventory['item_name'][index]
                    with st.expander("", expanded=True):
                        st.subheader(f"**ITEM NAME**: :blue[{self.table_inventory['item_name'][index]}]")
                        with st.form("Update item information"):
                            isUpdateSuccess = False
                            isRemove = False
                            with st.container():
                                row_1_1, row_1_2 = st.columns(2)
                                row_2_1, row_2_2 = st.columns(2)
                                with row_1_1:
                                    item_name = st.text_input(":blue[**Item name**]", f"{self.table_inventory['item_name'][index]}")
                                with row_1_2:
                                    item_price = st.number_input(":blue[**Price per item (VND)**]", step= 1000, value=self.table_inventory['price'][index])
                                with row_2_1:
                                    item_total = st.number_input(":blue[**Number of items**]", int(self.table_inventory['total'][index]), step= 1)
                                with row_2_2:
                                    item_remain = st.text_input(":blue[**Remain**]", self.table_inventory['remain'][index], disabled=True)

                                update_col,_,_,_,_,_,_,_,remove_col = st.columns(9)
                                with remove_col:
                                    remove_button = st.form_submit_button(":red[**Remove**]")
                                with update_col:
                                        udpate_button = st.form_submit_button("**Update**", type="primary")
                                if remove_button:
                                        with st.spinner('Processing...'):
                                            time.sleep(2)
                                        isRemove = True
                                        isRemove = self.mydb.remove_item(item_id)

                               
                                if udpate_button:
                                        with st.spinner('Processing...'):
                                            time.sleep(2)
                                        #check if item is valid to add
                                        if item_name == self.table_inventory['item_name'][index] and item_price == str(self.table_inventory['price'][index]) and item_remain == str(self.table_inventory['remain'][index]) and item_total == str(self.table_inventory['total'][index]):
                                            st.warning("You haven't done the update yet")
                                            time.sleep(2)
                                        elif item_name != "" and item_price != "" and item_remain != "" and item_total != "":
                                            isUpdateSuccess = self.mydb.update_item_inventory(item_id, item_name, int(item_price), int(item_total), int(item_remain))
                                        elif item_name == "" or item_price == "" or item_total == "" or item_remain == "":
                                            st.error("Item information must not be empty!")
                                                
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
                    price = st.number_input(":blue[**Price per item (VND)**]", 10000, step= 500)

                add_item = st.form_submit_button("Add an item", type = "primary")
                if add_item:
                    with st.spinner('Processing...'):
                        time.sleep(2)
                    
                    #check if item is valid to add
                    if item_name == "":
                        st.error("Item name must not be empty!")

                    if check_duplicate_item(item_name, self.table_inventory['item_name']) == False:
                        st.error('The item is in stock!')

                    if total == 0:
                        st.error("Number of the item must be > 0")    

                    if item_name != "" and check_duplicate_item(item_name, self.table_inventory['item_name']) and total != 0:
                        isProductadded = self.mydb.add_inventory(item_name,total,price)  

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