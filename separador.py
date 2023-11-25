from PIL import Image
import os

def dividir_imagem_verticalmente(imagem):
    largura, altura = imagem.size
    altura_parte = altura // 3  # Altura de cada parte igual

    partes = []
    for i in range(3):
        # Calcula as coordenadas de recorte para cada parte
        y1 = i * altura_parte
        y2 = (i + 1) * altura_parte

        # Recorta a parte da imagem
        parte = imagem.crop((0, y1, largura, y2))
        partes.append(parte)

    return partes

# Carrega a imagem
imagem = Image.open("imagens\\screenshot.png")

# Divide a imagem em partes
partes = dividir_imagem_verticalmente(imagem)

# Salva cada parte como uma imagem separada
for i, parte in enumerate(partes):
    parte.save(f"imagens\\parte{i+1}.png")


# Verifica se o arquivo existe
if os.path.exists("imagens\\screenshot.png"):
    # Remove o arquivo definitivamente
    os.remove("imagens\\screenshot.png")
    print("Arquivo excluído com sucesso.")
else:
    print("O arquivo não existe.")