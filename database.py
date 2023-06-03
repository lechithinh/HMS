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

def main():
    mydb = DataBase("localhost", "root", "root", "hms")
    data = mydb.Add_New_Staff("Le Chi T1233333", "0822043152", "lechithinh123@gmail.com", "13/04/2003", "Manager")
    
    


   
    

if __name__ == "__main__":
    main()