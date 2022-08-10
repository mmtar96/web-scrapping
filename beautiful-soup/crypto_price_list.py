import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Descarga del dato en bruto
headers = {'User-Agent': ''}
url = 'https://www.coingecko.com/?page='
pages = np.arange(1, 31, 1)
data = []
for i in pages:
    url1 = url + str(i)
    html = requests.get(url1, headers = headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    fila = soup.find('div', class_ = 'coingecko-table').find('tbody').find('tr')
    name = fila.find('td', class_ = 'py-0 coin-name cg-sticky-col cg-sticky-third-col px-0').find('span', class_ = 'lg:tw-flex font-bold tw-items-center tw-justify-between')
    acr = name.find_next('span')
    precio = fila.find('td', class_ = 'td-price price text-right pl-0').find('span')
    mkt_cap = fila.find('td', class_ = 'td-market_cap cap col-market cap-price text-right').find('span')
    data.append((name.text, acr.text, precio.text, mkt_cap.text))
    for i in range(99):
        fila = fila.find_next('tr') 
        name = fila.find('td', class_ = 'py-0 coin-name cg-sticky-col cg-sticky-third-col px-0').find('span', class_ = 'lg:tw-flex font-bold tw-items-center tw-justify-between')
        acr = name.find_next('span')
        precio = fila.find('td', class_ = 'td-price price text-right pl-0').find('span')
        mkt_cap = fila.find('td', class_ = 'td-market_cap cap col-market cap-price text-right').find('span')
        data.append((name.text, acr.text, precio.text, mkt_cap.text))

# Procesamiento del dato
nombres = []
acronimo = []
precio = []
market_cap = []
for i in range(len(data)):
    precio_num  = data[i][2].split('$')
    precio_num = precio_num[1].replace(',','')
    precio.append(float(precio_num))
    market_cap_num = data[i][3].split('$')
    market_cap_num = market_cap_num[1].replace(',','')
    market_cap.append(float(market_cap_num))
    nombres_name = data[i][0].split()
    nombres.append(nombres_name[0])
    acronimo_name = data[i][1].split()
    acronimo.append(acronimo_name[0])

# Creamos un DataFrame para exportar
final_data = pd.DataFrame({'Nombre' : nombres,
                           'Acronimo' : acronimo,
                           'Precio' : precio,
                           'Market Cap' : market_cap})

# Se crea un archivo excel en el directorio de trabajo actual con los datos extraidos
final_data.to_excel('precios.xls')
