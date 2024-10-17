from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
import requests
from bs4 import BeautifulSoup
import time

class DataEntry:
    def __init__(self):
        self.form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdagVYr_JkF4FXtcD82GL3f4rR9FUN6Mg4MJz1AKwNC3ZdG2Q/viewform?usp=sf_link"
        self.zillow_clone_url = "https://appbrewery.github.io/Zillow-Clone/"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.property_prices = []
        self.property_addresses = []
        self.property_links = []

    def get_data(self):
        response = requests.get(url=self.zillow_clone_url)
        data = response.text
        soup = BeautifulSoup(data,"html.parser")
        prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
        addresses = soup.find_all(class_ = "StyledPropertyCardDataWrapper")
        for price in prices:
            data = price.text[:6]
            if "+" in data:
                data = data.replace("+","")
            self.property_prices.append(data)

        for loc in addresses:
            tag = loc.find("a")
            link = tag.get("href")
            self.property_links.append(link)
            addr = tag.text.strip()
            if " | " in addr:
                addr = addr.replace(" | ",", ")
            self.property_addresses.append(addr)

        # print(self.property_addresses)
        # print(len(self.property_addresses))
        # print(self.property_links)
        # print(len(self.property_links))
        # print(self.property_prices)
        # print(len(self.property_prices))
    def fill_form(self):
        self.driver.get(self.form_url)
        time.sleep(3)
        for i in range(len(self.property_links)):
            all_inputs = self.driver.find_elements(By.CLASS_NAME, value="AgroKb")
            address_input = all_inputs[0].find_element(By.TAG_NAME, value="input")
            price_input = all_inputs[1].find_element(By.TAG_NAME, value="input")
            link_input = all_inputs[2].find_element(By.TAG_NAME, value="input")
            address = self.property_addresses[i]
            price = self.property_prices[i]
            link = self.property_links[i]
            address_input.send_keys(address)
            price_input.send_keys(price)
            link_input.send_keys(link)
            time.sleep(2)
            submit = self.driver.find_element(By.XPATH, '//*[@jsname="M2UYVd"]')
            submit.click()
            time.sleep(2)
            submit_again = self.driver.find_element(By.LINK_TEXT,value="Submit another response")
            submit_again.click()
            time.sleep(2)

response_sheet_link = "https://docs.google.com/spreadsheets/d/1whCFVLnSD9tkilOT8W2wRhLaa9ULDh6TX7-03s1O370/edit?resourcekey=&gid=529217484#gid=529217484"
de = DataEntry()
de.get_data()
de.fill_form()