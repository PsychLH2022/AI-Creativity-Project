from mysql.connector import Error
import mysql.connector
import pandas as pd
import streamlit as st

# create a class for database connection
class DBConnection: 
    def __init__(self):
        pass

    def create_connection():
        try:
            connection = mysql.connector.connect(host='dbnewyorkcartoon.cgyqzvdc98df.us-east-2.rds.amazonaws.com',
                                                 database='new_york_cartoon',
                                                 user='dbuser',
                                                 password='Sql123456')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                return connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None

    def select(query):
        connection = DBConnection.create_connection()
        mycursor = connection.cursor()

        if connection:
            try:
                mycursor.execute(query)
                df = pd.DataFrame(mycursor.fetchall())
                return df
            except Error as e:
                print("Error in executing the query:", e)
            finally:
                connection.close()
        return None
    
    def insert(query, data):
        connection = DBConnection.create_connection()
        mycursor = connection.cursor()
        
        if connection:
            try:
                mycursor.execute(query, data)
                connection.commit()
                print("Record is inserted into table successfully")
            except Error as e:
                print("Error in executing the query:", e)
            finally:
                connection.close()
        return None
    
    # get the contest number from the database and return a list
    def contest_num_list():
        connection = DBConnection.create_connection()
        mycursor = connection.cursor()
        
        if connection:
            try:
                mycursor.execute("""SELECT contest_num FROM base Where image_url IS NOT NULL""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['contest_num'])
                return df['contest_num'].tolist()
            except Error as e:
                print("Error in executing the query:", e)
            finally:
                connection.close()
        return None
    
    # insert final caption into the 'final_caption' table
    def insert_final_caption(contest_num, final_caption, user_id, time):
        connection = DBConnection.create_connection()
        mycursor = connection.cursor()
        
        if connection:
            try:
                # check if there is already a record for the contest number and user id
                mycursor.execute(f"""SELECT * FROM final_caption WHERE contest_num={contest_num} and user_id={user_id}""")
                df = pd.DataFrame(mycursor.fetchall())
                if df.empty:
                    # if there is no record, insert the record
                    mycursor.execute(f"""INSERT INTO final_caption (contest_num, caption, user_id, time) VALUES (%s, %s, %s, %s)""", (contest_num, final_caption, user_id, time))
                    st.success(f"Your final caption for contest {contest_num} has been submitted!")
                else:
                    # if there is already a record, update the record using prepared statement
                    mycursor.execute(f"""UPDATE final_caption SET caption = %s, time = %s WHERE contest_num = %s and user_id = %s""", (final_caption, time, contest_num, user_id))
                    st.success(f"Your final caption for contest {contest_num} has been updated!")
                connection.commit()
            except Error as e:
                print("Error in executing the query:", e)
            finally:
                connection.close()
        return None