from flask import Flask, request
from src.main import handler

app = Flask(__name__)


@app.route('/', methods=['POST'])
def entrypoint():
    return handler(request.data)
