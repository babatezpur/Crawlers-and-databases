//Script to capture facebook ads by various companies/organizations.


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import datetime
import mysql.connector
from time import sleep
import options
from options import Options, attrs
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--window-size=1920,1080")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
def todate(date: str) -> dict:
    months={'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05','Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    year=date[-4:]
    rest=date[:-5]
    mon=rest[-3:]
    month=months[mon]
    #year=date.split(", ")[1]
    day_temp=date.split(", ")[0]
    day=day_temp.split(" ")[1]
    day=date[:1]
    #if len(day)==1:
    #   day="0"+day
    final_date=year+"-"+month+"-"+day
    dic={'date':final_date, 'month':mon}
    return dic
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
        fin+=temp3[len(temp3)-1]
        """fin+=temp3[len(temp3)-1]+".com"
        index=1
        while index<len(temp2):
            fin+=temp2[index]
            index+=1
        """
        ans.append(fin)
        d[fin]=temp
    return ans
driver=webdriver.Chrome(executable_path="D:/chromedriver.exe",options=options)
driver.get("https://facebook.com")
time.sleep(3)
idlink=driver.find_element_by_id("email")
idlink.send_keys("alexxxxxxxxxx@gmail.com")
idlink=driver.find_element_by_id("pass")
idlink.send_keys("xxxxxx@1234")
idlink.send_keys(Keys.ENTER)
time.sleep(3)
driver.get("https://facebook.com/ads/library")
db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')
cursor = db.cursor()
query="select domain from domains_to_process_priority where (fb_status='N' and num_employees>0) limit 10"
query1=(
        "insert into fb_ads_main (brand, domain, ads_count, fb_handle, fb_likes, ig_handle, ig_followers, date_of_creation, date_of_crawl)"
        "values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
query2=(
    "insert into fb_ads_list (brand, domain, ad_id, active, date_of_ad, month_of_ad, multiple_versions, versions, description, ad_link)"
    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
query3="update domains_to_process_priority set fb_status='Y' where domain = %s"
d={}
cursor.execute(query)
result=cursor.fetchall()
domain_names=helper(result,d)
time.sleep(3)
al=driver.find_elements_by_xpath("//div[@class='s7wjoji2 tds9wb2m']")
al[0].click()
time.sleep(1)
sel_al=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div/div/div[2]/div')                                    
sel_al.click()
al[1].click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div[2]").click()
#####################################################################################
domain_names=[ "mamaearth"]
#####################################################################################
for brand in domain_names:
    d[brand]=brand+'.com'
    time.sleep(2)
    place=driver.find_element_by_xpath("//input[@placeholder='Search by keyword or advertiser']")
    for bs in range(50):
        place.send_keys(Keys.BACKSPACE)
    place.send_keys(brand)
    time.sleep(3)
    place.send_keys(Keys.ARROW_DOWN)
    place.send_keys(Keys.ENTER)
    numres=WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.CLASS_NAME,'_7gn2')))
    if numres.text=='0 results':
        #code for marking visited in db
        continue
    num_ads=""
    x=numres.text
    for i in x:
        if i.isnumeric():
            num_ads+=str(i)
    num_ads=int(num_ads)
    num_ads_use=min(num_ads,150)
    print(str(num_ads)+" ads")

    """
    name=driver.find_elements_by_xpath("//span[@role='heading']")
    name=str(name[0].text)
    print("Name : "+name)
    """

    fb_handle=str(driver.find_element_by_xpath("//div[@class='i0ppjblf e946d6ch']").text)
    fb_likes=str(driver.find_element_by_xpath("//div[@style='display: flex;']").text)
    temp=fb_likes.split(" ")[0]
    fb_likes=int(temp.replace(',',""))
    ig=driver.find_elements_by_xpath("//div[@class='i0ppjblf e946d6ch']")
    ind=0
    f=False
    for i in ig:
        if "followers" in i.text:
           f=True
           break
        ind=ind+1
    ig_handle=""
    ig_folls=""
    if f==True:
        ind=ind-1
        ig_handle=str(ig[ind].text)
        ind=ind+1
        ig_folls=(ig[ind].text).split(" ")[0]
        ig_folls=int(ig_folls.replace(',',""))
    creation_date=""
    #try:
     #   creation_date=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div[2]/div[1]/span[2]').text
    #except:
     #   creation_date=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[3]/div[1]/div[1]/div/div/div[2]/div/div[2]/div[1]/span[2]').text
    #dict_temp=todate(str(creation_date))
    #print("creation date: "+str(creation_date))
    #date=dict_temp['date']
    #month=dict_temp['month']
    date=""
    results_so_far=num_ads
    today=datetime.date.today()
    today=str(today.strftime("%Y-%m-%d"))
    data=(
        brand, d[brand], num_ads, fb_handle, fb_likes, ig_handle, ig_folls, date, today
        )
    db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

    cursor = db.cursor()
    cursor.execute(query1, data)
    db.commit()
    cursor.close()
    page=driver.find_element_by_tag_name('html')
    a=7
    if num_ads_use<120:
        a=4
    if num_ads_use<60:
        a=2
    for scroll in range(a):
        ads=driver.find_elements_by_xpath("//div[@class='_9b9p _99s6']")
        page.send_keys(Keys.END)
        time.sleep(1.5)
    ads=driver.find_elements_by_xpath("//div[@class='_9b9p _99s6']")
    count=1
    ad_data=[]
    for ad in ads:
        print("------------------AD NUMBER: "+str(count)+"-----------------------")
        text=ad.text
        active=False
        multiple_ver=False
        desc=""
        act_date=text.split("\nPlatforms\n")
        arr_act_date =act_date[0].split("\n")
        if arr_act_date[0]=='Active':
            active=True
        date=arr_act_date[1]
        date=date.split("Started running on ")[1]
        dict_temp=todate(date)
        date=dict_temp['date']
        ad_month=dict_temp['month']
        post_date=act_date[1].split("\n")
        ad_id_ind=post_date[0]
        multile_ver=False
        if ad_id_ind=='This ad has multiple versions':
            multiple_ver=True
        if multiple_ver==True:
            ad_id_ind=post_date[1]
        versions=""
        if multiple_ver==True:
            checkVer=post_date[2]
            if 'creative and text' in checkVer:
                for i in checkVer:
                    if i.isnumeric():
                        versions+=i
        else:
            checkVer=post_date[1]
            if 'creative and text' in checkVer:
                for i in checkVer:
                    if i.isnumeric():
                        versions+=i
        ad_id=str(ad_id_ind.split("ID: ")[1])
        print("Ad ID: "+ str(ad_id))
        spon=act_date[1]
        des=str(spon.split("Sponsored\n")[1])
        description=""
        for i in des:
            if i.isascii()==True:
                description+=i
        ad_link="https://www.facebook.com/ads/library/?id="+ad_id
        info=(
            str(brand), str(d[brand]), str(ad_id), str(active) , date, ad_month, str(multiple_ver), str(versions), description, ad_link
            )
        ad_data.append(info)
        print(len(ad_data))
        if len(ad_data)%10==0:
            db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

            cursor = db.cursor()
            cursor.executemany(query2, ad_data)
            db.commit()
            cursor.close()
            ad_data.clear()
        count=count+1
        time.sleep(0.5)
    db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

    cursor = db.cursor()
    cursor.execute(query3, (d[brand],))
    cursor = db.cursor()
    cursor.executemany(query2, ad_data)
    db.commit()
    cursor.close()
    print("***********Done for one brand**************")
    print(time.ctime())
    print(" ")
    
                 
    
