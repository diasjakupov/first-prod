from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class Parser:
    def login(self, driver,button):
        button.click()
        time.sleep(1)
        login_input=driver.find_element_by_id('login')
        login_input.send_keys('Yaroslav')
        password_input=driver.find_element_by_id('password')
        password_input.send_keys('sg9Fawi9rif8izk')
        submit=driver.find_element_by_css_selector("button[type='submit']")
        submit.click()
        time.sleep(1)
        driver.refresh()
        time.sleep(3)


    def parsing(self, html):
        soup=BeautifulSoup(html, 'html.parser')
        app=soup.find('div', {'id':'app'})
        div=app.find('div', {'id':'1'})
        pages=div.select('img')
        return [i['src'] for i in pages]
        

    def open(self, driver, link='https://remanga.org/manga/past-life-of-the-thunder-god/ch449236'):
        driver.get(link)
        time.sleep(1)
        try:
            button=driver.find_element_by_class_name('c26')
        except:
            button=None
        if button:
            self.login(driver=driver ,button=button)

        content=driver.page_source
        manga_pages=self.parsing(content)
        return manga_pages


    def start(self, link='', isStart=False):
        if isStart:
            chrome_options = Options()  
            chrome_options.add_argument("--headless")  
            driver=webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
            data=self.open(driver, 'https://remanga.org/manga/i-am-the-one-and-only-bully-in-this-novel/ch447204')
            driver.close()
            return data
        return None
    
    

