from flask import Flask
from src.main import handler

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handler(event, context):
    return handler(event, context)
