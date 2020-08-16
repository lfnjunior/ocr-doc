from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from PIL import Image
import pytesseract as tess
import os

# tess.pytesseract.tesseract_cmd = r'C:/Program Files\\Tesseract-OCR\\tesseract'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    print('0')
    file = request.files['image']

    filename = file.filename

    print('1')
    if not allowed_file(filename):
        # constroi o objeto de resposta
        response = {'message': "this extension is not allowed"}

        # Transforma o objeto response em um json para retornar ao cliente
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=400, mimetype="application/json")

    
    print('3')
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
