from flask import Blueprint, jsonify, render_template, request, Response
from typing import Union
from . import TronsForm, full_translation_loop, translate_text

routes = Blueprint("routes", __name__)


@routes.route('/tronslote', methods=['POST'])
def receive_translation_data() -> Response:
    try:
        text = request.form['text_field']
        base_language = request.form['base_language']
        interim_languages = request.form.getlist('interim_langauges')
        print(interim_languages)
        retranslations = full_translation_loop(
            text, base_language, interim_languages)
        return jsonify(retranslations)

    except Exception as e:
        response = {'status': 'error', 'error_message': str(e)}
        return jsonify(response)


@routes.route('/testo')
def test_translation() -> Response:
    t = translate_text("look at that flying eggplant!", "en", "fr")
    return jsonify(t._asdict())


@routes.route("/", methods=['GET', 'POST'])
def make_homepage() -> Union[str, Response]:
    tronsform = TronsForm()
    if tronsform.validate_on_submit():
        # Access selected values using form.data
        input_text = tronsform.text_field.data
        interim_languages = tronsform.interim_languages.data
        base_language = tronsform.base_language.data
        retranslations = full_translation_loop(
            input_text, base_language, interim_languages)
        return jsonify(retranslations)

    return render_template(
        'home.html',
        tronsform=tronsform
    )
