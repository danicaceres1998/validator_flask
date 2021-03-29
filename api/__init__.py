from flask import Flask, jsonify
from flask_restful import Api
from api.controller.validator import Validator

# API
app = Flask(__name__)
api = Api(app)

# -> Routes
api.add_resource(Validator, '/phones')
