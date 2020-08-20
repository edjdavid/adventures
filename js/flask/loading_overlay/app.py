from flask import Flask, render_template, redirect
from time import sleep
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/form')
def form():
    return render_template('form.jinja', ran=randint(10000, 20000))

@app.route('/slow', methods=['GET', 'POST'])
def slow():
    sleep(1)
    return redirect('/form')

@app.route('/escape')
def escape():
    return "Escaped the iframe"

if __name__ == "__main__":
    app.run(debug=True)