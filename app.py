from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handler():
    return 'Fuck yeah, Docker!'
