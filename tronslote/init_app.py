import os
from dotenv import load_dotenv
from flask import Flask


def init_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    return app


app = init_app()
