from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Filme, Cliente

app = Flask(__name__)
app.secret_key = "chave_super_secreta_aqui"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
def home():
    return render_template("home.html", title="Locadora")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(username=username, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html", title="Cadastro")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        user = Usuario.query.filter_by(username=username).first()

        if user and check_password_hash(user.senha, senha):
            session['usuario'] = username
            return redirect('/area-protegida')
        else:
            return "Usuário ou senha incorretos!"

    return render_template("login.html", title="Login")

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/area-protegida')
def area_protegida():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return f"<h1>Bem-vindo {session['usuario']}!</h1>"


@app.route('/filmes')
@login_required
def filmes_lista():
    filmes = Filme.query.all()
    return render_template("filmes/lista.html", filmes=filmes, title="Filmes")



@app.route('/filmes/adicionar', methods=['GET', 'POST'])
@login_required
def filmes_adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        ano = request.form['ano']
        quantidade = request.form['quantidade']

        novo = Filme(
            titulo=titulo,
            genero=genero,
            ano=ano,
            quantidade=quantidade
        )
        db.session.add(novo)
        db.session.commit()

        return redirect('/filmes')

    return render_template("filmes/adicionar.html", title="Adicionar Filme")


 
@app.route('/filmes/editar/<int:id_filme>', methods=['GET', 'POST'])
@login_required
def filmes_editar(id_filme):
    filme = Filme.query.get(id_filme)

    if request.method == 'POST':
        filme.titulo = request.form['titulo']
        filme.genero = request.form['genero']
        filme.ano = request.form['ano']
        filme.quantidade = request.form['quantidade']

        db.session.commit()
        return redirect('/filmes')

    return render_template("filmes/editar.html", filme=filme, title="Editar Filme")


@app.route('/filmes/excluir/<int:id_filme>')
@login_required
def filmes_excluir(id_filme):
    filme = Filme.query.get(id_filme)
    db.session.delete(filme)
    db.session.commit()
    return redirect('/filmes')

@app.route('/clientes')
@login_required
def clientes_lista():
    clientes = Cliente.query.all()
    return render_template("clientes/lista.html", clientes=clientes, title="Clientes")

@app.route('/clientes/adicionar', methods=['GET', 'POST'])
@login_required
def clientes_adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        novo = Cliente(
            nome=nome,
            telefone=telefone,
            email=email
        )
        db.session.add(novo)
        db.session.commit()

        return redirect('/clientes')

    return render_template("clientes/adicionar.html", title="Adicionar Cliente")

@app.route('/clientes/editar/<int:id_cliente>', methods=['GET', 'POST'])
@login_required
def clientes_editar(id_cliente):
    cliente = Cliente.query.get(id_cliente)

    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.telefone = request.form['telefone']
        cliente.email = request.form['email']

        db.session.commit()
        return redirect('/clientes')

    return render_template("clientes/editar.html", cliente=cliente, title="Editar Cliente")

@app.route('/clientes/excluir/<int:id_cliente>')
@login_required
def clientes_excluir(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/clientes')

if __name__ == "__main__":
    app.run(debug=True)