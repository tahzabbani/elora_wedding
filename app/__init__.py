from flask import Flask
app = Flask(__name__)
from app import views

app.config['TEMPLATES_AUTO_RELOAD'] = True