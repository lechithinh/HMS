import streamlit as st
def check_duplicate_item(item_name, lst_item):
    for item in lst_item:
        if item == item_name:
            return False
    return True


