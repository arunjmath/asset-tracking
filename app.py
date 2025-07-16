from flask import Flask
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from routes.auth_routes import auth_bp
from routes.employee_routes import emp_bp
from routes.main_routes import main_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(emp_bp, url_prefix='/')
app.register_blueprint(main_bp, url_prefix='/main')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
