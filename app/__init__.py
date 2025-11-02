from flask import Flask
from app.extensions import db, login_manager, bcrypt
from flask_migrate import Migrate
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    
    # Set login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Đăng nhập để truy cập trang này.'

    # Import and register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app