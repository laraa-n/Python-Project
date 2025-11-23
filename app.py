from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Filme, Cliente, Emprestimo
from datetime import datetime

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
            return redirect('/')
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

@app.route('/emprestimos')
@login_required
def emprestimos_lista():
    emprestimos = Emprestimo.query.all()
    return render_template("emprestimos/lista.html", emprestimos=emprestimos, title="Empréstimos")

@app.route('/emprestimos/adicionar', methods=['GET', 'POST'])
@login_required
def emprestimos_adicionar():
    clientes = Cliente.query.all()
    filmes = Filme.query.filter(Filme.quantidade > 0).all()  # somente filmes disponíveis

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_filme = request.form['id_filme']
        data_retirada = request.form['data_retirada']
        data_devolucao = request.form['data_devolucao']

        # Criar empréstimo
        novo = Emprestimo(
            id_cliente=id_cliente,
            id_filme=id_filme,
            data_retirada=data_retirada,
            data_devolucao=data_devolucao,
            devolvido=False
        )

        # Atualizar estoque
        filme = Filme.query.get(id_filme)
        filme.quantidade -= 1

        db.session.add(novo)
        db.session.commit()

        return redirect('/emprestimos')

    return render_template("emprestimos/adicionar.html", clientes=clientes, filmes=filmes, title="Novo Empréstimo")

@app.route('/emprestimos/devolver/<int:id_emprestimo>')
@login_required
def emprestimos_devolver(id_emprestimo):
    emp = Emprestimo.query.get(id_emprestimo)
    emp.devolvido = True

    # Atualiza estoque do filme
    filme = Filme.query.get(emp.id_filme)
    filme.quantidade += 1

    db.session.commit()
    return redirect('/emprestimos')

@app.route('/emprestimos/excluir/<int:id_emprestimo>')
@login_required
def emprestimos_excluir(id_emprestimo):
    emp = Emprestimo.query.get(id_emprestimo)

    # Devolver o filme automaticamente se o empréstimo não foi devolvido
    if not emp.devolvido:
        filme = Filme.query.get(emp.id_filme)
        filme.quantidade += 1

    db.session.delete(emp)
    db.session.commit()

    return redirect('/emprestimos')

if __name__ == "__main__":
    app.run(debug=True)