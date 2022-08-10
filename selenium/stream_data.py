from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

# Define the web shipping options
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Initialise the driver
driver_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(driver_path, chrome_options=options)

driver.get('https://sullygnome.com/')

streamer = 'Gaules'

# Write keywords on the search bar
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[2]/div[1]/div/div[3]/div/input')))\
    .send_keys(streamer)

# Select on the list
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/ul/li[1]/div/a[1]/span')))\
    .click()

# Select 365 days
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[2]/div[2]/div[2]/div/div[2]/div[7]/div/a')))\
    .click()

# Look for all streams
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[2]/div[2]/div[6]/div[1]/div/div[1]/div[2]/div/div[3]/a')))\
    .click()


# Data extraction
texto_columnas = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[5]/div/div/div/div/div[1]/div[2]/div/table')
texto_columnas = texto_columnas.text
#texto_columnas = texto_columnas.find_elements(By.cssSelector('a [data-gamename]'))
print(texto_columnas)
array_columna = texto_columnas.split('\n')
print(len(array_columna))


# Data processing
hora_inicio = []
hora_fin = []
long_stream = []
tiempo_visualizacion = []
average_viewers = []
max_viewers = []
seguidores_ganados = []
seguidores_hora = []
visitas = []
visitas_hora = []

cabecera = array_columna.pop(0)

for i in range (0, len(array_columna),9):
    hora_inicio.append(array_columna[i])
    hora_fin.append(array_columna[i+1][:array_columna[i+1].find(':')+2])
    long_stream.append(array_columna[i+1][array_columna[i+1].find(':')+3:])
    tiempo_visualizacion.append(array_columna[i+2])
    average_viewers.append(array_columna[i+3])
    max_viewers.append(array_columna[i+4])
    seguidores_ganados.append(array_columna[i+5])
    seguidores_hora.append(array_columna[i+6])
    visitas.append(array_columna[i+7])
    visitas_hora.append(array_columna[i+8])


# Save on DataFrame
df = pd.DataFrame({'Hora inicio' : hora_inicio,
                       'Hora fin' : hora_fin,
                       'Longitud directo' : long_stream,
                       'Tiempo de visualizacion' : tiempo_visualizacion,
                       'Espectadores medios' : average_viewers,
                       'Espectadores maximos' : max_viewers,
                       'Seguidores ganados' : seguidores_ganados,
                       'Seguidores por hora' : seguidores_hora,
                       'Visistas' : visitas,
                       'Visitas por hora' : visitas_hora})

# Data export
pd.to_excell('data_stream.xls')
