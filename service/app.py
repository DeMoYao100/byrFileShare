from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from routes import api  # api 是在 routes.py 中定义的 Blueprint 对象
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)
app.config['SECRET_KEY'] = 'your-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

if __name__=='__main__':
    app.run(debug=True)
