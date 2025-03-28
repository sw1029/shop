from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from extensions import db, login_manager

from routes import auth, board, product as product_routes, admin, main, transfer, static_product

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(board.bp)
app.register_blueprint(product_routes.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(transfer.bp)           # ✅ 추가
app.register_blueprint(static_product.bp)     # ✅ 추가

if __name__ == '__main__':
    app.run(debug=True)
