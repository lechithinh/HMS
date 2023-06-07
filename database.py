import mysql.connector


class DataBase:
    
    def __init__(self, host, user, passwd, database):
        self.mydb = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database= database,
        connect_timeout=1000 ,
        )

        self.Cursor = self.mydb.cursor(buffered=True)
        self.Cursor.stored_results()
        
    def get_staff_table(self):
        query = "SELECT * FROM staff"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        staff_data = {
            "staff_id": [],
            "Update": [],
            'Name': [],
            'Phone': [],
            'Email': [],
            "Date Of Birth": [],
            "Role": []
            }

        for item in data:
                staff_data["staff_id"].append(item[0])
                staff_data["Update"].append(False)
                staff_data["Name"].append(item[2])
                staff_data["Phone"].append(str(item[3]))
                staff_data["Email"].append(item[4])
                staff_data["Date Of Birth"].append(item[5])
                staff_data["Role"].append(item[6])
        return staff_data
        

    
    def Update_One_Staff(self, staff_id, Name, Phone, Email, DateOfBirth, Role):
        query = "UPDATE staff SET Name = %s, Phone = %s, Email = %s, Date_Of_Birth = %s, Role = %s WHERE staff_id = %s"
        try:
            self.Cursor.execute(query, (Name, Phone, Email, DateOfBirth, Role, staff_id))
            self.mydb.commit()
            return True
        except:
            return False
        
    def Add_New_Staff(self, Name, Phone, Email, DateOfBirth, Role):
        query = "INSERT INTO staff (Name, Phone, Email, Date_Of_Birth, Role) VALUES (%s, %s, %s, %s, %s) " 
        try: 
            self.Cursor.execute(query, (Name, Phone, Email, DateOfBirth, Role))
            self.mydb.commit()
            return True
        except:
            return False

    def get_room_table(self):
        query = "SELECT * FROM room"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        table_data = {
            "View information": [],
            "Room ID": [],
            "Room Name": [],
            'Floor': [],
            "Room type": [],
            'Room price': [],
            "Room beds": [],
            "Max people": [],
            "Status": [],
            "is Active":[],
            "Created at":[]
            }

        for item in data:
                table_data["View information"].append(False)
                table_data["Room ID"].append(item[0])
                table_data["Room Name"].append(item[1])
                table_data["Floor"].append(item[2])
                table_data["Room type"].append(str(item[3]))
                table_data["Room price"].append(item[4])
                table_data["Room beds"].append(item[5])
                table_data["Max people"].append(item[6])
                table_data["Status"].append(item[7])
                table_data["is Active"].append(item[8])
                table_data["Created at"].append(item[9])
        return table_data
    
    # check-in
    def add_a_guest(self, first_guest_name,first_guest_phone,first_guest_address,first_guest_dob):
        query = "INSERT INTO Guest (guest_name, phone_number, address, date_of_birth) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE modified_at = current_timestamp()"
        try: 
            self.Cursor.execute(query, (first_guest_name,first_guest_phone,first_guest_address,first_guest_dob))
            self.mydb.commit()
            return True
        except:
            return False
        
    def check_in_room(self, room_id):
        query = f"UPDATE room SET `status` = 'Occupied' WHERE room_id = {room_id}"
        self.Cursor.execute(query)
        self.mydb.commit()

    def add_a_booking(self,room_id, checkin_date, checkout_date, isClose = False):
        query = "INSERT INTO booking (room_id ,checkin_date, checkout_date,isClose) values (%s,%s,%s,%s)"
        try:
            self.Cursor.execute(query,(room_id,checkin_date,checkout_date,isClose))
            self.mydb.commit()
            return True
        except:
            return False
    
    def get_guest_id(self, limit):
        query = f"SELECT guest_id FROM guest ORDER BY modified_at DESC LIMIT {limit}"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
        return [item[0] for item in data]

    def get_booking_id(self,room_id):
        query_1 = f"SELECT booking_id FROM booking WHERE room_id = {room_id} and isClose = FALSE;"
        self.Cursor.execute(query_1)
        booking_id = self.Cursor.fetchone()
        return booking_id[0]
    
    def add_a_booking_guest(self, booking_id, guest_id):
        query_2 = "INSERT INTO booking_guest values (%s,%s)"
        try:
            for item in guest_id:
                self.Cursor.execute(query_2,(booking_id, item))
                self.mydb.commit()
            return True
        except:
            return False
    
    def insert_order(self,booking_id, product, amount):
        # get item_id, price
        query_1 = f"SELECT item_id, price FROM inventory WHERE item_name = '{product}' "
        self.Cursor.execute(query_1)
        item = self.Cursor.fetchone()
        item_id, item_price = item

        query_2 = "INSERT INTO	`order` (booking_id,item_id,amount,total_price) values (%s,%s,%s,%s)"
        try:
            self.Cursor.execute(query_2,(booking_id,item_id,amount, amount* item_price))
            self.mydb.commit()
            return True
        except:
            return False
    
    def update_inventory(self,product, amount):
        query = "UPDATE inventory SET remain = remain - %s WHERE item_name = %s"
        try: 
            self.Cursor.execute(query, (amount,product))
            self.mydb.commit()
            return True
        except:
            return False
        
    def get_remain_item(self,product):
        query = f"SELECT remain FROM inventory WHERE item_name = '{product}'"
        self.Cursor.execute(query)
        data = self.Cursor.fetchone()
        return data[0]
    

    def update_room(self,  room_name, floor, room_type, room_price, room_beds, max_people, status, isActive,room_id):
        query = """UPDATE room
            SET room_name = %s , floor = %s , room_type = %s , room_price = %s , room_beds  = %s , max_people  = %s , `status` = %s , isActive = %s
            WHERE room_id = %s
        """
        try: 
            self.Cursor.execute(query, (room_name, floor, room_type, room_price, room_beds, max_people, status, isActive,room_id))
            self.mydb.commit()
            return True
        except:
            return False


def main():
    mydb = DataBase("127.0.0.1", "root", "uynnibeo2104", "HMS")
    
    #data = mydb.Add_New_Staff("Le Chi T1233333", "0822043152", "lechithinh123@gmail.com", "13/04/2003", "Manager")
    #data = mydb.insert_order(1,"water",2)
    #data = mydb.get_booking_id(2)
    #data = mydb.get_remain_item("water")
    #mydb.update_inventory("water",8)
    #mydb.get_remain_item()
    mydb.update_room('Room2',	1,	'NORMAL'	,200,	1,	2,	'Available','TRUE',2)
if __name__ == "__main__":
    main()