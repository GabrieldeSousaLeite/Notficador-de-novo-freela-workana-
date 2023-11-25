from selenium import webdriver
import time
from PIL import Image
from itertools import zip_longest
import os
import pytesseract
from winotify import Notification, audio
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.action_chains import ActionChains

def dividir_imagem_verticalmente(imagem):
    largura, altura = imagem.size
    altura_parte = altura // 3

    partes = []
    for i in range(3):
        y1 = i * altura_parte
        y2 = (i + 1) * altura_parte

        parte = imagem.crop((0, y1, largura, y2))
        partes.append(parte)

    return partes

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options)

# Navega para a página desejada
driver.get("https://www.workana.com/jobs?category=it-programming&has_few_bids=1&language=pt&publication=1d&skills=python&subcategory=web-development%2Cdata-science-1%2Cdesktop-apps")

#actions = ActionChains(driver)
#actions.move_by_offset(600, 850).click().perform()

time.sleep(2)

driver.find_element('xpath',"//button[text()='Aceitar todos os cookies']").click()
driver.find_element('xpath',"//span[contains(@class,'wk2-icon')]").click()
driver.execute_script("document.body.style.zoom = '0.75';")
driver.execute_script("document.body.style.textTransform = 'uppercase';")
driver.execute_script("document.body.style.fontWeight = 'bold';")
driver.set_window_size(480, 1080)
excluir1 = driver.find_element('xpath',"//nav[contains(@class,'navbar')]")
excluir2 = driver.find_elements('xpath',"//a[contains(@class,'btn')]")
excluir3 = driver.find_elements('xpath',"//div[contains(@class,'skills')]")
driver.execute_script("arguments[0].remove()", excluir1)

for item2, item3 in zip_longest(excluir2, excluir3, fillvalue=None):
    if item2:
        driver.execute_script("arguments[0].remove()", item2)
    if item3:
        driver.execute_script("arguments[0].remove()", item3)

driver.execute_script("window.scrollBy(0, 566)")

diretorio_atual = os.getcwd()
pasta_imagens = os.path.join(diretorio_atual, 'imagens')

if not os.path.exists(pasta_imagens):
    os.makedirs(pasta_imagens)

driver.save_screenshot("imagens\\screenshot.png")

driver.quit()

imagem = Image.open("imagens\\screenshot.png")

partes = dividir_imagem_verticalmente(imagem)

for i, parte in enumerate(partes):
    parte.save(f"imagens\\parte{i+1}.png")


if os.path.exists("imagens\\screenshot.png"):
    os.remove("imagens\\screenshot.png")
    print("Arquivo excluído com sucesso.")

else:
    print("O arquivo não existe.")

import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Gabriel\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

for c in range(3):

    image = Image.open(f"imagens\\parte{str(c+1)}.png")

    texto = pytesseract.image_to_string(image).lower()

    linhas = texto.splitlines()

    resumo_linhas = linhas[0:3]

    resumo = ""

    for linha in linhas:
        resumo += linha + "\n"

    notificação = Notification(app_id='Novo freela', title='Novo freela', msg=resumo, duration= 'short')
    notificação.set_audio(audio.Mail, loop=False)
    notificação.show()

    time.sleep(5)

