from flask import Flask, jsonify
import sys
import traceback

# Create a simple test app first to verify basic functionality
app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Now try to import and initialize the main app
        from app import app as main_app
        return "Flask app is working! Now we can add more functionality."
    except Exception as e:
        error_info = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print("Error details:", error_info, file=sys.stderr)
        return jsonify(error_info), 500

@app.route('/debug')
def debug():
    import os
    debug_info = {
        "python_version": sys.version,
        "environment_vars": dict(os.environ),
        "sys_path": sys.path
    }
    return jsonify(debug_info)

if __name__ == '__main__':
    app.run() 