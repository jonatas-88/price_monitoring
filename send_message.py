import os
import sys
import requests
from time import sleep
import database_functions as dbf
import configparser

config_file_name = 'price_monitoring.config'
#cwd = os.path.dirname(sys.argv[0]) #working on linux server or windows python script
cwd = os.getcwd() #working on windows during python notebook execution
cfg = configparser.ConfigParser()
ini_config_path = os.path.join(cwd,config_file_name)
cfg.read(ini_config_path)
bot_token = cfg['telegram_config']['bot_token']

token = bot_token

#FUNCTION TO RETURN A LIST FROM ALL PRODUCTS WITH PRICE LESS THAN TARGET PRICE FROM SPECIFIC USER
def verify_lower_prices(dbname, user_id):
    chat_id = str(user_id)
    df = dbf.get_data_table_from_user_db(dbname, user_id)
    df
    if df is None:
        return None
    #iterate all rows from dataframe
    lower_price_list = []
    for index, row in df.iterrows():
        #if price is lower than target price, send message to user
        if row['price'] <= row['target_price']:
            message = 'O produto ' + row['product_id'] + ' esta com o preco abaixo do alvo. \nPreco atual: ' + str(row['price']) + '\nPreco alvo: ' + str(row['target_price'])
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url)
            sleep(0.5)
            lower_price_list.append(row)
    if len(lower_price_list) > 0:
        return lower_price_list
    return None


def send_message_to_users(dbname):
    #LIST ALL TABLES FROM USERS
    tables = dbf.read_all_tables(dbname)
    #ITERATE ALL TABLES
    for table in tables:
        #GET USER ID FROM TABLE NAME
        table_name = table[0]
        if 'user_' in table_name:
            user_id = table_name.replace('user_', '')
            #VERIFY IF USER HAS PRODUCTS WITH PRICE LOWER THAN TARGET PRICE
            lower_price_list = verify_lower_prices(dbname, user_id)
            if lower_price_list is not None:
                print('User ID: ' + str(user_id) + ' has products with lower price than target price')
            else:
                print('User ID: ' + str(user_id) + ' has no products with lower price than target price')