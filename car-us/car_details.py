import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

data = pd.read_csv('data1.csv')
names =  data['name'].values.tolist()
links = data['path'].values.tolist()

driver = webdriver.Chrome()
driver.maximize_window()

hq_image = []

df = []

for link in links:
    new_link = f'https://repairpal.com{link}'
    
    driver.get(new_link)
    name = driver.find_element(By.XPATH,"//div[@class = 'ng-heading-1 ng-pr16']").text
    about = driver.find_element(By.XPATH,'//div[@class="content ng-flex-xlarge-7 ng-flex-large-7 ng-flex-medium-12 ng-pr16"]').text
    message = driver.find_element(By.XPATH,'//div[@class="ng-pb32"]').text
    try:
        images = driver.find_elements(By.XPATH,'//img[@class="lazy image-element"]')
        for image in images:
            hq_image.append(image.get_attribute('src'))
    except:
        hq_image = None
        
 
    
    address = driver.find_element(By.XPATH,'//div[@class="ng-pt8"]').text.split('\n')[0]
    city = driver.find_element(By.XPATH,'//div[@class="ng-pt8"]').text.split('\n')[1].split(',')[0]
    state = driver.find_element(By.XPATH,'//div[@class="ng-pt8"]').text.split('\n')[1].split(',')[1]
    # zipcode = driver.find_element(By.XPATH,'//div[@class="ng-pt8"]').text.split('\n')[1].split(',')[1].split(' ')[1]
    try:
        email = driver.find_element(By.XPATH,"//a[@class='ds-body-regular ds-link ds-link--variant-regular ds-link--external-link']").get_attribute('href')
    except:
        email = None
    time.sleep(2)
    click1 = driver.find_elements(By.XPATH,'//div[@class="collapsible-summary ng-flex ng-space-between ng-pr16"]')[-1]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6.5);") 
    time.sleep(2)
    actions = ActionChains(driver)
    actions.move_to_element(click1)
    actions.click(click1)
    actions.perform()
    time.sleep(2)
    text1 = driver.find_element(By.XPATH,'//div[@class=" collapsible collapsible--open"]').text
    of = text1.find('of')
    month = text1.find('month')
    mile = text1.find('mile')
    warrentyMonth = f'{text1[mile+9:month-1]} months'
    warrentyTime = text1[mile+9:month-1] 
    warrentyMileage = text1[of+2:mile-1]
    click2 = driver.find_element(By.XPATH,'//div[@class="ng-flex ng-center"]')
    actions = ActionChains(driver)
    actions.click(click2)
    actions.perform()
    time.sleep(2) 
    
    categories = driver.find_elements(By.XPATH,'//div[@class="amenities-category"]')
    transportationAmenities = None
    discountAmenities = None
    filterOption = None
    
    for cat in categories:
        text = cat.text        
        if text.find('Transportation Assistance') > -1:
            transportationAmenities = text.split('\n')[1:]
            
    for cat in categories:
        text = cat.text        
        if text.find('Discount') > -1:
            discountAmenities = text.split('\n')[1:]
            
    for cat in categories:
        text = cat.text        
        if text.find('Services') > -1:
            filterOption = text.split('\n')[1:]
    
    
    
    
    print(name)
    df.append([name,about,message,hq_image,address,city,state,email,warrentyMonth,warrentyTime,warrentyMileage,transportationAmenities,discountAmenities,filterOption])
    
data = pd.DataFrame(df,columns =['name','about','message','hq_image','address','city','state','email','warrentyMonth','warrentyTime','warrentyMileage','transportationAmenities','discountAmenities','filterOption'])
data.to_csv('data2.csv',index=False)