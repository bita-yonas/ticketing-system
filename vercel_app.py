from flask import Flask, render_template, jsonify, session, redirect, url_for
import os
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-123')

# Initialize Firebase Admin SDK with credentials from environment variables
if os.environ.get('FIREBASE_PROJECT_ID'):
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
        "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.environ.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
        "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
    })
    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        # App already initialized
        pass

# Configure Firebase client-side settings
app.config.update(
    FIREBASE_API_KEY=os.environ.get('FIREBASE_API_KEY'),
    FIREBASE_AUTH_DOMAIN=os.environ.get('FIREBASE_AUTH_DOMAIN'),
    FIREBASE_PROJECT_ID=os.environ.get('FIREBASE_PROJECT_ID'),
    FIREBASE_STORAGE_BUCKET=os.environ.get('FIREBASE_STORAGE_BUCKET'),
    FIREBASE_MESSAGING_SENDER_ID=os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
    FIREBASE_APP_ID=os.environ.get('FIREBASE_APP_ID')
)

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
        "templates_folder": app.template_folder,
        "firebase_initialized": bool(firebase_admin._apps),
        "firebase_config": {
            "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
            "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
            "auth_domain": os.environ.get('FIREBASE_AUTH_DOMAIN')
        }
    })

if __name__ == '__main__':
    app.run() 