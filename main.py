from flask import Flask, request

app = Flask(__name__)


@app.route('/vectorizer', methods=['GET'])
def vectorizer():
    data = request.get_json()
