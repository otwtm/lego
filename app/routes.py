from flask import render_template, url_for
from app import app, dash_app


@app.route("/")
@app.route("/index")
def app1_template():
    return render_template(url_for('dash_app'), dash_url = '/')


"""
def index():
    return render_template(url_for('index'))
"""


"""
@app.route('/dash_app')
"""