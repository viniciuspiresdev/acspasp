from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    
# Criação das tabelas
with app.app_context():
    db.create_all()

# Adicione esta nova rota para a página de sucesso de edição
@app.route("/edicao_sucesso/<int:id>")
def edicao_sucesso(id):
    return render_template("edicao_sucesso.html", id=id)

# Adicione esta nova rota para exibir o formulário de edição
@app.route("/editar_registro/<int:id>")
def editar_registro(id):
    # Busque o registro no banco de dados
    registro = Pessoa.query.get(id)

    # Renderize o formulário de edição
    return render_template("editar_registro.html", registro=registro)

# Atualize a rota para processar o formulário de edição
@app.route("/salvar_edicao/<int:id>", methods=["POST"])
def salvar_edicao(id):
    # Busque o registro no banco de dados
    registro = Pessoa.query.get(id)

    if registro:
        # Atualize os dados do registro com os dados do formulário
        registro.nome = request.form["nome"]
        registro.idade = request.form["idade"]

        # Salve as alterações no banco de dados
        db.session.commit()

        # Redirecione para a página de exibição de registros
        return redirect("/exibir_registro/" + str(registro.id))

    # Redirecione para a página de exibição de registros se o registro não for encontrado
    return redirect("/exibir_registro/" + str(id))


# Adicione uma nova rota para excluir registros
@app.route("/excluir_registro/<int:id>")
def excluir_registro(id):
    # Tente excluir o registro do banco de dados
    try:
        registro = Pessoa.query.get(id)
        if registro:
            db.session.delete(registro)
            db.session.commit()
            return render_template("exclusao_sucesso.html")
        else:
            return render_template("exclusao_sucesso.html")  # Mostrar a página de sucesso mesmo se o registro não for encontrado
    except Exception as e:
        print(f"Erro ao excluir registro: {str(e)}")
        # Caso ocorra um erro, você pode personalizar a resposta aqui
        return render_template("exclusao_sucesso.html")


# Atualize a rota para consultar registros
@app.route("/consultar_registro", methods=["GET"])
def consultar_registros():
    # Obtenha os parâmetros da consulta
    id_param = request.args.get("id")
    nome_param = request.args.get("nome")

    # Inicialize a variável de registro
    registro = None

    # Tente buscar o registro no banco de dados
    try:
        if id_param:
            registro = Pessoa.query.filter_by(id=id_param).first()
        elif nome_param:
            registro = Pessoa.query.filter_by(nome=nome_param).first()
    except Exception as e:
        print(f"Erro ao consultar registros: {str(e)}")
        # Caso ocorra um erro, você pode personalizar a resposta aqui
    return render_template("consultar_registro.html", registro=registro)

# Rota para listar todas as pessoas
@app.route("/")
def listar_pessoa():
    with app.app_context():
        pessoas = Pessoa.query.all()
    return render_template("listar_pessoa.html", pessoas=pessoas)

# Rota para adicionar uma nova pessoa
@app.route("/adicionar_pessoa", methods=["GET", "POST"])
def adicionar_pessoa():
    if request.method == "POST":
        nome = request.form['nome']
        idade = request.form['idade']
        with app.app_context():
            nova_pessoa = Pessoa(nome=nome, idade=idade)
            db.session.add(nova_pessoa)
            db.session.commit()
        return redirect("/")
    return render_template("adicionar_pessoa.html")

# Rota para landing page
@app.route("/landing_page")
def landing_page():
    return render_template("landing_page.html")

# Rota para editar uma pessoa existente
@app.route("/editar_pessoa/<int:id>", methods=["GET", "POST"])
def editar_pessoa(id):
    with app.app_context():
        pessoa = Pessoa.query.get(id)
    if request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.idade = request.form['idade']
        with app.app_context():
            db.session.commit()
        return redirect("/")
    return render_template("editar_pessoa.html", pessoa=pessoa)

# Rota para excluir uma pessoa
@app.route("/excluir_pessoa/<int:id>")
def excluir_pessoa(id):
    with app.app_context():
        pessoa = Pessoa.query.get(id)
        db.session.delete(pessoa)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)