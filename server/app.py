from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/lesson', methods=['GET', 'POST'])
def lesson():
    if request.method == 'GET':
        return json.dumps({'success':True})
    elif request.method == 'POST':
        return json.dumps({'success':True})


if __name__ == '__main__':
   app.run(debug=True)