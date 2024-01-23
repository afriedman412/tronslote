from flask import Flask, url_for, request, jsonify, render_template
from tronslote.src import LANGUAGES
from tronslote.src.routes import routes
from tronslote.init_app import app

app.register_blueprint(routes)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')

if __name__ == "__main__":
    app.run()
