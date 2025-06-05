from flask import Flask, render_template, jsonify, session, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-123')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/debug')
def debug():
    return jsonify({
        "status": "running",
        "environment": os.environ.get('FLASK_ENV'),
        "vercel": os.environ.get('VERCEL_ENV'),
        "templates_folder": app.template_folder
    })

if __name__ == '__main__':
    app.run() 