import os

import pytest
import requests
from dotenv import load_dotenv
from flask_testing import TestCase
from google.cloud import translate

from app import app
from tronslote.src import extract_translation, make_credentials


@pytest.fixture
def gunicorn_server():
    import subprocess
    import time

    command = [
        "gunicorn",
        "--config",
        "gunicorn_config.py",
        "--env",
        "FLASK_ENV=test",
        "app:app",
    ]
    process = subprocess.Popen(command)

    time.sleep(2)

    yield process
    process.terminate()
    process.wait()


def test_guni(gunicorn_server):
    response = requests.get("http://127.0.0.1:5000/")
    assert response.status_code == 200


class TestFolio(TestCase):
    def create_app(self):
        return app

    def test_home_route(self):
        response = self.client.get("/")
        self.assert200(response)


def test_credentials():
    os.environ['APP_DIR'] = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    load_dotenv()
    credentials = make_credentials()
    client = translate.TranslationServiceClient(credentials=credentials)
    location = "global"
    parent = f"projects/{os.environ['PROJECT_ID']}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": ["The farmer had never been faced with such an intelligent chicken."],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en",
            "target_language_code": "fr",
        }
    )

    assert extract_translation(response) == "Le fermier n’avait jamais été confronté à un poulet aussi intelligent."
