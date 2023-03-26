from flask import Flask, request
from src.main import handler

app = Flask(__name__)


@app.route('/', methods=['POST'])
def entrypoint():
    event = request.args.get('event')
    return handler(event)
