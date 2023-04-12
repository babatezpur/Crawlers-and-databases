import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import mysql.connector
from mysql.connector import MySQLConnection
from time import sleep
import options
from options import Options, attrs
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

def helper(x:list, d:dict) -> list:
    ans=[]
    for i in x:
        s=str(i)
        s=s.split("'")
        temp=s[1]
        if '.com' not in temp:
            temp1=temp
            if 'www.' in temp:
                temp1=temp[4:]
            ans.append(temp1)
            d[temp1]=temp
            continue
        temp2=temp.split('.com')
        temp3=temp2[0].split('.')
        fin=""
        fin+=temp3[len(temp3)-1]+".com"
        index=1
        while index<len(temp2):
            fin+=temp2[index]
            index+=1
        ans.append(fin)
        d[fin]=temp
    return ans

print("Enter the roles one at a time. When done, Enter 'DONE'. ")
done=False
roles=[]
while not done:
	s=input()
	roles.append(s)
	if s=="DONE":
		done=True
roles=roles[:len(roles)-1]
# https://chromedriver.chromium.org/
driver=webdriver.Chrome(executable_path="D:/chromedriver.exe",options=options)
print("Entering :")
print(time.ctime())
driver.get("https://app.apollo.io")                

db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

cursor = db.cursor()
query="select distinct url from growth_store_details_klaviyo where (Updated='N') limit 5"
d={}
cursor.execute(query)
result=cursor.fetchall()
orgs=helper(result,d)


time.sleep(3)

mail=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//input[@placeholder='Work Email']")))
mail.send_keys('xxxxx@yyyyyy.io')
time.sleep(2)
pwd=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//input[@placeholder='Enter your password']")))
pwd.send_keys('yyyyyyy@12345')
pwd.send_keys(Keys.RETURN)
time.sleep(6)
driver.get('https://app.apollo.io/#/people')
time.sleep(8)
current=1
search=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[5]/div')))

search.click()
for i in orgs:
    print(current)
    #time.sleep(1)
    time.sleep(1)
    name=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//input[@class='Select-input ']")))
    time.sleep(1)
    for b in range(20):
        name.send_keys(Keys.BACKSPACE)
    name.send_keys(i)
    time.sleep(3)
    name.send_keys(Keys.ENTER)
    time.sleep(3)
    names=driver.find_elements_by_xpath("//div[@class='zp_PrhFA']")
    if len(names)==0:
        query2="update growth_store_details_klaviyo set Updated='Y' where url = %s"
        db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

        cursor = db.cursor()
        cursor.execute(query2,(d[i],))
        db.commit()
        current+=1
        continue
    emp=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/a[1]'))).text

    emp_no=""
    k=False
    print("Yes ht")
    print(emp)
    for j in emp:
        if(j.isdigit() or j=='.'):
            emp_no+=j
        if j=='K':
            k=True
    if emp_no=="" or emp_no=='222.8':
        current+=1
        continue
    emp_no=emp_no.split('.')[0]
    emp_count=int(emp_no)
    if k==True:
        emp_count=emp_count*1000
    print(i)
    print(emp_count)
    if emp_count<=5:
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//i[@class='zp-icon mdi mdi-menu-down zp_2BRav zp_35LDu zp_g96Mj']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div/div/div[3]'))).click()    
        time.sleep(4)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@data-cy='toolbar-action-export-button']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@class='zp-button zp_1X3NK']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@class='zp-button zp_1X3NK']"))).click()
        time.sleep(4)
        query2="update growth_store_details_klaviyo set Updated='Y' where url = %s"
        db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

        cursor = db.cursor()
        cursor.execute(query2,(d[i],))
        db.commit()
        current+=1
        continue
    rsrch=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[4]/div/span[2]"))).click()

    for role in roles:
        time.sleep(2)
        rname=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//input[@class='Select-input ']")))
        time.sleep(1)
        for b in range(20):
            rname.send_keys(Keys.BACKSPACE)
        rname.send_keys(role)
        time.sleep(3)
        rname.send_keys(Keys.ENTER)
        time.sleep(4)
        collected=[]
        update_list=[]
        time.sleep(1)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//i[@class='zp-icon mdi mdi-menu-down zp_2BRav zp_35LDu zp_g96Mj']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div/div/div[3]'))).click()    
        time.sleep(4)
        try:
            WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@data-cy='toolbar-action-export-button']"))).click()
        except:
            rname=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//input[@class='Select-input ']")))
            time.sleep(1)
            for b in range(30):
                rname.send_keys(Keys.BACKSPACE)
            continue
        time.sleep(3)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@class='zp-button zp_1X3NK']"))).click()
        time.sleep(4)
        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,"//div[@class='zp-button zp_1X3NK']"))).click()
        time.sleep(4)

    WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[4]/div[1]/span[2]'))).click()
    current=current+1
    query2="update growth_store_details_klaviyo set Updated='Y' where url = %s"
    db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

    cursor = db.cursor()
    cursor.execute(query2,(d[i],))
    db.commit()
    current+=1
    time.sleep(2)
    search=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[5]/div[1]')))

    time.sleep(2)
    search.click()
    
print("Exiting : ")
print(time.ctime())
driver.close()
