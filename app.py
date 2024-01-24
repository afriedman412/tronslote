import os
from flask import url_for
from tronslote.src.routes import routes
from tronslote.init_app import app

app.register_blueprint(routes)
app.config['SECRET_KEY'] = 'your_secret_key'  # for WTForms, not important rn
os.environ['APP_DIR'] = os.path.abspath(os.path.dirname(__file__))


@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


if __name__ == "__main__":
    app.run()
