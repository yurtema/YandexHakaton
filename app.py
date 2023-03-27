from flask import Flask, request
from src.main import handler
import json


if __name__ == '__main__':

    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def entrypoint():

        event = json.loads(request.data.decode('utf8'))

        return handler(event)
