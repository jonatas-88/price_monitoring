#!/usr/bin/python
import sqlite3
import pandas as pd
from time import sleep

#CONNECTION TO DATABASE
def connect_to_database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur

#CREATE TABLE IF NOT EXISTS
def create_table(conn, cur, table_name, columns):
    cur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns))
    conn.commit()
    #print("Table {} created".format(table_name))
    return

#CLOSE CONNECTION
def close_connection(conn):
    conn.close()
    #print("Connection closed")
    return

#SELECT DATA FROM TABLE
def select_data(conn, cur, query):
    cur.execute(query)
    data = cur.fetchall()
    conn.commit()
    #print("Data selected")
    return data

#FUNCTION TO EXECUTE QUERY
def execute_query(conn, cur, query):
    cur.execute(query)
    conn.commit()
    #print("Query executed")
    return

#READ ALL TABLES
def read_all_tables(dbname):
    conn, cur = connect_to_database(dbname)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    conn.commit()
    #print("Tables read")
    return tables

## SQL MANAGING FUNCTIONS
# FUNCTION TO RETRIEVE DATA FROM SQLITE DATABASE
def get_data_from_user_db(dbname, user_id):
    conn, cur = connect_to_database(dbname)
    query = "SELECT * FROM user_" + str(user_id)
    data = select_data(conn, cur, query)
    title = [description[0] for description in cur.description]
    conn.close()
    return data, title

#FUNCTION TO RETURN DATAFRAME WITH USER DB AND PRICES RELATED
def get_data_table_from_user_db(dbname, user_id):
    try:
        conn, cur = connect_to_database(dbname)
        #GET DATA FROM USER DB
        query_user = "SELECT * FROM user_" + str(user_id)
        #GET DATA FROM PRICES TABLE
        query_ordered = "SELECT product_id, price, time_utc_now, image_link FROM prices ORDER BY time_utc_now DESC"
        query_last_info = f"SELECT min(product_id) AS product_id, price, time_utc_now, image_link FROM ({query_ordered}) GROUP BY product_id"
        #JOIN TABLES
        query_join = f"SELECT p.*, s.price, s.time_utc_now, s.image_link FROM ({query_user}) p LEFT JOIN ({query_last_info}) s ON p.product_id=s.product_id"
        #EXECUTE QUERY AND GENERATE DATAFRAME
        data = select_data(conn, cur, query_join)
        title = [description[0] for description in cur.description]
        conn.close()
        df = pd.DataFrame(data, columns=title)
    except:
        return None
    return df

#FUNCTION TO READ ALL PRODUCT ID FROM SPECIFIC USER TABLE
def read_all_product_id_from_user(dbname, user_id):
    conn, cur = connect_to_database(dbname)
    query = "SELECT product_id FROM user_" + str(user_id)
    data = select_data(conn, cur, query)
    close_connection(conn)
    product_id_list = [str(row[0]) for row in data]
    return product_id_list

#CONNECT TO DATABASE AND CREATE TABLE IF IT DOESN'T EXIST
def update_database(dbname, product_id, user, product_link, target_price):
    try:
        conn, cur = connect_to_database(dbname)
        columns = "product_id TEXT PRIMARY KEY, user TEXT, product_link TEXT, target_price REAL"
        table_name = "user_" + str(user)
        create_table(conn, cur, table_name, columns)
        sleep(0.5)
        data = "'" + str(product_id) + "','" + str(user) + "','" + product_link + "','" + str(target_price) + "'"
        query = "INSERT INTO {} VALUES ({})".format(table_name, data)
        execute_query(conn, cur, query)
        sleep(0.5)
    except:
        pass
    close_connection(conn)

#FUNCTION TO UPDATE PRICE IN DATABASE
def update_price_database(dbname, product_id, user, target_price):
    try:
        conn, cur = connect_to_database(dbname)
        table_name = "user_" + str(user)
        query = "UPDATE " + table_name + " SET target_price = '" + str(target_price) + "' WHERE product_id = '" + str(product_id) + "'"
        #print(query)
        execute_query(conn, cur, query)
        sleep(0.5)
    except:
        pass
    close_connection(conn)

#FUNCTION TO DELETE PRODUCT FROM DATABASE
def delete_product_database(dbname, product_id, user):
    try:
        conn, cur = connect_to_database(dbname)
        table_name = "user_" + str(user)
        query = "DELETE FROM " + table_name + " WHERE product_id = '" + str(product_id) + "'"
        #print(query)
        execute_query(conn, cur, query)
        sleep(0.5)
    except:
        pass
    close_connection(conn)