# app/routes.py

from flask import render_template
from app import app

@app.route('/index')
def login():
    return render_template('index.html')
