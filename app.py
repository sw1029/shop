from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)

from models import user, post, product
from routes import auth, board, product as product_routes, admin

app.register_blueprint(auth.bp)
app.register_blueprint(board.bp)
app.register_blueprint(product_routes.bp)
app.register_blueprint(admin.bp)

if __name__ == '__main__':
    app.run(debug=True)