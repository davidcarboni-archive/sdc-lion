import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import components
import keys

app = Flask(__name__)

# Enable cross-origin requests
CORS(app)


@app.route('/', methods=['GET'])
def info():
    return "This is: " + components.NAME


@app.route('/keys')
def public_keys():
    return jsonify({"key_id": 1, "key": keys.public_key()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
