import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.imovirtual.com/comprar/apartamento/?search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=153&page=1'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
page_limit = int(soup.find('div', {'class': 'col-md-content section-listing__row-content'}).find('nav',{'class': 'pull-left'}).find_all('li')[4].text)

ids = []

for x in range(1, page_limit):
    url = f'https://www.imovirtual.com/comprar/apartamento/?search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=153&page={x}'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    articles = soup.find('div', {'class': 'col-md-content section-listing__row-content'}).find_all('article')
    id_houses = [article.get('data-url').split('-')[-1] for article in articles]
    ids.extend(id_houses)
    print(f'page {x} appended')

ids_houses = pd.DataFrame({'id': ids})
ids_houses.to_csv(r'C:\Users\josej\Programming for Data Science\Programming Course\Group project\ids_houses_imo.csv', index=False)

ids_houses_csv = pd.read_csv(r'C:\Users\josej\Programming for Data Science\Programming Course\Group project\ids_houses_imo.csv')

ids_houses = pd.DataFrame(ids_houses_csv['id'])


def get_information_houses(id_inhouses):
    print('\nHouse number: ' + id_inhouses)
    url = 'https://www.imovirtual.com/pt/anuncio/'+id_inhouses
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    title = "NA"
    location = "NA"
    price = "NA"
    topology = "NA"
    area = "NA"
    try:
        title = soup.find('h1', {'class': 'css-1wnihf5 efcnut38'}).text.strip()
    except:
        print('Title not found') 
    print('Title: '+ title)
    try:
        location = soup.find('a', {'class': 'e1w8sadu0 css-qan2aj exgq9l20'}).text.strip().replace(', Lisboa', '')
    except:
        print('Location not found')
    try:
        price = soup.find('strong', {'class': 'css-1i5yyw0 e1l1avn10'}).text.strip().replace('€', '').replace(' ', '')
    except:
        print('Price not found')
    try:
        topology = soup.find('div', {'aria-label': 'Tipologia'}).find('div', {'class': 'css-1ytkscc e1qm3vsd3'}).text.strip()
    except:
        print('Topology not found')
    try:
        area = soup.find('div', {'aria-label': 'Área bruta (m²)'}).find('div', {'class': 'css-1ytkscc e1qm3vsd3'}).text.strip().replace(',','.').replace(' m²','')
    except:
        print('Area not found')
    
    houses = pd.Series({'HouseID': id_inhouses,
                        'Title': title,
                        'Location': location,
                        'Price': price,
                        'Gross_Area': area,
                        'Topology': topology})
    
    return houses


houses_list = []
for id_inhouses in ids_houses['id']:
    houses_list.append(get_information_houses(id_inhouses))

df_houses = pd.concat(houses_list, axis=1).T
df_houses.reset_index(drop=True, inplace=True)

df_houses.to_csv(r'C:\Users\josej\Programming for Data Science\Programming Course\Group project\houses_imo1.csv', index = False)

