from flask import Blueprint, jsonify, render_template, request, Response
from typing import Union
from . import TronsForm, full_translation_loop, translate_text

routes = Blueprint("routes", __name__)


@routes.route('/tronslote', methods=['POST'])
def receive_translation_data() -> Response:
    tronsform = TronsForm(request.form)
    if tronsform.validate():
        try:
            input_text = tronsform.text_field.data
            interim_languages = tronsform.interim_languages.data
            base_language = tronsform.base_language.data
            retranslations = full_translation_loop(
                input_text, base_language, interim_languages)
            return jsonify(retranslations)

        except Exception as e:
            response = {'status': 'error', 'error_message': str(e), 'content': tronsform}
            return jsonify(response)
    else:
        return request.form


@routes.route('/testo')
def test_translation() -> Response:
    t = translate_text("look at that flying eggplant!", "en", "fr")
    return jsonify(t._asdict())

@routes.route("/api/submit", methods=['POST'])
def trons_endpoint() -> Response:
    input_dict = request.get_json()
    input_text = input_dict['input_text']
    interim_languages = input_dict['interim_langs']
    base_language = input_dict['base_lang']
    retranslations = full_translation_loop(
        input_text, base_language, interim_languages)
    return jsonify(retranslations)
    return request.data


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
