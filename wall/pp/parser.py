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


    def parsing(self, html, count):
        soup=BeautifulSoup(html, 'html.parser')
        app=soup.find('div', {'id':'app'})
        div=app.find('div', {'id':count})

        pages=div.select('img')
        return [i['src'] for i in pages]

    def counting_pages(self, driver, html , link): 
        time.sleep(2) 
        raw_list=driver.find_elements_by_class_name('MuiButton-label')
        for i in raw_list:
            if i.text.find('/')>-1:
                raw_count=i.text
        
        gesture=raw_count.find('/')
        count=int(raw_count[gesture:].replace('/', ''))
        data=[]
        for i in range(1, count+1):
            images=self.open(html, i)
            for image in images:

                data.append(image)
        time.sleep(0.5)
        return data

    def open(self, content, count):
        manga_pages=self.parsing(content, count)
        return manga_pages

    def get_data(self, driver, link):
        driver.get(link)
        time.sleep(1.5)
        try:
            button=driver.find_element_by_class_name('c26')
        except:
            button=None
        if button:
            self.login(driver=driver ,button=button)
            time.sleep(1)

        time.sleep(1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        driver.execute_script('window.scrollTo(0, 10)')
        lenOfPage = int(driver.execute_script('return document.body.scrollHeight'))#200 
        match=True
        times=lenOfPage//1000
        while match:
            lastCount=lenOfPage
            
            for i in range(0, times+1):
                driver.execute_script('window.scrollBy(0, 1000)')
                time.sleep(0.4)
            lenOfPage = int(driver.execute_script('return document.body.scrollHeight'))
            times=(lenOfPage-lastCount)//1000
            if lastCount==lenOfPage:
                match=False

        content=driver.page_source
        data=self.counting_pages(driver, content, link)
        return data

    def start(self, link, isStart=False):
        if isStart:
            chrome_options = Options()  
            chrome_options.add_argument("--headless")  
            driver=webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
            driver.set_window_size(1366, 768)
            data=self.get_data(driver, link)
            driver.close()
            return data
        return None


    
# t=Parser()
# d=t.start("https://remanga.org/manga/one_hundred_to_make_god/ch452253", True)
# print(d)
    

