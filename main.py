import time
import os
from selenium import webdriver
from datetime import datetime,timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from config import *


    
class Browser:           
    def __init__(self,headless=False):
        print('Preparing stuff...')
        if headless:
            self.browser=webdriver.PhantomJS('phantomjs.exe',service_args=['--load-images=no'])
        else:
            self.browser=webdriver.Chrome('chromedriver.exe',service_args=['--load-images=no'])
        self.url='https://www.eventcinemas.co.nz'
        
        #Open a new tab to login, switch back to original tab while waiting
        self.browser.execute_script("window.open('"+self.url+"', 'new_window')")
        self.browser.switch_to_window(self.browser.window_handles[0])

        #Open original tab while waiting for login tab to load
        self.browser.get(self.url+'/Movies/NowShowing')
        
        #Login then switch back to original tab
        self.browser.switch_to_window(self.browser.window_handles[1])
        self.login()
        self.browser.switch_to_window(self.browser.window_handles[0])

        
    def moviesList(self,movies):
        mList=[]
        for movie in movies:
            name=movie.get_attribute("data-name")
            cinemas=movie.get_attribute("data-cinemas").replace('"','').split(',')
            firstsession=movie.get_attribute("data-firstsession")
            link=movie.find_element_by_xpath(".//a").get_attribute('href')
            mDict={"name":name,
                   "cinemas":cinemas,
                   "firstsession":firstsession,
                   "link":link,
                   "movie":movie,
            }
            mList.append(mDict)
        return mList
    def login(self):
        print("Logging in...")
        try: #non-mobile
            form=self.browser.find_element_by_class_name('login-section')
            form.click()
        except: #mobile
            form=self.browser.find_element_by_class_name('mobile-cinebuzz')
            form.click()
        time.sleep(0.5)    
        username = self.browser.find_element_by_id('Username')
        username.send_keys(VARS['USERNAME'])
        password=self.browser.find_element_by_id('Password')
        password.send_keys(VARS['PASSWORD'])
        button=self.browser.find_element_by_xpath("//a[@class='blue  submit btn']")
        button.click()
    def getNowShowing(self):
        while True:
            self.nowshowing=self.browser.find_elements_by_xpath("//div[@class='movie-container-item split-content']")
            if len(self.nowshowing)!=0:
                break
            time.sleep(0.5)
        self.mList=self.moviesList(self.nowshowing)
    def chooseMovie(self):
        os.system('cls') 
        self.getNowShowing()
        #Print all now showing movies
        for order in range(len(self.mList)):
            print(order+1,end='. ')
            print(self.mList[order]["name"])
        #Choose one    
        t=int(input('Choose a movie: '))
        self.browser.get(self.mList[t-1]["link"]+"#cinemas="+str(VARS['CINEMA'])+"")
        

    def chooseTime(self):
        os.system('cls')
        date=datetime.today()
        today=date.strftime('%Y-%m-%d')
        activedate=self.browser.find_element_by_xpath("//a[@class='date active']").get_attribute("data-date")
        
        #Get earliest session
        if activedate!=today:
            print('No sessions today at Queen Street') #TODO make this more dynamic
            print('Earliest session on '+activedate)     
        
        while True:
            times=self.browser.find_elements_by_xpath("//a[@class='session-btn']")
            try:
                self.browser.find_element_by_xpath("//div[@class='filter-message' and @style='display: block;']")
                date=date + timedelta(days=1)
                self.browser.find_element_by_xpath("//a[@class='date' and @data-date='"+date.strftime('%Y-%m-%d')+"']").click()
                continue    
            except: pass
            if len(times)>0:break

        print('Showing time sessions for '+date.strftime('%Y-%m-%d'))
        count=0
        for timeSession in times:
            count+=1
            print(count,end='. ')
            print(timeSession.text)
            
        #Choose time session
        t=int(input('Choose time: '))
        times[t-1].click()
        
    def chooseTickets(self):
        os.system('cls') 
        t=int(input('Number of tickets: '))
        self.numoftickets=t
        while True:
            try:
                rows = self.browser.find_elements_by_xpath("//tr[@data-price='10' and @data-hidden='false']") #NZ Student, up to 1
            except:
                time.sleep(0.5)
                continue
            break
        try:
            star=self.browser.find_element_by_xpath("//tr[@data-price='9' and @data-hidden='false']") #Movie of the week, up to 4
            select=star.find_elements_by_xpath(".//option")
            tickets=min(t,4)
            t-=tickets
            select[tickets].click()
        except: pass
        
        for row in rows:
            select=row.find_elements_by_xpath(".//option")
            tickets=min(t,len(select)-1)
            t-=tickets
            select[tickets].click()
        if t>0:
            row = self.browser.find_element_by_xpath("//tr[@data-hidden='false' and @data-hocode='STUD']") #Students, up to 10
            select=row.find_elements_by_xpath(".//option")
            tickets=min(10,t)
            select[tickets].click()        
        self.browser.find_element_by_xpath("//a[@class='blue continue btn']").click()
        
    def chooseSeats(self):
        os.system('cls') 
        while True:
            try: table=self.browser.find_element_by_xpath("//div[@class='seats']")   #Keep getting the element until the page has fully loaded
            except:
                time.sleep(0.5)
                continue
            break
        rows=table.find_elements_by_xpath(".//ul[@class='row']")
        grid=[[[True,slot] if slot.get_attribute('class')=='0 ' else [False,slot] for slot in row.find_elements_by_xpath(".//li")] for row in rows]
        

        #This part uses brute force so it takes time...
        gridpoints=calculate(grid)
        point=0
        jval=0
        ival=0
        for i in range(len(grid)):   
            for j in range(len(grid[0])-self.numoftickets+1):
                if check(grid[i][j:j+self.numoftickets])==True:
                    total=sum(gridpoints[i][j:j+self.numoftickets])
                    if total>point:
                        point=total
                        ival=i
                        jval=j
        print('Your seats: ')                
        for j in range(jval,jval+self.numoftickets):
            grid[ival][j][1].click()
            title=grid[ival][j][1].get_attribute('title')
            print(title,end=' ')
            grid[ival][j][0]='Chosen'
        print()
        visualisegrid(grid)
        self.browser.find_element_by_xpath("//a[@class='continue check']").click()        
    def pay(self):
        while True:
            try:self.browser.find_element_by_xpath("//div[@class='debit-cards payment']").click()
            except:
                time.sleep(0.5)
                continue
            
            break
        time.sleep(0.5)
        cnum = self.browser.find_element_by_id('CardNumber')
        cnum.send_keys(VARS['CARD_NUM'])
        exdate=self.browser.find_element_by_id('CardExpiry')
        exdate.send_keys(VARS['EX_DATE'])
        csc=input('Enter your Card Security Code: ')
        self.browser.find_element_by_id('CardSecurityCode').send_keys(csc)
        self.browser.find_elements_by_xpath("//a[@class='blue continue btn']")[-1].click()
           
def  main():
    browser=Browser() 
    browser.chooseMovie()
    browser.chooseTime()
    browser.chooseTickets()
    browser.chooseSeats()
    browser.pay()
    #browser.browser.quit()
    
        
    
if __name__=="__main__":
    startTime = datetime.now()
    main()
    print(datetime.now() - startTime)
    input('Thanks!')

