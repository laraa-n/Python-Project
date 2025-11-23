from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Filme(db.Model):
    __tablename__ = 'filmes'
    id_filme = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    quantidade = db.Column(db.Integer, default=1)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id_emprestimo = db.Column(db.Integer, primary_key=True)
    
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'))
    id_filme = db.Column(db.Integer, db.ForeignKey('filmes.id_filme'))

    data_retirada = db.Column(db.String(10))     # simplificado
    data_devolucao = db.Column(db.String(10))
    devolvido = db.Column(db.Boolean, default=False)

    cliente = db.relationship("Cliente", backref="emprestimos")
    filme = db.relationship("Filme", backref="emprestimos")

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)