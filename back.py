from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from PIL import Imagecd
import pytesseract as tess
import os

tess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    r = request

    # Convert a imagem binaria para o formato to uint8
    nparr = np.fromstring(r.data, np.uint8)
    
    # Decodifica a imagem
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # grava a imagem
    cv2.imwrite('.\\uploads\\{}'.format(filename), img)
    
    # extrai o texto da imagem
    texto = tess.image_to_string('.\\uploads\\{}'.format(filename), lang='por')

    # constroi o objeto de resposta
    response = {'message': texto}

    # remove a imagem do servidor                
    os.remove('.\\uploads\\{}'.format(filename))

    # Transforma o objeto response em um json para retornar ao cliente
    response_pickled = jsonpickle.encode(response)

    # retorno ao cliente
    return Response(response=response_pickled, status=200, mimetype="application/json")
