from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Gabriel\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

for c in range(3):
    # Abre a imagem
    image = Image.open(f"imagens\\parte{str(c+1)}.png")

    # Extrai o texto da imagem usando o Tesseract OCR
    texto = pytesseract.image_to_string(image)

    # Exibe o texto extraído
    print(texto, '\n\n')