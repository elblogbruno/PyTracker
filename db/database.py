import sqlite3
from sqlite3 import Error
import os
#need to install sudo apt-get install libsqlite3-dev
import time
class EmailDatabase:

    def __init__(self):
        self.db_name = 'db/pytracker-tracking-db.db'
        self.conn = self.create_database()

    def create_database(self):
        """ create a database connection to a SQLite database """
        db_file = self.db_name
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            if os.path.isfile(db_file):
                conn.execute('''CREATE TABLE EMAILS
                        ([generated_id] INTEGER PRIMARY KEY,[sender] text, [receiver] text,[counter] integer,[tracking_code] integer)''')
            else:
                print("Database exists already")
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
        return conn
        
    def create_con(self):
        db_file = self.db_name
        return  sqlite3.connect(db_file)

    def get_data(self):
        try:
             con = self.create_con()
             cur = con.cursor()

             cur.execute("SELECT * FROM emails")

             rows = cur.fetchall()

             for row in rows:
                 print(row)
             
             return str(rows)
        except Error as e:
            print(e)

    

    def add_sample_data(self):
        print("Adding sample data")
        self.write_data('brunomoyaruiz@gmail.com','glassearproject@gmail.com','0',int(time.time()%99999))
        return "Adding sample data"

    #Writes data to csv, in case server is stopped when runned again it looks at this saved file.
    def write_data(self,sender, receiver, counter,tracking_code):
        try:
            query = "INSERT INTO EMAILS (sender, receiver, counter, tracking_code) " \
            "values (?,?,?,?)"

            args  = (sender,receiver,counter,tracking_code)
            print(query)
            print(args)
            self.execute_list_query(query,args)
            
        except Error as e:
            print("Error writing data: " + str(e))

    #Finds tracking_code on the csv file and updates the counter 
    def find_row_by_tracking_code(self,tracking_code,update=True):
        connection = self.create_con()
        cursor = connection.cursor()
        try:
            sql = "SELECT e.sender,e.receiver,e.counter,e.tracking_code FROM EMAILS e where e.tracking_code = ?"
            cursor.execute(sql,(tracking_code,))

            rows = cursor.fetchall()

            counter = list(rows[0])[2]
            counter = counter + 1
            print("Query select successful: " + str(counter))

            sql_update = "UPDATE emails SET counter = ? WHERE tracking_code = ?"

            cursor.execute(sql_update,(int(counter),int(tracking_code)))

            print("Query update successful: ")
            print(rows)
            connection.commit()

            if len(rows) > 0:
                row = list(rows[0])
                row[2] = counter
                return True,row
            else:
                return False,None

        except Error as err:
            print(f"Error queryng: '{err}'")
            return False,None
    
    def execute_list_query(self,sql, val):
        connection = self.create_con()
        cursor = connection.cursor()
        try:
            cursor.execute(sql, val)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error queryng: '{err}'")