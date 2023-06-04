import streamlit as st


def Inventory():
    tab1, tab2 = st.tabs(["**View inventory**", "**Add an item**"])
    with tab1:
        seeding_inventory = {'Update': [False, False,  False],
                            'Product Name': ["Bottle of water", "Bottle of coca", "Bottle of pessi"], 
                            'Total': [60, 30, 20], 
                            'Price per each': [5, 10, 10], 
                            'Remaining': [30, 25, 10]}
                        
        
        table_inventory = st.experimental_data_editor(seeding_inventory ,use_container_width= True)

    with tab2:
            st.markdown('''
            <h3 style='text-align: center;  color: black;'>Add a new item</h3>
            ''', unsafe_allow_html=True)
            
            with st.form("Add a new item"):              
                with st.container():
                    item_name = st.selectbox("Product Name", seeding_inventory['Product Name'])
                    col1, col2 = st.columns(2)
                    with col1:
                        total = st.slider('Total', 0, 150, 25)
                    with col2:
                        price = st.number_input("Price per item", 5000)
                        _, _, _, _, _, col6 = st.columns(6)
                        with col6:
                            add_item = st.form_submit_button("Add", type = "primary")
                            if add_item:
                                pass
    