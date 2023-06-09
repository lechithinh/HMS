
import streamlit as st
def display_table_staff(staff_table):
       table_new = {
              "Update": [],
              'Name': [],
              'Phone': [],
              'Address': [],
              "Date Of Birth": [],
              "Role": [],
              "Username": []
       }
       table_new["Update"] = staff_table['Update']
       table_new["Name"] = staff_table['Name']
       table_new["Phone"] = staff_table['Phone']
       table_new["Address"] = staff_table['Address']
       table_new["Date Of Birth"] = staff_table['Date Of Birth']
       table_new["Role"] = staff_table['Role']
       table_new["Username"] = staff_table['Username']
       return table_new
def check_valid_phone(phone_number):
       if len(phone_number) == 10:
              if phone_number.isnumeric():
                     return True
              else:
                     return False
       else:
              return False
def check_user_name(my_username, lst_username):
       if my_username:
              for username in lst_username:
                     if my_username == username:
                            return False
              return True
       else:
              return False
def check_name_staff(username):
       if username:
              for item in username:
                     if item.isalpha() == False:
                            if item.isspace() == False:
                                   return False
              return True
       else:
              return False

