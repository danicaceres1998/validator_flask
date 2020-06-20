from flask import Flask, jsonify
from flask_restful import Api
from controller.validator import Validator

app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(Validator, '/phones')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False)