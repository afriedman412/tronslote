import os
from collections import namedtuple
from typing import Tuple, List, Dict, Any

from flask_wtf import FlaskForm
from google.cloud import translate
from google.oauth2 import service_account
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField

Language: Tuple[str, str, bool] = namedtuple(
    'Language', ['name', 'code', 'base_enabled'])
Translation: Tuple[str] = namedtuple("Translation", [
    "input_language",
    "output_language",
    "input_text",
    "output_text"
])

LANGUAGES = [
    Language(name, code, base_enabled) for name, code, base_enabled in [
        ('English', 'en', True),
        ('French', 'fr', True),
        ('Spanish', 'es', True),
        ('Dutch', 'nl', True),
        ('Hebrew', 'he', False),
        ('Arabic', 'ar', False),
        ('Farsi', 'fa', False),
        ('Afrikaans', 'af', False)
    ]
]


class TronsForm(FlaskForm):
    interim_languages = LANGUAGES
    base_languages = [lang for lang in LANGUAGES if lang.base_enabled]
    text_field = StringField('Input String')
    input_language = SelectField('Select Input Language', choices=[
                                 (lang.code, lang.name) for lang in base_languages])
    interim_languages = SelectMultipleField('Select Interim Languages', choices=[
                                            (lang.code, lang.name) for lang in interim_languages])
    base_language = SelectField('Select Output Language', choices=[
                                (lang.code, lang.name) for lang in base_languages])
    submit = SubmitField('Submit')


def extract_translation(translation: Any) -> Any:
    return translation.translations[0].translated_text


def full_translation_loop(
        input_text: str,
        base_language: str,
        interim_languages: list[str],
) -> List[Dict[str, str]]:
    translations = []
    for lang in interim_languages:
        translated = translate_text(input_text, base_language, lang)
        translations.append(translated.output_text)

    retranslations = []
    for text, lang in zip(translations, interim_languages):
        retranslated = translate_text(text, lang, base_language)
        retranslations.append(
            dict(
                zip(
                    [
                        'input_language',
                        'input_text',
                        'interim_language',
                        'interim_text',
                        'output_text'
                    ],
                    [
                        base_language,
                        input_text,
                        lang,
                        text,
                        retranslated.output_text
                    ]
                )
            )
        )

    return retranslations


def translate_text(
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    input_language_code: str = "en-US",
    output_language_code: str = "en-US"
) -> Translation:
    """Translating Text.

    later: https://cloud.google.com/translate/docs/advanced/batch-translation
    """
    credentials = service_account.Credentials.from_service_account_file(
        os.path.join(os.getenv("APP_DIR"), os.getenv("GOOGLE_APP_CREDENTIALS_FILE")),
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    client = translate.TranslationServiceClient(credentials=credentials)
    location = "global"
    parent = f"projects/{os.getenv('PROJECT_ID')}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": input_language_code,
            "target_language_code": output_language_code,
        }
    )

    return Translation(input_language_code, output_language_code, text, extract_translation(response))
