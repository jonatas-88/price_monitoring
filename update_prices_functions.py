import os
import sys
import database_functions as dbf
import webscraping_functions as wsf
import configparser

config_file_name = 'price_monitoring.config'
#cwd = os.path.dirname(sys.argv[0]) #working on linux server or windows python script
cwd = os.getcwd() #working on windows during python notebook execution
cfg = configparser.ConfigParser()
ini_config_path = os.path.join(cwd,config_file_name)
cfg.read(ini_config_path)
database = cfg['database_config']['database']
link_prefix = cfg['general_config']['link_prefix']
link_sufix = cfg['general_config']['link_sufix']

#FUNCTION TO READ ALL TABLES FROM SQLITE.DB AND TABLE NAME STARTS WITH "USER"
def read_all_tables(database):
    #read all tables from sqlite.db
    tables = dbf.read_all_tables(database)
    #filter tables with user id
    tables = [table[0] for table in tables if table[0].startswith('user')]
    return tables

#FUNCTION TO READ ALL PRODUCT ID FROM ALL TABLES
def read_all_product_id(database):
    tables = read_all_tables(database)
    product_id_list = []
    for table in tables:
        conn, cur = dbf.connect_to_database(database)
        query = "SELECT product_id FROM {}".format(table)
        data = dbf.select_data(conn, cur, query)
        dbf.close_connection(conn)
        product_id_list += [row[0] for row in data]
    product_id_list = list(set(product_id_list))
    return product_id_list

#FUNCTION TO GENERATE URL LIST FROM PRODUCT ID
def generate_url_list(product_id_list):
    url_list = [link_prefix + str(product_id) + link_sufix for product_id in product_id_list]
    return url_list

#FUNCTION TO REGISTER PRICES FROM URL LIST
def register_price_from_url_list(url_list):
    result_list = []
    price_list = []
    for url in url_list:
        product_data, product_dict = wsf.get_product_info(url)
        price_list.append(product_dict)
        result = wsf.register_price_into_db(product_data)
        # if result:
        #     print('Price registered into database')
        # else:
        #     print('Price not registered into database for item: ' + url)
        result_list.append(result)
    return result_list, price_list

#MAIN FUNCTION TO UPDATE ALL PRICES LISTED INTO DATABASE
def update_db_prices():
    product_id_list = read_all_product_id(database)
    url_list = generate_url_list(product_id_list)
    result_list, price_list = register_price_from_url_list(url_list)
    return result_list, price_list
