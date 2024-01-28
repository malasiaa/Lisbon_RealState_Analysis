from bs4 import BeautifulSoup as bs
import random
import time
import pandas as pd


import sys
sys.path.append(r'C:\Users\josej\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages')

import undetected_chromedriver as uc

url = 'https://www.idealista.pt/comprar-casas/lisboa/com-t0'

browser = uc.Chrome()
browser.get(url)
browser.find_element("xpath",'//*[@id="didomi-notice-agree-button"]').click()
html = browser.page_source
soup = bs(html,'lxml')
articles = soup.find('main',{'class':'listing-items'}).find_all('article')
id_houses = [article.get('data-adid') for article in articles] 
id_houses = [houses for houses in id_houses if houses is not None]


x=1
ids = []

while True:
    
    url = f'https://www.idealista.pt/comprar-casas/lisboa/com-t0/pagina-{x}'
    browser.get(url)
    time.sleep(random.randint(5,8))
    
    try:
        browser.find_element("xpath",'//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass
    html = browser.page_source
    soup = bs(html,'lxml')
    present_page = int(soup.find('main',{'class':'listing-items'}).find('div',{'class':'pagination'}).find('li',{'class':'selected'}).text)
    if x == present_page:
        articles = soup.find('main',{'class':'listing-items'}).find_all('article')
    else:
        break
    x = x+1
    
    for article in articles:
        id_houses = article.get('data-adid')
        ids.append(id_houses)
        time.sleep(0.2)
        print(id_houses)
    ids = [houses for houses in ids if houses is not None]    
        
ids_houses = pd.DataFrame(ids)
ids_houses.columns = ['id'] 
ids_houses.to_csv(r'C:\Users\josej\Programming for Data Science\Programming Course\Group project\ids_houses_T0.csv', index = False)

houses = pd.Series()
def get_information_houses(id_inhouses):
    print('\nHouse number: ' + id_inhouses)
    url = 'https://www.idealista.pt/imovel/'+id_inhouses+'/'
    browser.get(url)
    html = browser.page_source
    soup = bs(html, 'lxml')
    
    hood = "NA"
    parish = "NA"
    price = "NA"
    gross_area = "NA"
    typology = "NA"
    
    title = soup.find('span',{'class':'main-info__title-main'}).text
    print('Title: '+ title)
    hood = soup.find('span',{'class':'main-info__title-minor'}).text.split(', ')[0]
    try:
        parish = soup.find('span',{'class':'main-info__title-minor'}).text.split(', ')[1]
    except:
        print('Parish not found')
    price = int(soup.find('span',{'class':'txt-bold'}).text.replace('.',''))
    gross_area = soup.find('div',{'class':'details-property'}).find('div',{'class':'details-property-feature-one'}).find_all('li')[0].text.split(' ')[0]
    typology = soup.find('div',{'class':'details-property'}).find('div',{'class':'details-property-feature-one'}).find_all('li')[1].text
    
    
    houses['HouseID']=id_inhouses
    houses['Title']=title
    houses['Hood']=hood
    houses['Parish']=parish
    houses['Price']=price
    houses['Gross_Area']=gross_area
    houses['Typology']=typology
    
    df_houses=pd.DataFrame(houses)
    return(df_houses.T)


df_houses = get_information_houses(ids_houses.iloc[0].id)

for i in range(1,len(ids)):
    df_houses = pd.concat([df_houses,get_information_houses(ids[i])])


df_houses.reset_index(drop=True, inplace=True)
df_houses

df_houses.to_csv(r'C:\Users\josej\Programming for Data Science\Programming Course\Group project\houses_T0.csv', index = False)