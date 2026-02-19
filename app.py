import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="membro") 
    
class Ministerio(db.Model):
    __tablename__ = "ministerios"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    descricao = db.Column(db.String(300), nullable=True)

@app.get("/")
def home():
    return render_template("home.html")

# ROTAS - PESSOA

@app.get("/pessoas")
def listar_pessoas():
    pessoas = Pessoa.query.all()
    return render_template("pessoas/list.html", pessoas = pessoas)

@app.get("/pessoas/cadastro")
def mostrar_cadastro_pessoa():
    return render_template("pessoas/form.html", pessoa = None)

@app.post("/pessoas/cadastro")
def salvar_cadastro_pessoa():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    status = request.form.get("status") or "membro"
    nova_pessoa = Pessoa(
        nome = nome,
        telefone = telefone,
        email = email,
        status = status
    )
    db.session.add(nova_pessoa)
    db.session.commit()
    return redirect(url_for("listar_pessoas"))

@app.get("/pessoas/<int:id>/editar")
def mostrar_edicao_pessoa(id):
    pessoa = db.session.get(Pessoa, id)
    return render_template("pessoas/form.html", pessoa = pessoa)

@app.post("/pessoas/<int:id>/editar")
def salvar_edicao_pessoa(id):
    pessoa = db.session.get(Pessoa, id)
    pessoa.nome = request.form.get("nome")
    pessoa.telefone = request.form.get("telefone")
    pessoa.email = request.form.get("email")
    pessoa.status = request.form.get("status")
    db.session.commit()
    return redirect(url_for("listar_pessoas"))

@app.post("/pessoas/<int:id>/excluir")
def excluir_pessoa(id):
    pessoa = db.session.get(Pessoa, id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for("listar_pessoas"))

# ROTAS - MINISTÉRIOS

@app.get("/ministerios")
def listar_ministerios():
    ministerios = Ministerio.query.all()
    return render_template("ministerios/list.html", ministerios = ministerios)

@app.get("/ministerios/cadastro")
def mostrar_cadastro_ministerio():
    return render_template("ministerios/form.html", ministerio = None)

@app.post("/ministerios/cadastro")
def salvar_cadastro_ministerio():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    novo_ministerio = Ministerio(
        nome = nome,
        descricao = descricao
    )
    db.session.add(novo_ministerio)
    db.session.commit()
    return redirect(url_for("listar_ministerios"))

@app.get("/ministerios/<int:id>/editar")
def mostrar_edicao_ministerio(id):
    ministerio = db.session.get(Ministerio, id)
    return render_template("ministerios/form.html", ministerio = ministerio)

@app.post("/ministerios/<int:id>/editar")
def salvar_edicao_ministerio(id):
    ministerio = db.session.get(Ministerio, id)
    ministerio.nome = request.form.get("nome")
    ministerio.descricao = request.form.get("descricao")
    db.session.commit()
    return redirect(url_for("listar_ministerios"))

@app.post("/ministerios/<int:id>/excluir")
def excluir_ministerio(id):
    ministerio = db.session.get(Ministerio, id)
    db.session.delete(ministerio)
    db.session.commit()
    return redirect(url_for("listar_ministerios"))
    
if __name__ == "__main__":
    app.run(debug=True)
