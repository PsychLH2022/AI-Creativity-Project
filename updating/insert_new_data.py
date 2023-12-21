import mysql.connector
from mysql.connector import Error
import pandas as pd

def updata_base(df):
    # connect to database
    try:
        connection = mysql.connector.connect(host='dbnewyorkcartoon.cgyqzvdc98df.us-east-2.rds.amazonaws.com',
                                             database='new_york_cartoon',
                                             user='dbuser',
                                             password='Sql123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You succeed to connect to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    # insert new data into 'base' table
    contests = list(range(df['contest_num'].min(), df['contest_num'].max()+1))
    for contest in contests:
        num_caption = int(df.loc[df['contest_num'] == contest, 'num_caption'].values[0])
        num_resp = int(df.loc[df['contest_num'] == contest, 'num_resp'].values[0])
        image_url = df.loc[df['contest_num'] == contest, 'image_url'].values[0]
        contest = int(contest)
        sql = "INSERT INTO base (contest_num, num_caption, num_resp, image_url) VALUES (%s, %s, %s, %s)"
        val = (contest, num_caption, num_resp, image_url)
        cursor.execute(sql, val)
        connection.commit()
    
    print("You succeed to insert new data into 'base' table.")

    # close database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")



def updata_result(df):
    # connect to database
    try:
        connection = mysql.connector.connect(host='dbnewyorkcartoon.cgyqzvdc98df.us-east-2.rds.amazonaws.com',
                                             database='new_york_cartoon',
                                             user='dbuser',
                                             password='Sql123456',
                                             charset='utf8mb4')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You succeed to connect to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    # insert new data into 'result' table
    num_records = len(df.index)
    for i in range(num_records):
        contest = int(df.loc[i, 'contest_num'])
        caption = df.loc[i, 'caption']
        ranking = int(df.loc[i, 'ranking'])
        mean = float(df.loc[i, 'mean'])
        prec = float(df.loc[i, 'precision'])
        votes = int(df.loc[i, 'votes'])
        not_funny = int(df.loc[i, 'not_funny'])
        somewhat_funny = int(df.loc[i, 'somewhat_funny'])
        funny = int(df.loc[i, 'funny'])
        sql = "INSERT INTO result (contest_num, caption, ranking, mean, prec, votes, not_funny, somewhat_funny, funny) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (contest, caption, ranking, mean, prec, votes, not_funny, somewhat_funny, funny)
        cursor.execute(sql, val)
        connection.commit()

    print("You succeed to insert new data into 'result' table.")

    # close database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")