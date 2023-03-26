from flask import Flask, request
from src.main import handler
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def entrypoint():
    return handler(request.data)
