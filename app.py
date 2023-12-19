from selenium import webdriver
from PIL import Image
from itertools import zip_longest
import pytesseract
from winotify import Notification, audio
from selenium.webdriver.chrome.options import Options
import sqlite3

import re
from time import sleep
import os


link = "https://www.workana.com/jobs?category=it-programming&has_few_bids=1&language=pt&publication=1d&skills=python&subcategory=web-development%2Cdata-science-1%2Cdesktop-apps"

caminho_tesseract_exe = ""


try:
    banco = sqlite3.connect('Workana.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM freelas")
    x = 0

except:
    banco = sqlite3.connect('Workana.db')
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE freelas (resumo text, informações text, verificar text)")
    x = 1


diretorio_atual = os.getcwd()
pasta_imagens = os.path.join(diretorio_atual, 'imagens')

if not os.path.exists(pasta_imagens):
    os.makedirs(pasta_imagens)


def salvar_e_notificar(resumo, informações, verificar):
        cursor.execute("INSERT INTO freelas (resumo, informações, verificar) VALUES (?, ?, ?)", (str(resumo), str(informações), str(verificar)))
        banco.commit()
        notificação = Notification(app_id='Novo freela', title='Novo freela', msg=resumo, duration= 'short')
        notificação.set_audio(audio.LoopingAlarm, loop=False)
        notificação.show()


def remover_numeros(texto):
    return re.sub(r'\d+', '', texto)


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options)

driver.get(link)
sleep(1)
driver.find_element('xpath',"//button[text()='Aceitar todos os cookies']").click()
driver.find_element('xpath',"//span[contains(@class,'wk2-icon')]").click()
driver.execute_script("document.body.style.zoom = '1.2';")
driver.execute_script("document.body.style.fontWeight = 'bold';")
driver.set_window_size(910, 1080)
excluir1 = driver.find_element('xpath',"//nav[contains(@class,'navbar')]")
excluir2 = driver.find_elements('xpath',"//a[contains(@class,'btn')]")
excluir3 = driver.find_elements('xpath',"//div[contains(@class,'skills')]")
excluir4 = driver.find_elements('xpath',"//div[contains(@class,'project-author')]")
excluir5 = driver.find_elements('xpath',"//a[contains(@data-content,'Lembre-se que o orçamento serve apenas como guia')]")
driver.execute_script("arguments[0].remove()", excluir1)

for item2, item3, item4, item5 in zip_longest(excluir2, excluir3, excluir4, excluir5, fillvalue=None):
    if item2:
        driver.execute_script("arguments[0].remove()", item2)
    if item3:
        driver.execute_script("arguments[0].remove()", item3)
    if item4:
        driver.execute_script("arguments[0].remove()", item4)
    if item5:
        driver.execute_script("arguments[0].remove()", item5)

driver.execute_script(f"window.scrollBy(0, 780)")
div_elements = driver.find_elements('xpath',"//div[contains(@class,'project-item')]")
altura_janela = driver.execute_script("return window.innerHeight;")
altura_body = driver.execute_script("return document.body.scrollHeight;")
div_elements = div_elements[:2]

i = 0
mover = 0

for div in div_elements:
    i += 1
    div_size = div.size
    driver.save_screenshot('imagens\\screenshot.png')
    screenshot = Image.open('imagens\\screenshot.png')
    div_screenshot = screenshot.crop((0, 0, 910, div_size['height'] + 30))
    div_screenshot.save(f'imagens\\screenshot{i}.png')
    mover += div_size['height'] + 70
    driver.execute_script(f"window.scrollBy(0, {mover})")

driver.quit()

pytesseract.pytesseract.tesseract_cmd = caminho_tesseract_exe

for c in range(2):
    image = Image.open(f"imagens\\screenshot{str(c+1)}.png")
    texto = pytesseract.image_to_string(image)
    linhas = texto.splitlines()
    resumo_linhas = linhas[:3]
    resumo = ''

    for linha in resumo_linhas:
        resumo += linha + '\n'

    verificar = remover_numeros(linhas[0])

    if x == 0:
        consulta = "SELECT * FROM freelas WHERE verificar = ?"
        cursor.execute(consulta, (str(verificar),))
        verificação = cursor.fetchall()

        if not verificação:
            sleep(5)
            salvar_e_notificar(resumo, texto, verificar)

    else:
        sleep(5)
        salvar_e_notificar(resumo, texto, verificar)

cursor.execute(f"DELETE FROM freelas WHERE rowid NOT IN (SELECT rowid FROM freelas ORDER BY rowid DESC LIMIT {6})")

banco.commit()
banco.close()