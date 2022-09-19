import os
import sys
from datetime import datetime
from time import sleep
from selenium import webdriver
import configparser
import database_functions as dbf
import locale
import platform

#IMPORT CONFIG FROM FILE .CONFIG
config_file_name = 'price_monitoring.config'
#locale.setlocale(locale.LC_ALL, "ko_KR.UTF-8")
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
#cwd = os.path.dirname(sys.argv[0]) #working on linux server or windows python script
cwd = os.getcwd() #working on windows during python notebook execution
cfg = configparser.ConfigParser()
ini_config_path = os.path.join(cwd,config_file_name)
cfg.read(ini_config_path)

if platform.system() == "Linux":
    driver_path_chrome = cfg['general_config']['driver_path_chrome_linux']
else:
    driver_path_chrome = cfg['general_config']['driver_path_chrome']
    driver_path_edge = cfg['general_config']['driver_path_edge']
    driver = webdriver.Edge(driver_path_edge)

database = cfg['database_config']['database']
db_price_columns = cfg['database_config']['db_price_columns']
db_price_table_name = cfg['database_config']['db_price_table_name']
link_prefix = cfg['general_config']['link_prefix']
link_sufix = cfg['general_config']['link_sufix']
link_sufix_split = cfg['general_config']['link_sufix_split']

#FUNCTION TO GET PRICE FROM WEBPAGE
def get_price(driver):
    xpath_price = '/html/body/div[2]/section/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[1]/strong'
    price_content = driver.find_element("xpath", xpath_price).text
    try:
        price_content = price_content.replace('원', '')
    except:
        price_content = price_content
    price = locale.atof(price_content)
    return price

#FUNCTION TO GET PRICE FROM WEBPAGE
def get_image(driver):
    xpath_image = '/html/body/div[2]/section/div[1]/div/div[1]/div[1]/img'
    image_content = driver.find_element("xpath", xpath_image).get_attribute('src')
    return image_content

def get_driver():
    if platform.system() == "Linux":
        driver = webdriver.Chrome(driver_path_chrome)
    else:
        driver = webdriver.Edge(driver_path_edge)
    return driver

#FUNCTION TO GET PRODUCT INFO FROM URL
def get_product_info(url):
    driver = get_driver()
    try:
        driver.get(url)
        sleep(0.5)
        price = get_price(driver)
        time_utc_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        image_link = get_image(driver)
        #link = url
        product_id = url.split(link_prefix)[1].split(link_sufix_split)[0]
        product_link = link_prefix + product_id + link_sufix
        product_data = str(price) + ",'" + time_utc_now + "','" + image_link + "','" + product_id + "','" + product_link + "'"
        product_dict = {
            'price': price,
            'time_utc_now': time_utc_now,
            'image_link': image_link,
            'product_id': product_id,
            'product_link': product_link
            }
    except:
        return None, None
    driver.quit()
    sleep(1)
    return product_data, product_dict

#FUNCTION TO REGISTER PRICE INTO DATABASE
def register_price_into_db(product_data):
    try:
        conn, cur = dbf.connect_to_database(database)
        dbf.create_table(conn, cur, db_price_table_name, db_price_columns)
        query = "INSERT INTO {} VALUES ({})".format(db_price_table_name, product_data)
        dbf.execute_query(conn, cur, query)
        dbf.close_connection(conn)
    except:
        return False
    return True
