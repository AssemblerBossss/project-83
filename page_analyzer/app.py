from flask import Flask
from flask import (
    render_template,
    redirect,
    request,
)

app = Flask(__name__)

@app.get('/')
def index():
    return {'index.html': 1}