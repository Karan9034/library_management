import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)

    from library_management.main.routes import main
    from library_management.books.routes import books
    from library_management.members.routes import members
    from library_management.transactions.routes import transactions
    app.register_blueprint(main)
    app.register_blueprint(books)
    app.register_blueprint(members)
    app.register_blueprint(transactions)

    return app