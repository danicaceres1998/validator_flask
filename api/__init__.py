import sentry_sdk
from os import environ
from flask import Flask
from flask_restful import Api
from api.controller.validator import Validator
from sentry_sdk.integrations.flask import FlaskIntegration

SAMPLE_RATE = 0.1
sentry_sdk.init(
    environ['SENTRY_KEY'],
    integrations=[FlaskIntegration()],
    traces_sample_rate=SAMPLE_RATE,
)

# API
app = Flask(__name__)
api = Api(app)

# -> Routes
api.add_resource(Validator, '/phones')
