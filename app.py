from flask import Flask, request
from src.main import handler
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def entrypoint():

    event = json.dumps(json.loads(request.data.decode('utf8')), indent=2, sort_keys=False)

    return handler(event)
