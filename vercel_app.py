import sys
import traceback
from flask import jsonify

try:
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
            
            # Seed initial data if needed
            from app import get_db
            db = get_db()
            
            # Check if admin user exists
            admin = db.execute(
                'SELECT * FROM users WHERE username = ?', ('admin',)
            ).fetchone()
            
            if not admin:
                from werkzeug.security import generate_password_hash
                # Create admin user
                db.execute(
                    'INSERT INTO users (username, email, password, is_admin, role) VALUES (?, ?, ?, ?, ?)',
                    ('admin', 'bitayonas@gmail.com',
                     generate_password_hash('Admin@2024!'), 1, 'admin')
                )
                db.commit()

    # Error handling
    @flask_app.errorhandler(500)
    def handle_500_error(e):
        original = getattr(e, "original_exception", None)
        
        # Log the error
        error_details = {
            "error": str(e),
            "original_error": str(original) if original else None,
            "traceback": traceback.format_exc()
        }
        
        print("Error details:", error_details, file=sys.stderr)
        
        return jsonify(error="Internal server error", details=error_details), 500

    app = flask_app

except Exception as e:
    print("Initialization error:", str(e), file=sys.stderr)
    print("Traceback:", traceback.format_exc(), file=sys.stderr)
    
    def create_error_app():
        from flask import Flask
        error_app = Flask(__name__)
        
        @error_app.route('/')
        def error_handler():
            return jsonify(
                error="Application initialization failed",
                details=str(e),
                traceback=traceback.format_exc()
            ), 500
        
        return error_app
    
    app = create_error_app() 