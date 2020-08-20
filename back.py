from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import numpy as np
import cv2
from PIL import Image
import pytesseract as tess
import os
import datetime as dt
import magic


# tess.pytesseract.tesseract_cmd = r'C:/Program Files\\Tesseract-OCR\\tesseract'

app = Flask(__name__) 

CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    r = request
    # verifica se foi enviado um arquivo com nome imagem
    if 'image' not in r.files:
        # constroi o objeto de resposta
        response = {'message': "image not found"}

        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=400, mimetype="application/json")

    file = request.files['image']

    if file.content_type != 'image/jpeg':
        # constroi o objeto de resposta
        response = {'message': "this extension is not allowed"}
    
        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=400, mimetype="application/json")

    date = dt.datetime.now()
    filename = date.strftime("%m%d%Y%H%M%S")+".jpeg"

    file.save('./uploads/{}'.format(filename))

    print('4')
    texto = tess.image_to_string('./uploads/{}'.format(filename), lang='por')

    # constroi o objeto de resposta
    response = {'message': texto}

    # remove a imagem do servidor                
    os.remove('./uploads/{}'.format(filename))

    # Transforma o objeto response em um json para retornar ao cliente
    response_pickled = jsonpickle.encode(response)

    # retorno ao cliente
    return Response(response=response_pickled, status=200, mimetype="application/json")
