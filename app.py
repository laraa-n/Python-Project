from flask import Flask
from models import db, Filme, Cliente, Emprestimo, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chaveSecreta"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Sistema de Locadora funcionando!"

if _name_ == '_main_':
    app.run(debug=True)