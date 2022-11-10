from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium import webdriver
from datetime import datetime
from threading import Thread
from time import sleep
import numpy as np
from typing import Literal
import random
import sys
import os

global driver
path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(path),options=options,keep_alive=True)

URL = 'http://192.168.1.1'

USER = '1234'
PASSWORD = '1234'



def login(user,password):
    #USERNAME
    username_input = driver.find_element(By.XPATH,'//*[@id="orgusername"]')
    username_input.send_keys(user)
    #PASSWORD
    password_input = driver.find_element(By.XPATH,'//*[@id="orgpassword"]')
    password_input.send_keys(password)
    #LOGIN BUTTON
    login_button = driver.find_element(By.XPATH,'//*[@id="login_btn"]')
    login_button.click()
    

def get_network_info()->dict:
    '''IPv4 WAN Connection Status
    Returned dict's Keys: 'ConnectionName','Type','IPAddress','DefaultGateway','PrimaryDNS','SecondaryDNS','Status' '''
    #get the network info page
    driver.get(URL+'/page/status/status_wannetwork.shtml')
    #get data
    data_elements = driver.find_elements(By.XPATH,'//*[@id="4_table"]/tbody/tr[2]/td')
    data = [a.text for a in data_elements]
    keywords = ['ConnectionName','Type','IPAddress','DefaultGateway','PrimaryDNS','SecondaryDNS','Status']
    data_dict = {key:data[i] for i,key in enumerate(keywords)}
    
    driver.back()#go back to main menu
    
    return data_dict


def reboot():
    '''clicks the reboot button'''
    #get the reboot page
    driver.get(URL+'/page/management/mngt_reboot.shtml')
    
    #get reboot button
    reboot_button = driver.find_element(By.XPATH,'//*[@id="reboot"]')
    reboot_button.click()
    
    #TODO: Puede que al reiniciar se caiga selenium, no esta testeado
    
    driver.back()
    
    return True


    
    
    
    
def main():
    driver.get(URL)
    login(USER,PASSWORD)
    print(get_network_info())
    
    
if __name__ == '__main__':
    main()