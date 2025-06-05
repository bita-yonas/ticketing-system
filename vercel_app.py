from app import app as flask_app
import os

# Configure for Vercel
if os.environ.get('VERCEL_ENV') == 'production':
    # Use in-memory SQLite for Vercel
    flask_app.config['DATABASE'] = ':memory:'
    
    # Initialize the database
    with flask_app.app_context():
        from app import init_db
        init_db()

# Export the app for Vercel
app = flask_app 