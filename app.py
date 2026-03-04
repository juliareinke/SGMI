import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
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
    
class Funcao(db.Model):
    __tablename__ = "funcoes"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    
    ministerio_id = db.Column(
        db.Integer,
        db.ForeignKey("ministerios.id"),
        nullable=False
    )
    
    ministerio = db.relationship("Ministerio", backref="funcoes")
    
    __table_args__ = (
        db.UniqueConstraint("ministerio_id", "nome", name="uq_ministerio_nome"),
    )
    
class PessoaFuncao(db.Model):
    __tablename__ = "pessoa_funcoes" 
    
    id = db.Column(db.Integer, primary_key=True)
    
    pessoa_id = db.Column(
        db.Integer,
        db.ForeignKey("pessoas.id"),
        nullable=False
    )
    
    funcao_id = db.Column(
        db.Integer,
        db.ForeignKey("funcoes.id"),
        nullable=False
    )
    
    pessoa = db.relationship("Pessoa", backref="habilidades")
    funcao = db.relationship("Funcao", backref="pessoas_habilitadas")
    
    __table_args__ = (
        db.UniqueConstraint("pessoa_id", "funcao_id", name="uq_pessoa_funcao"),
    )

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
    
# ROTAS - FUNÇÕES

@app.get("/funcoes")
def listar_funcoes():
    funcoes = Funcao.query.all()
    return render_template("funcoes/list.html", funcoes = funcoes)

@app.get("/funcoes/cadastro")
def mostrar_cadastro_funcao():
    ministerios = Ministerio.query.all()
    return render_template("funcoes/form.html", funcao = None, ministerios = ministerios)

@app.post("/funcoes/cadastro")
def salvar_cadastro_funcao():
    nome = request.form.get("nome")
    ministerio_id = request.form.get("ministerio_id")
    nova_funcao = Funcao(
        nome = nome,
        ministerio_id = ministerio_id
    )
    db.session.add(nova_funcao)
    db.session.commit()
    return redirect(url_for("listar_funcoes"))

@app.get("/funcoes/<int:id>/editar")
def mostrar_edicao_funcao(id):
    funcao = db.session.get(Funcao, id)
    ministerios = Ministerio.query.all()
    return render_template("funcoes/form.html", funcao = funcao, ministerios = ministerios)

@app.post("/funcoes/<int:id>/editar")
def salvar_edicao_funcao(id):
    funcao = db.session.get(Funcao, id)
    funcao.nome = request.form.get("nome")
    funcao.ministerio_id = request.form.get("ministerio_id")
    db.session.commit()
    return redirect(url_for("listar_funcoes"))

@app.post("/funcoes/<int:id>/excluir")
def excluir_funcao(id):
    funcao = db.session.get(Funcao, id)
    db.session.delete(funcao)
    db.session.commit()
    return redirect(url_for("listar_funcoes"))

# ROTAS - PESSOA_FUNÇÃO
@app.get("/pessoas/<int:id>/funcoes")
def pessoa_funcoes(id):
    pessoa = db.session.get(Pessoa, id)
    if not pessoa:
        return "Pessoa não encontrada", 404
    habilidades = PessoaFuncao.query.filter_by(pessoa_id=id).all()
    ids_atribuidos = [h.funcao_id for h in habilidades]
    if ids_atribuidos:
        funcoes = Funcao.query.filter(~Funcao.id.in_(ids_atribuidos)).all()
    else:
        funcoes = Funcao.query.all()
    return render_template(
        "pessoas/funcoes.html",
        pessoa=pessoa,
        habilidades=habilidades,
        funcoes=funcoes
    )
    
@app.post("/pessoas/<int:id>/funcoes/adicionar")
def adicionar_funcao_pessoa(id):
    pessoa = db.session.get(Pessoa, id)
    if not pessoa:
        return "Pessoa não encotrada", 404
    funcao_id = request.form.get("funcao_id")
    if not funcao_id:
        return redirect(url_for("pessoa_funcoes", id=id))
    vínculo = PessoaFuncao(pessoa_id=id, funcao_id=int(funcao_id))
    db.session.add(vínculo)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback() 
    return redirect(url_for("pessoa_funcoes", id=id))

@app.post("/pessoas/<int:id>/funcoes/<int:pf_id>/remover")
def remover_funcao_pessoa(id, pf_id):
    vínculo = db.session.get(PessoaFuncao, pf_id)
    if vínculo:
        db.session.delete(vínculo)
        db.session.commit()
    return redirect(url_for("pessoa_funcoes", id=id))
        
if __name__ == "__main__":
    app.run(debug=True)
