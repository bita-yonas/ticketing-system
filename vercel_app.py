from flask import Flask, render_template, jsonify, session, redirect, url_for
import os
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-123')
app.config['DATABASE'] = ':memory:'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode())
    
    # Create admin user
    admin = db.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin:
        db.execute(
            'INSERT INTO users (username, email, password, is_admin, role) VALUES (?, ?, ?, ?, ?)',
            ('admin', 'bitayonas@gmail.com', generate_password_hash('Admin@2024!'), 1, 'admin')
        )
        db.commit()

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
        "database": app.config['DATABASE'],
        "templates_folder": app.template_folder
    })

# Initialize the app
with app.app_context():
    from flask import g
    init_db()

if __name__ == '__main__':
    app.run() 