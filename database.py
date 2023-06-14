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
        
    def get_staff_id(self, username):
        query = "SELECT staff_id FROM staff WHERE username = %s"
        self.Cursor.execute(query, (username, ))
        data = self.Cursor.fetchone()
        return data[0]

    def get_staff_role(self, staff_id):
        query = "SELECT role FROM staff WHERE staff_id = %s"
        self.Cursor.execute(query, (staff_id, ))
        data = self.Cursor.fetchone()
        return data[0]

    def get_staff_status(self, staff_id):
        query = f"SELECT `status` FROM staff WHERE staff_id = {staff_id}"
        self.Cursor.execute(query)
        data = self.Cursor.fetchone()
        return data[0]
    
    def get_staff_login(self):
        query = "SELECT staff_name, username, password FROM staff where `status` = 'Active'"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()

        staff_login = {
            "staff_name": [],
            "username": [],
            "password": []
        }
        for item in data:
            staff_login['staff_name'].append(item[0])
            staff_login['username'].append(item[1])
            staff_login["password"].append(item[2])
        return staff_login
    
    def get_a_staff(self, staff_id):
        query = f"SELECT staff_name, phone_number,address,date_of_birth,username,role FROM staff WHERE staff_id = {staff_id}"
        self.Cursor.execute(query)
        data = self.Cursor.fetchone()
        return data
    
    def get_staff_table(self, staff_id):
        # query = "SELECT * FROM staff WHERE isActive = 'TRUE'"
        query = "SELECT * FROM staff"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        staff_data = {
            "Update": [],
            "Staff ID": [],
            'Name': [],
            'Phone': [],
            'Address': [],
            "Date Of Birth": [],
            "Role": [],
            "Username": [],
            "Status" : [],
            "Suspend at": []
            }

        for item in data:
            if item[0] != staff_id: 
                staff_data["Update"].append(False)
                staff_data["Staff ID"].append(item[0])
                staff_data["Name"].append(item[1])
                staff_data["Phone"].append(str(item[2]))
                staff_data["Address"].append(item[4])
                staff_data["Date Of Birth"].append(item[5])
                staff_data["Role"].append(item[6])
                staff_data["Username"].append(item[3])
                staff_data["Status"].append(item[8])
                staff_data["Suspend at"].append(item[10])
        return staff_data
    
    def get_all_staff_username(self):
        query = "SELECT username FROM staff"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
        staff_username = []
        for item in data:
            staff_username.append(item[0])
        return staff_username
    
    def Update_One_Staff(self, Name, Phone, Address, DateOfBirth, Username, Role, staff_id):
        query = "UPDATE staff SET staff_name = %s, phone_number = %s, address = %s, date_of_birth = %s, username = %s, role = %s WHERE staff_id = %s"
        try:
            self.Cursor.execute(query, (Name, Phone, Address, DateOfBirth, Username, Role,staff_id))

            self.mydb.commit()
            return True
        except:
            return False
    def Update_Profile_Staff(self, Name, Phone, Address, DateOfBirth, Username, Role, password, staff_id):
        query = "UPDATE staff SET staff_name = %s, phone_number = %s, address = %s, date_of_birth = %s, username = %s, role = %s, password = %s WHERE staff_id = %s"
        try:
            self.Cursor.execute(query, (Name, Phone, Address, DateOfBirth, Username, Role, password, staff_id))

            self.mydb.commit()
            return True
        except:
            return False

    def Add_New_Staff(self, Name, Phone, username, password, DateOfBirth, Role, address):
        query = "INSERT INTO staff (staff_name,phone_number, username, password,date_of_birth, role, address) VALUES (%s, %s, %s, %s, %s,%s,%s) " 
        try: 
            self.Cursor.execute(query, (Name, Phone,username, password, DateOfBirth, Role, address))
            self.mydb.commit()
            return True
        except:
            return False
        
    def Hide_staff(self, staff_id):
        # query = f"UPDATE staff SET isActive = 'FALSE' where staff_id = {staff_id}"
        query = f"UPDATE staff SET `status` = 'Suspend', suspend_at = current_timestamp() where staff_id = {staff_id}"
        try:
            self.Cursor.execute(query)
            self.mydb.commit()
            return True
        except:
            return False
        
    def Update_suspended_staff(self, staff_id):
        query = f"UPDATE staff SET `status` = 'Active', suspend_at = null where staff_id = {staff_id}"
        try:
            self.Cursor.execute(query)
            self.mydb.commit()
            return True
        except:
            return False
        
    def get_suspend_staff(self):
        query = "SELECT username FROM staff WHERE `status` = 'Suspend'"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
        suspend_staff = []
        for item in data:
            suspend_staff.append(item[0])
        
        return suspend_staff
    
    #CHECK-IN
    def get_room_table(self):
        query = "SELECT * FROM room ORDER BY floor ASC"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()

        query1 = """SELECT room_id, num_adult, num_child
                    FROM booking 
                    WHERE isClose = 'FALSE'
        """
        self.Cursor.execute(query1)
        data1 = self.Cursor.fetchall()

        #convert to dictionary
        table_data = {
            "View information": [],
            "Room ID": [],
            "Room Name": [],
            "Num. adult": [],
            "Num. child": [],
            # "Num. Guest": [],
            'Floor': [],
            "Room type": [],
            'Room price': [],
            "Room beds": [],
            "Max people": [],
            "Status": [],
            "is Active":[],
            "Created at":[],
            "Removed at":[]
            }

        for item in data:
            table_data["View information"].append(False)
            table_data["Room ID"].append(item[0])
            table_data["Room Name"].append(item[1])
            # table_data["Num. Guest"].append(0)
            table_data["Floor"].append(item[2])
            table_data["Room type"].append(str(item[3]))
            table_data["Room price"].append(item[4])
            table_data["Room beds"].append(item[5])
            table_data["Max people"].append(item[6])
            table_data["Status"].append(item[7])
            table_data["is Active"].append(item[8])
            table_data["Created at"].append(item[9])
            table_data["Removed at"].append(item[10])

            isExist = False
            for temp in data1:
                if temp[0] == item[0]:
                    table_data["Num. adult"].append(temp[1])
                    table_data["Num. child"].append(temp[2])
                    isExist = True
            if isExist == False:
                table_data["Num. adult"].append(0)
                table_data["Num. child"].append(0)
        return table_data
    
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

    def add_a_booking(self,room_id, checkin_date, checkout_date, num_adult, num_child, isClose = 'FALSE'):
        query = "INSERT INTO booking (room_id ,checkin_date, checkout_date,num_adult, num_child, isClose) values (%s,%s,%s,%s,%s,%s)"
        try:
            self.Cursor.execute(query,(room_id,checkin_date,checkout_date,num_adult, num_child,isClose))
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
        query_1 = f"SELECT booking_id FROM booking WHERE room_id = {room_id} and isClose = 'FALSE';"
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
        query = """UPDATE inventory 
                SET remain = remain - %s, updated_at = current_timestamp()
                WHERE item_name = %s"""
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
    
    def update_room(self,  room_name, floor, room_type, room_price, room_beds, max_people,room_id):
        query = """UPDATE room
            SET room_name = %s , floor = %s , room_type = %s , room_price = %s , room_beds  = %s , max_people  = %s
            WHERE room_id = %s
        """
        try: 
            self.Cursor.execute(query, (room_name, floor, room_type, room_price, room_beds, max_people,room_id))
            self.mydb.commit()
            return True
        except:
            return False
        
    def add_a_room(self, room_name, floor, room_type,room_price, room_beds, max_people):
    
        query = "INSERT INTO room(room_name, floor, room_type, room_price, room_beds, max_people, status) values (%s, %s, %s, %s, %s, %s, %s)"
        try:
            room_status = 'Available'
            self.Cursor.execute(query, (room_name, floor, room_type, room_price, room_beds, max_people, room_status))
            self.mydb.commit()
            return True
        except:
            return False

    def remove_a_room(self, room_id):
        query = f"UPDATE room SET isActive = 'FALSE', removed_at = current_timestamp() WHERE room_id = {room_id}"
        try:
            self.Cursor.execute(query)
            self.mydb.commit()
            return True
        except:
            return False
    
    def update_removed_room(self, room_id):
        query = f"UPDATE room SET `isActive` = 'TRUE', removed_at = null where room_id = {room_id}"
        try:
            self.Cursor.execute(query)
            self.mydb.commit()
            return True
        except:
            return False

    def get_inventory_table_in_room(self):
        query = "SELECT item_name, remain FROM inventory where isActive = 'TRUE' and remain > 0"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        inventory_data = {
            "item name": [],
            "remain":[]
            }

        for item in data:
                inventory_data["item name"].append(item[0])
                inventory_data["remain"].append(item[1])
        return inventory_data
    
    #CHECKOUT
    #Lấy thông tin khách
    def get_guest_table(self):
        query = "SELECT * FROM Guest"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()

        guest_data = {
            "guest_id": [],
            "update": [],
            "guest_name": [],
            "phone_number": [],
            "address": [],
            "date_of_birth": [],
            "created_at": [],
            "modified_at": []
        }
        # print(data)
        for item in data:
            guest_data['guest_id'].append(item[0])
            guest_data["update"].append(False)
            guest_data["guest_name"].append(item[1])
            guest_data["phone_number"].append(str(item[2]))
            guest_data["address"].append(item[3])
            guest_data["date_of_birth"].append(item[4])
            guest_data["created_at"].append(item[5])
            guest_data["modified_at"].append(item[6])
        return guest_data
    #Lấy lượng order
    def get_order_amount(self, booking_id, item_name):
        # query = """select amount
        #             from `order` join `inventory`
        #             on `order`.item_id = inventory.item_id join booking 
        #             on booking.booking_id = `order`.booking_id
        #             where room_id = %s and isClose = 'FALSE' and item_name = %s"""
        query = "SELECT amount FROM `order` inner join inventory on `order`.item_id = inventory.item_id WHERE booking_id = %s and item_name = %s"
        try:
            self.Cursor.execute(query, (booking_id, item_name))
            data = self.Cursor.fetchone()
            return data[0]
        except:
            return 0
        
    def get_order_of_room(self, booking_id):
        query = f"SELECT item_name, amount FROM `order` inner join inventory on `order`.item_id = inventory.item_id WHERE booking_id = {booking_id}"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        order_data = {
            "item name": [],
            "order amount":[]
            }

        for item in data:
                order_data["item name"].append(item[0])
                order_data["order amount"].append(item[1])
        return order_data
    
    #Lấy thông tin khách hàng trong một room chỉ định
    def get_guest_of_room(self, id, close='FALSE'):
        query = """select guest.guest_id, guest_name, phone_number, address, date_of_birth, created_at, modified_at
    from (
	    select * 
	    from booking 
	    where room_id = %s and isClose = %s ) table1
            inner join booking_guest
            on table1.booking_id = booking_guest.booking_id
            inner join guest
            on booking_guest.guest_id = guest.guest_id;"""
        self.Cursor.execute(query, (id, close))
        data = self.Cursor.fetchall()
        guest_data = {
            "guest_id": [],
            "update": [],
            "guest_name": [],
            "phone_number": [],
            "address": [],
            "date_of_birth": [],
            "created_at": [],
            "modified_at": []
        }
     
        for item in data:
            guest_data['guest_id'].append(item[0])
            guest_data["update"].append(False)
            guest_data["guest_name"].append(item[1])
            guest_data["phone_number"].append(item[2])
            guest_data["address"].append(item[3])
            guest_data["date_of_birth"].append(item[4])
            guest_data["created_at"].append(item[5])
            guest_data["modified_at"].append(item[6])
        return guest_data
    #checkout
    def Update_room_status(self, id):
        query = """UPDATE Room
        SET status = 'Available'
        WHERE room_id = %s"""
        try:
            self.Cursor.execute(query, (id,))
            self.mydb.commit()
            return True
        except:
            return False
    def Update_isClose_booking(self, id):
        query = """UPDATE booking
                    SET isClose = 'TRUE'
                    WHERE room_id = %s AND isClose = 'FALSE'; """
        try:
            self.Cursor.execute(query, (id,))
            self.mydb.commit()
            return True
        except:
            return False
    def finalize_a_bill(self, booking_id):
        # query = """SELECT checkin_date, checkout_date, room_type, room_beds, room_price, total_price, TIMESTAMPDIFF(Day,checkin_date,checkout_date) as remainday,  TIMESTAMPDIFF(Day,checkin_date,checkout_date) * room_price + total_price as bill_price
        #         FROM (SELECT booking_id, room.room_id, checkin_date, checkout_date, room_type, room_beds, room_price
	    #         FROM booking inner join room
	    #         on booking.room_id = room.room_id
	    #         WHERE booking_id = %s) as table1
        #         inner join 
	    #         (SELECT booking_id, sum(total_price) as total_price
        #         FROM `order`
        #         WHERE booking_id = %s ) as table2
        #         ON table1.booking_id = table2.booking_id;"""        
        query1 = f"""SELECT sum(total_price) as order_price
                    FROM `order`
                    WHERE booking_id = {booking_id}
        """

        query2= f"""SELECT DATEDIFF(DATE(checkout_date), DATE(checkin_date)) * room_price as room_price
                    FROM booking inner join room
                    ON booking.room_id = room.room_id
                    WHERE booking_id = {booking_id}"""
        
        # query2 = f"""SELECT TIMESTAMPDIFF(Day,checkin_date,checkout_date) * room_price as room_price
        #             FROM booking inner join room
        #             ON booking.room_id = room.room_id
        #             WHERE booking_id = {booking_id}
        # """
        query3 =  f"SELECT checkin_date, checkout_date, room_type, room_beds,DATEDIFF(DATE(checkout_date), DATE(checkin_date))  FROM booking inner join room on booking.room_id = room.room_id WHERE booking_id = {booking_id}"


        self.Cursor.execute(query1)
        order_price = self.Cursor.fetchone()
        self.Cursor.execute(query2)
        room_price = self.Cursor.fetchone()
        

        self.Cursor.execute(query3)
        data3 = self.Cursor.fetchone()


        if order_price[0] == None:
            temp = 0
        else:
            temp = order_price[0]
        total_price = temp + room_price[0]
        table_bill = {
            "checkin_date": [],
            "checkout_date": [],
            "room_type": [],
            "room_beds": [],
            "room_price": [],
            "order_price": [],
            "day_remain": [],
            "bill_price": []
        }

        table_bill["checkin_date"].append(data3[0])
        table_bill["checkout_date"].append(data3[1])
        table_bill["room_type"].append(data3[2])
        table_bill["room_beds"].append(data3[3])
        table_bill["room_price"].append(room_price[0])
        table_bill["order_price"].append(temp)
        table_bill["day_remain"].append(data3[4])
        table_bill["bill_price"].append(total_price)
        return table_bill
    
    

    def update_guest_info(self, guest_id,  guest_name, phone, address, dob):
        query = f"UPDATE guest SET guest_name = '{guest_name}', phone_number = '{phone}', address = '{address}', date_of_birth='{dob}'WHERE guest_id = {guest_id}"
        try:
            self.Cursor.execute(
                query)
            self.mydb.commit()
            return True
        except:
            return False
    def update_order(self, booking_id, item_name, amount):
        query_1 = f"SELECT item_id, price FROM inventory Where item_name = '{item_name}'"
        self.Cursor.execute(query_1)
        item = self.Cursor.fetchone()
        item_id, item_price = item

        query = """INSERT INTO `order`(booking_id, item_id, amount, total_price)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    amount = %s,
                    total_price = %s * %s
        """
        try:
            total_price_insert = item_price * amount
            self.Cursor.execute(query, (booking_id, item_id, amount, total_price_insert , amount, item_price, amount))
            self.mydb.commit()
            return True
        except:
            return False
    #BILL
    def add_bill(self,booking_id, room_id, staff_id, total_price):
        query = "INSERT INTO bill (booking_id, room_id,staff_id,total_price) values (%s,%s,%s, %s)"
        try:
            self.Cursor.execute(query, (booking_id, room_id, staff_id, total_price))
            self.mydb.commit()
            return True
        except:
            return False

    #inventory
    def get_inventory_table(self):
        query = "SELECT * FROM inventory where isActive = 'TRUE'"
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()
    
        #convert to dictionary
        inventory_data = {
            "item_id": [],
            "Update":[],
            "item_name": [],
            'price': [],
            'total': [],
            'remain': [],
            "updated_at": []
            }

        for item in data:
                inventory_data["item_id"].append(item[0])
                inventory_data["Update"].append(False)
                inventory_data["item_name"].append(item[1])
                inventory_data["price"].append(item[2])
                inventory_data["total"].append(str(item[3]))
                inventory_data["remain"].append(item[4])
                inventory_data["updated_at"].append(item[7])
        return inventory_data
    
    def add_inventory(self,item_name, amount, price):
        #query = "UPDATE inventory SET total = total + %s , remain = remain + %s , price = %s WHERE item_name = %s"
        query = """INSERT INTO `inventory`(item_name, price , total, remain)
                    VALUES (%s,%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    price = %s,
                    total = %s,
                    remain = %s,
                    created_at = current_timestamp(),
                    updated_at = current_timestamp(),
                    isActive = 'TRUE'"""
        try:
            self.Cursor.execute(query, (item_name,price,amount,amount, price, amount, amount))
            self.mydb.commit()
            return True
        except:
            return False
    
    #edit profile
    def get_infor_staff(self, staff_id):
        query = f"SELECT * FROM staff WHERE staff_id = {staff_id}"
        self.Cursor.execute(query)
        data = self.Cursor.fetchone()
        return data[0]
    def update_item_inventory(self, item_id, item_name, item_price, total, remain):
        query = """update inventory
                   set item_name = %s, price = %s, total = %s, remain = %s, created_at = current_timestamp()
                   where item_id = %s"""
        try:
            self.Cursor.execute(query, (item_name, item_price, total, remain, item_id))
            self.mydb.commit()
            return True
        except:
            return False
    def remove_item(self, item_id):
        query = f"UPDATE inventory SET isActive = 'FALSE' WHERE item_id = {item_id}"
        try:
            self.Cursor.execute(query)
            self.mydb.commit()
            return True
        except:
            return False
    def get_table_bill(self):
        query = """select sum(total_price) as total, DATE(created_at) as date_only
                from bill
                group by date_only"""
        try:
            self.Cursor.execute(query)
            data = self.Cursor.fetchall()
            table_bill = {
                'total_price': [],
                'created_at': []
            }
            for item in data:
                table_bill["total_price"].append(int(item[0]))
                table_bill["created_at"].append(item[1])
            return table_bill
        except:
            return False
        
    #dashboard
    def guest_chart(self):
        query = """SELECT DATE(checkin_date) as checkin_date, count(guest_id)as num_guest
                    FROM booking inner join booking_guest
                    ON booking.booking_id = booking_guest.booking_id
                    GROUP BY DATE(checkin_date)
                    ORDER BY DATE(checkin_date) DESC
                    LIMIT 7;
        """
        self.Cursor.execute(query)
        data = self.Cursor.fetchall()

        guest_chart_table = {
            "check_in date": [],
            "num_guest":[]
            }

        for item in data:
                guest_chart_table["check_in date"].append(item[0])
                guest_chart_table["num_guest"].append(item[1])
        
        return guest_chart_table
    
    
def main():
    mydb = DataBase("127.0.0.1", "root", "uynnibeo2104", "hms")
    
    
    
    #data = mydb.Add_New_Staff("Le Chi T1233333", "0822043152", "lechithinh123@gmail.com", "13/04/2003", "Manager")
    #data = mydb.insert_order(1,"water",2)
    #data = mydb.get_booking_id(2)
    #data = mydb.get_remain_item("water")
    #mydb.update_inventory("water",8)
    #mydb.get_remain_item()
    # mydb.update_room('Room2',	1,	'NORMAL'	,200,	1,	2,	'Available','TRUE',2)
    #mydb.add_bill(1, 1, 6, 1300)
    # mydb.get_a_staff(2)
    # mydb.Update_One_Staff(4,"nmt",21323,"bh","1999-04-04","nmtt","Staff")
    # print(mydb.get_order_amount(34, "water"))
    # print(mydb.get_booking_id(1))
    # print(mydb.add_a_guest("BINZ",'8888888888',"SONLA","2023-9-6
    # print(mydb.get_inventory_table_in_room())
    # print(mydb.get_order_of_room(9))
    # mydb.add_inventory("banana",50,200)
    # mydb.add_a_room("ROOM8",2,"NORMAL",2)
    # mydb.add_a_booking(2,"2023-01-01","2023-01-01",2,4,"FALSE")
    # mydb.get_room_table()
    # print(mydb.get_inventory_table())
    # data = mydb.get_table_bill()
    # print(data)
    # import streamlit_authenticator as stauth

    # hashed_password = stauth.Hasher(["M"]).generate()
    # print(hashed_password)
    # print(mydb.get_staff_table())
    # print(mydb.get_staff_status(11))
    # mydb.remove_a_room(3)
    # print(mydb.get_staff_login())
    # print(mydb.get_all_staff_username())
if __name__ == "__main__":
    main()