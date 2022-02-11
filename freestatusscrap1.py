from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from tqdm import tqdm
from multiprocessing import Pool
import threading
import json
threadLocal = threading.local()

leftproductids=["3633","3659","3749","3785","3824","3827","3828","4000","4051","4059","4060","4061","4230","4236","4238","4548","4566","4700","4874","4997","5041","5096","5167","5304","5338","5519","5543","5610","5632","5647","5653"]
df = pd.read_csv("coursera1.csv", encoding='cp1252')
links = df['link']
productids = df['product_id']
print(len(productids))


    # Writing to sample.json
with open("courseraproductids.json", "w") as outfile:
    outfile.write(str(list(productids)))
    print("file written")
urls = []
for i,link in enumerate(links):
    link = link.split("murl=")[1]
    link = link.replace("%3A", ":")
    link = link.replace("%2F", "/")
    urls.append({"product_id":str(productids[i]),"link":link})
allcoursedetails=[]
urls=urls[3000:]
urls=[url for url in urls if str(url["product_id"]) in leftproductids]
def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        PATH="C:\Program Files (x86)\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=PATH,options=chrome_options)
        setattr(threadLocal, 'driver', driver)
    return driver

def scrap(url):
    print(urls.index(url))
    driver = get_driver()
    coursedetail={}
    coursedetail["product_id"]=url["product_id"]
    driver.get(url["link"])
    time.sleep(4)
    try:
        enrollelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"EnrollButton")))
        time.sleep(3)
        try:
            headingelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//h1")))
            if(headingelement):
                heading=headingelement.get_attribute("innerHTML")
            else:
                heading="NA"
        except:
            heading="NA"
        try:
            finaidelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//button[@class="button-link finaid-link"]')))
            if('Financial aid' in finaidelement.get_attribute("innerHTML")):
                coursedetail["financial_aid"]=True
            else:
                coursedetail["financial_aid"]=False
        except:
            coursedetail["financial_aid"]=False
        time.sleep(2)
        if('specialization' in heading.lower()):
            type="specialization"
        elif('professional certificate' in heading.lower()):
            type="professional certificate"
        elif(heading=="NA"):
            type="NA"
        else:
            type="course"
        coursedetail["type"]=type
        if('start guided project' in enrollelement.text.lower()):
            coursedetail["type"]="guided project"
        enrollelement.click()
        if(url["link"]==urls[0]["link"] or url["link"]==urls[4]["link"]):
            time.sleep(60)
        print("Hello time up")
        try:
            nextprogramelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//button[@class="primary cozy m-y-1"]')))
            print(nextprogramelement)
            chooseprogramelement=driver.find_element_by_xpath('//p[@class="headline-5-text punch-line"]')
            if(chooseprogramelement and chooseprogramelement.get_attribute("innerHTML")=="Choose a program"):
                nextprogramelement.click()
                time.sleep(3)
        except:
            pass
        try:
            priceelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//span[@class="rc-ReactPriceDisplay"]/span')))
            price=priceelement.get_attribute("innerHTML")[1:]
        except:
            price="NA"
        try:
            contentelement=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'c-modal-content')))
            content=contentelement.text
        except:
            content="NA"
            
        if(content=="NA"):
            coursedetail["costfree"]="NA"
        elif "Full Course, No Certificate" in content:
            coursedetail["costfree"]="full free"
        elif "Audit " in content:
            coursedetail["costfree"]="audit"
        else:
            coursedetail["costfree"]="no"
        coursedetail["price"]=price 
    except:
        coursedetail["type"]="NA"
        coursedetail["financial_aid"]="NA"
        coursedetail["costfree"]="NA"
        coursedetail["price"]="NA"
    return coursedetail


if __name__ == '__main__':
    p = Pool(2)
    coursedetails=p.map(scrap,urls)
    p.close()
    p.join()
    json_object = json.dumps(coursedetails)

    # Writing to sample.json
    with open("freedetails1.json", "w") as outfile:
        outfile.write(json_object)
  

