from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import numpy as np
import cv2 as cv
from PIL import Image
import pytesseract as tess
import os
import datetime as dt
import magic
import math
import re
from pytesseract import Output
from documento import documento

# tess.pytesseract.tesseract_cmd = r'C:/Program Files\\Tesseract-OCR\\tesseract'

app = Flask(__name__)

CORS(app)


@app.route("/upload", methods=["POST"])
def upload_file():
    r = request
    # verifica se foi enviado um arquivo com nome imagem
    if "image" not in r.files:
        # constroi o objeto de resposta
        response = {"message": "image not found"}
        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(
            response=response_pickled, status=400, mimetype="application/json"
        )

    file = request.files["image"]

    if file.content_type != "image/jpeg":
        # constroi o objeto de resposta
        response = {"message": "this extension is not allowed"}

        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(
            response=response_pickled, status=400, mimetype="application/json"
        )

    date = dt.datetime.now()
    filename = date.strftime("%m%d%Y%H%M%S") + ".jpeg"

    file.save("./uploads/{}".format(filename))

    # Carrega imagem para processar
    img = cv.imread("./uploads/{}".format(filename), cv.IMREAD_GRAYSCALE)

    # Redimensionamento
    img = cv.resize(img, None, fx=3, fy=3, interpolation=cv.INTER_CUBIC)

    # Limiarização
    img = cv.adaptiveThreshold(
        img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 5
    )

    # cv.imwrite("./uploads/{}".format(filename), th)

    # Encontrar contornos
    # img2 = cv.imread('./uploads/{}'.format(filename), 0)
    # contours, hierarchy = cv.findContours(th,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # cv.drawContours(img2, contours, -1, (255, 0, 0), 3)
    # cv.imshow('Contours', img2)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # img2 = cv.imread("./uploads/{}".format(filename), 0)

    d = tess.image_to_data(img, output_type=Output.DICT)

    doc = documento()

    pontos = [0, 0, 0, 0]

    date_pattern = "^[0-9]{2}/[0-9]{2}/[0-9]{4}$"
    cpf_pattern = "^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"

    n_boxes = len(d["text"])
    for i in range(n_boxes):
        if int(d["conf"][i]) > 60:
            if d["text"][i] == "REGISTRO":
                pontos[0] = d["left"][i]  # X
                pontos[1] = d["top"][i] - (math.trunc(d["height"][i] * 0.5))  # Y
                pontos[3] = (
                    d["left"][i] + (math.trunc(d["width"][i] * 7.8)) - pontos[0]
                )  # largura
            # altura
            if re.match(cpf_pattern, d["text"][i]):
                pontos[2] = d["top"][i] + d["height"][i] - pontos[1]
            if pontos[2] == 0 and d["text"][i] == "CPF:":
                pontos[2] = d["top"][i] + d["height"][i] - pontos[1]
            # largura
            if re.match(date_pattern, d["text"][i]):
                pontos[3] = (
                    d["left"][i] + (math.trunc(d["width"][i] * 0.72)) - pontos[0]
                )
            if pontos[3] == 0 and d["text"][i] == "NASCIMENTO:":
                pontos[3] = d["left"][i] + (math.trunc(d["width"][i] * 1.9)) - pontos[0]
            if pontos[3] == 0 and d["text"][i] == "PLASTIFICAR":
                pontos[3] = (
                    d["left"][i] + (math.trunc(d["width"][i] * 0.95)) - pontos[0]
                )
            if pontos[3] == 0 and d["text"][i] == "NACIONAL":
                pontos[3] = (
                    d["left"][i] + (math.trunc(d["width"][i] * 0.72)) - pontos[0]
                )

    if pontos[0] == 0 or pontos[1] == 0 or pontos[2] == 0 or pontos[3] == 0:
        # constroi o objeto de resposta
        response = {"message": "shit boy", "pontos": pontos}

        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(
            response=response_pickled, status=400, mimetype="application/json"
        )

    crop_img = img[pontos[1] : pontos[1] + pontos[2], pontos[0] : pontos[0] + pontos[3]]

    # Remoção de ruido
    crop_img = cv.fastNlMeansDenoising(crop_img, 1.0, 7, 21)

    # Limiarização
    crop_img = cv.adaptiveThreshold(
        crop_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 41, 11
    )

    # Suavização de bordas
    crop_img = cv.GaussianBlur(crop_img, (5, 5), 1)

    height, width = crop_img.shape

    # 0:0:0:0
    # y:altura, x:largura
    # pontoInicialY:pontoFinalY, pontoInicialX:pontoFinalX

    imgRg = crop_img[
        0 : math.trunc(height * 0.09),
        math.trunc(width * 0.23) : math.trunc(width * 0.55),
    ]

    doc.setRg(tess.image_to_string(imgRg))

    imgExpedicao = crop_img[
        0 : math.trunc(height * 0.09), math.trunc(width * 0.86) : width
    ]

    doc.setExpedicao(tess.image_to_string(imgExpedicao))

    imgNome = crop_img[
        math.trunc(height * 0.09) : math.trunc(height * 0.22),
        math.trunc(width * 0.09) : width,
    ]

    doc.setNome(tess.image_to_string(imgNome, lang="por"))

    imgPai = crop_img[
        math.trunc(height * 0.26) : math.trunc(height * 0.35),
        math.trunc(width * 0.118) : width,
    ]

    doc.setPai(tess.image_to_string(imgPai, lang="por"))

    imgMae = crop_img[
        math.trunc(height * 0.35) : math.trunc(height * 0.42),
        math.trunc(width * 0.118) : width,
    ]

    doc.setMae(tess.image_to_string(imgMae, lang="por"))

    imgNaturalidade = crop_img[
        math.trunc(height * 0.46) : math.trunc(height * 0.55),
        math.trunc(width * 0.20) : math.trunc(width * 0.54),
    ]
    # Redimensionamento
    imgNaturalidade = cv.resize(
        imgNaturalidade, None, fx=5, fy=5, interpolation=cv.INTER_CUBIC
    )

    naturalidade = tess.image_to_string(imgNaturalidade, lang="por").strip()

    doc.setNaturalidade(naturalidade[0 : len(naturalidade) - 3])
    doc.setUf(naturalidade[len(naturalidade) - 2 : len(naturalidade)])

    print(doc.getNaturalidade)
    print(doc.getUf)

    imgNascimento = crop_img[
        math.trunc(height * 0.46) : math.trunc(height * 0.55),
        math.trunc(width * 0.86) : width,
    ]

    cv.imshow("cropped", crop_img)
    cv.waitKey(0)

    # constroi o objeto de resposta
    response = {"message": texto}

    # remove a imagem do servidor
    # os.remove('./uploads/{}'.format(filename))
    # Transforma o objeto response em um json para retornar ao cliente
    response_pickled = jsonpickle.encode(response)

    print(doc)

    # retorno ao cliente
    return Response(response=response_pickled, status=200, mimetype="application/json")
