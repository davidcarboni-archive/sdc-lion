import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import components
from keys import generate_key
from db import db
import public_keys

app = Flask(__name__)

# Enable cross-origin requests
CORS(app)


@app.route('/', methods=['GET'])
def info():
    return "This is: " + components.NAME


@app.route('/keys')
def keys():
    key_id = request.args.get("key_id")
    if key_id:
        print("Getting key ID " + repr(key_id))
        return jsonify(public_keys.get_key(key_id))
    print("Listing all keys")
    return jsonify(public_keys.list_keys())


@app.route('/chat')
def chat():
    return "I'm going to try to talk to " + repr(components.components)


if __name__ == '__main__':

    # Set up the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise the database
    db.app = app
    db.init_app(app)
    db.create_all()

    # Debugging
    if os.getenv('SQL_DEBUG') == 'true':
        import logging
        import sys

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    # Initialise a key-pair for this instance
    generate_key()

    port = int(os.environ.get('PORT', 5001))
    print("Running on port " + repr(port))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
