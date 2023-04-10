import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://repairpal.com/auto-repair-near-me#&zipCode=98064')

while True:
    try:
        driver.find_element(By.XPATH, "//div[@class='ng-pr16 ng-pl16 ng-pt8 ng-pb8 clickable ng-border-radius-4 ng-border-blue ng-white-background ng-font-primary-40 ng-heading-5 show-more-shops-button']")
        print('true')
        driver.find_element(By.XPATH, "//div[@class='ng-pr16 ng-pl16 ng-pt8 ng-pb8 clickable ng-border-radius-4 ng-border-blue ng-white-background ng-font-primary-40 ng-heading-5 show-more-shops-button']").click()
        time.sleep(1)
    except:
        break
   
df = []     
names =[]
phones =[]
nextOpens=[]
opens = []
firstValidAppointments=[]
appointmentsEnables  = []
imageUrls = []
ratings = []
reviewCounts = []
paths = []
distances = []

n = driver.find_elements(By.XPATH,"//h3[@class='ng-heading-3 ng-mt0 ng-mb4']")
# # distance =
for name in n:
    names.append(name.text)
p = driver.find_elements(By.XPATH,'//div[@class="ci-phone top-stack ng-pt4 ng-flex ng-flex-row ng-center-y ng-font-neutral-60"]')
for phone in p:
    phones.append(phone.text)
    
nOpen = driver.find_elements(By.XPATH,"//div[@class='ng-pl4 ']")

for nextOpen in nOpen:
    nextOpens.append(nextOpen.text[9:])

O = driver.find_elements(By.XPATH,"//div[@class='ng-pl4 ']")
for open in O:
    opens.append(open.text[:6])

first = driver.find_elements(By.XPATH,"//span[@class='ng-font-neutral-60 ds-medium']")

# for firstValidAppointment in first:
    
dis = driver.find_elements(By.XPATH,'//div[@class="ng-flex ng-flex-row ng-space-between"]')
for distance in dis:
    if distance.text.find('mi)') > -1:
        f = distance.text.find('(')
        t = distance.text.find(')')
        distances.append(distance.text[f+1:t-3])
    

appo= driver.find_elements(By.XPATH,'//div[@class = "ng-flex ng-flex-row shop-card-content "]')

for appointmentsEnable  in appo:
    appointmentsEnables.append(True if appointmentsEnable.text.find('Soonest availability') > -1 else False)
    firstValidAppointments.append(appointmentsEnable.text.split('\n')[-2].split('·')[-1] if appointmentsEnable.text.find('Soonest availability') > -1 else None)

image = driver.find_elements(By.XPATH,"//img[@class='shop-imagev2']")

for imageUrl in image:
    imageUrls.append(imageUrl.get_attribute('src'))

rat = driver.find_elements(By.XPATH,"//span[@class='ng-font-neutral-60']")

for rating in rat:
    ratings.append(rating.text[:3])
    

review =driver.find_elements(By.XPATH,"//span[@class='ng-font-neutral-60']")

for reviewCount in review:
    reviewCounts.append(reviewCount.text[5:-1])
    

pa = driver.find_elements(By.XPATH,"//a[@class='ng-flex ng-flex-row ng-heading-5 reviews-width top-stack']")

for path in pa:
    link = str(path.get_attribute('href'))[21:]
    paths.append(link)  

    # print(name,phone,nextOpen,Open,firstValidAppointment,appointmentsEnable,imageUrl,rating,reviewCount,path)
for i in range(len(names)):  
    df.append([names[i],phones[i],nextOpens[i],opens[i],firstValidAppointments[i],appointmentsEnables[i],imageUrls[i],ratings[i],reviewCounts[i],paths[i],distances[i]])
    
data = pd.DataFrame(df,columns=['name','phone','nextOpen','Open','firstValidAppointment','appointmentsEnable','imageUrl','rating','reviewCount','path','distance'])

data.to_csv('data1.csv',index=False)

# print(len(names),len(phones),len(nextOpens),len(opens),len(firstValidAppointments),len(appointmentsEnables),len(imageUrls),
#       len(ratings),len(reviewCounts),len(paths))


time.sleep(10)

driver.close()