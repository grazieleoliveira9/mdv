from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

from app import routes  # Importe DEPOIS da criação do app