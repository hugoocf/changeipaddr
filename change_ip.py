from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from threading import Thread
from time import sleep
import requests
import os



global driver

path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(path),options=options)

URL = 'http://192.168.1.1'

USER = '1234'
PASSWORD = '1234'


class NoConnection(Exception):...


def wait_until_connection():
    def is_connected():
        try:
            requests.get('google.com')
            print('Connected')
            return True
        
        except Exception:
            print('Waiting for connection')
            return True 
    
    while not is_connected:
        sleep(15)
    return True
        
    




def on_thread(_func=None,*,reps=1,loop=False,timeout=600):
    global l
    l = loop
    def decorator(func):
        def wrapper(*args, **kwargs):
            if l:
                def loop(*args,**kwargs):
                    while True:
                        func(*args, **kwargs)
                        sleep(timeout)
            else:
                def loop(*args,**kwargs):
                    for _ in range(reps):
                        func(*args, **kwargs)
                        sleep(timeout)
                        
            t = Thread(target=loop,args=args,kwargs=kwargs)
                
            t.start()
            
            return 0
        return wrapper
    
    if _func is None:
        return decorator
    else:
        return decorator(_func)
            
    

def login(user,password):
    '''Log In '''
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
    Returned a dict (keys: 'ConnectionName', 'Type', 'IPAddress', 'DefaultGateway', 'PrimaryDNS', 'SecondaryDNS', 'Status') '''
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
    '''Reboot'''
    #get the reboot page - it reboots automatically
    driver.get(URL+'/page/management/mngt_restart.shtml')
    wait_until_connection()
    driver.refresh()
    login(USER,PASSWORD)
    


def main():
    driver.get(URL)
    login(USER,PASSWORD)
    print(get_network_info()['IPAddress'])



@on_thread(loop=True,timeout=60*15)
def subrutine():
    print('Rebooting',end='... ')
    reboot()
    new_ip = get_network_info()['IPAdress']
    if new_ip:
        print('Success')
        print('New ip:',new_ip)
    
    else:
        print('Failed')
    
    
    
    
if __name__ == '__main__':
    main()
    subrutine()
