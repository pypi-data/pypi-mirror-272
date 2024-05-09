
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager            #for ChromeDriver installation
from webdriver_manager.firefox import GeckoDriverManager            #for ChromeDriver installation
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

import sys, json
import urllib.request

sys.path.append("..") # Adds higher directory to python modules path.

from config.config import *

from core import mssentinelapi as mde
from core import msgraphapi as msgraph
from core import multifactor as mfa
from helper import requestheader as helper


#import MSSentinelApi as mde
#import MSGraphAPI as msgraph
#import MSGraphApi as graphapi
#import RequestHeader as helper
#from PyLog import *
import logging
from loguru import logger

import time, os, re, pickle
from pathlib import Path

security_page = 'https://security.microsoft.com'
azuread_page = 'https://portal.azure.com/api/DelegationToken?feature.cacheextensionapp=true&feature.internalgraphapiversion=true&feature.tokencaching=true'
Endpoint_page = 'https://endpoint.microsoft.com/api/DelegationToken?feature.internalgraphapiversion=true&feature.tokencaching=true'

#dbgPrint = PyLog(__name__, level=logging.INFO, store=False, consolePrint=True)

logger.add(f"./logs/{__name__}.log",mode="w", backtrace=True, diagnose=True, level="DEBUG", filter="Login")
#logger.add(sys.stdout, backtrace=True, diagnose=True)
dbgPrint = logger
class Login(object):
    """description of class"""
    def __init__(self, email=None, organization="kwijp.onmicrosoft.com"):
        self.organization = organization
        if email != None:
            self.email = email   

    def delete_session(self):
        session_path = os.path.abspath(os.path.dirname(__file__)) + "\..\session"
        for p in Path(session_path).glob("*.pkl"):
            if p.name != "mdr.pkl":
                os.remove(p)

    def wait(self, driver, timeout, type, element):
        while True:
            try:
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((type, element)))
                break
            except TimeoutException:
                dbgPrint.warning("[-] Loading took too much time!!!")
        dbgPrint.debug("[+] Your webpage is ready...")

    def web_app(self, driver, web_app, email, organization):

        if driver.current_url == 'data:,':
            driver.get(web_app)
        else:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
            while(True):
                try:
                    driver.get(web_app)
                    break
                except:
                    driver.get(web_app)

        self.wait(driver, 20, By.XPATH, "//div[contains(text(),'Sign-in options')]")
        element = driver.find_element(By.XPATH, "//div[contains(text(),'Sign-in options')]")
        WebDriverWait(driver,20).until(EC.element_to_be_clickable(element)).click()
        self.wait(driver, 20, By.XPATH, "//div[@data-test-cred-id='organization']")
        element = driver.find_element(By.XPATH, "//div[@data-test-cred-id='organization']")
        WebDriverWait(driver,20).until(EC.element_to_be_clickable(element)).click()
        self.wait(driver, 20, By.ID, "searchOrganizationInput")
        driver.find_element(By.ID, "searchOrganizationInput").send_keys(organization)
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(3)

        if "login.microsoftonline.com" not in driver.current_url:
            return

        self.wait(driver, 20, By.NAME, 'loginfmt')
        driver.find_element(By.NAME, 'loginfmt').send_keys(email)
        driver.find_element(By.ID, 'idSIButton9').click()

        override = False
        one_time_code = ""

        while len(one_time_code) <= 8:
            try:
                one_time_code = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='idTxtBx_OTC_Password']"))).get_attribute("value")
            except:
                if "login.microsoftonline.com" not in driver.current_url:
                    dbgPrint.debug("[+] Button override")
                    override = True
                    break
            if len(one_time_code) == 8:
                element = driver.find_element(By.ID, "idSIButton9")
                WebDriverWait(driver,20).until(EC.element_to_be_clickable(element)).click()

    def create_driver(self):

        try:
#            service = ChromeService(ChromeDriverManager().install())
            service = FirefoxService(GeckoDriverManager().install())
        except ValueError:
            latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
            service = ChromeService(ChromeDriverManager(version=latest_chromedriver_version).install())
#        options = webdriver.ChromeOptions()
        options = webdriver.FirefoxOptions()
#        options.add_argument('--disable-logging')
#        options.add_experimental_option('excludeSwitches', ['enable-logging'])          #Disable logging of webdriver #Chrome
#        driver = webdriver.Chrome(service=service, options=options)                     #August 26, 2023
        options.binary_location = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        driver = webdriver.Firefox(service=service, options=options)                     #April 12, 2024
#        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="114.0.5735.90").install()), options=options)  #New update 8/15/2023 11:35:31 PM
        return driver

    def login(self):
        self.driver = self.create_driver()   
        dbgPrint.info("[+] Checking session...")

#        if not os.path.exists('./session/ms365.pkl'):
        dbgPrint.debug("[-] Session does not exists...")

        dbgPrint.info("[-] ./session/MS365Dheaders.pkl and ./session/MS365Dcookies.pkl does not exist")
        time.sleep(1)
        dbgPrint.debug("[+] Starting new session...")
        #options = webdriver.EdgeOptions()
        #driver = webdriver.Edge(options=options)
        dbgPrint.debug("[+] Logging in...")
        
        self.web_app(self.driver , security_page, self.email, self.organization)
#        self.web_app(driver , security_page, "kwijp.onmicrosoft.com", self.email)

        self.wait(self.driver, 20, By.XPATH, "//div[@class='ms-List-page']")

        time.sleep(10)             
        auth_header = helper.RequestHeader(self.driver, "api/v2/auth")
        auth_header.get_headers()
        cookie = auth_header.get_param("cookie")

        dbgPrint.debug("[+] Retrieving current cookie...\n")

        mde.MSSentinelApi(cookies=cookie).save_session()

#        self.web_app(self.driver , "https://intune.microsoft.com/#dashboard", self.email, self.organization)
        self.web_app(self.driver , "https://intune.microsoft.com/#home", self.email, self.organization)
#        self.wait(self.driver, 20, By.XPATH, "//div[@class='ext-FlexColumn']//div//div[@data-bind='pcControl: card']")
#        self.wait(self.driver, 20, By.XPATH, "//*[@id='_weave_e_40']")
        self.wait(self.driver, 20, By.XPATH, "//*[@name='Home.ReactView']")
        dbgPrint.info("Sleeping for 15s")

        time.sleep(20)

        http_rqst = helper.RequestHeader(self.driver, "api/DelegationToken")        #1/27/2023 5:00:48 PM 
        http_rqst.get_headers()
        cookie = http_rqst.get_param("cookie")

        json_data = json.loads(http_rqst.body)
#        delegation_token = json.loads(http_rqst.body)

#        http_rqst = helper.RequestHeader(self.driver, "oauth2/v2.0/token")
#        http_rqst.get_headers_special("scope", "email openid profile")
#        token = json.loads(http_rqst.response_body)["access_token"]

        msgraph.MSGraphApi(cookies=cookie, json=json_data, verify=False).save_session()

#        self.web_app(self.driver , "https://account.activedirectory.windowsazure.com/usermanagement/multifactorverification.aspx?", self.email, self.organization)

#        self.wait(self.driver, 20, By.ID, "UserListGrid_ActionBarContainer")

#        time.sleep(2)
#        http_rqst = helper.RequestHeader(self.driver, "/GenericGetAvailableFilters.ajax")         #1/27/2023 5:00:48 PM 
#        cookies = http_rqst.get_param("Cookie")
#        headers = dict(http_rqst.headers._headers)
#        page = mfa.MultiFactor(cookies=cookies, headers=headers)            

#        page.save_session()

#        self.driver.quit()

    def mfa_login(self, email):
        self.driver = self.create_driver()  
        self.web_app(self.driver , "https://account.activedirectory.windowsazure.com/usermanagement/multifactorverification.aspx?", email, self.organization)

        self.wait(self.driver, 20, By.ID, "UserListGrid_ActionBarContainer")
#            self.wait(driver, 20, By.XPATH, "//img[@boxtype='Image' and @title='Search']")

        time.sleep(2)
        http_rqst = helper.RequestHeader(self.driver, "/GenericGetAvailableFilters.ajax")         #1/27/2023 5:00:48 PM 
        cookies = http_rqst.get_param("Cookie")
        headers = dict(http_rqst.headers._headers)
        page = mfa.MultiFactor(cookies=cookies, headers=headers)            

        page.save_session()

    def msgraph_login(self, email):
        self.driver = self.create_driver()  
        self.web_app(self.driver , "https://endpoint.microsoft.com", email, self.organization)

        self.wait(self.driver, 20, By.XPATH, "//div[@class='ext-FlexColumn']//div//div[@data-bind='pcControl: card']")
#            self.wait(driver, 20, By.XPATH, "//img[@boxtype='Image' and @title='Search']")

        time.sleep(5)       
        http_rqst = helper.RequestHeader(self.driver, "api/DelegationToken")         #1/27/2023 5:00:48 PM 
        cookie = http_rqst.get_param("cookie")

        json_data = json.loads(http_rqst.body)         
        page = msgraph.MSGraphApi(cookies=cookie, json=json_data, verify=False)
        page.save_session()

        pass


