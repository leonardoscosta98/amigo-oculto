from flask import Flask, render_template, request, redirect, url_for
from models import (
    listar_confraternizacoes, criar_confraternizacao,
    listar_participantes, cadastrar_participante,
    get_participante, participantes_disponiveis, atualizar_sorteio
)
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", lista=listar_confraternizacoes())

@app.route("/nova", methods=["POST"])
def nova():
    nome = request.form["nome"]
    _id = criar_confraternizacao(nome)
    return redirect(url_for("ver_confraternizacao", cid=_id))

@app.route("/c/<int:cid>")
def ver_confraternizacao(cid):
    return render_template(
        "confraternizacao.html",
        cid=cid,
        participantes=listar_participantes(cid)
    )

@app.route("/c/<int:cid>/add", methods=["POST"])
def add_participante(cid):
    nome = request.form["nome"]
    cadastrar_participante(nome, cid)
    return redirect(url_for("ver_confraternizacao", cid=cid))

@app.route("/sorteio/<int:pid>")
def sorteio(pid):
    p = get_participante(pid)

    if p["ja_sorteou"]:
        return render_template("sorteio.html", participante=p, amigo=None)

    disponiveis = participantes_disponiveis(p["confraternizacao_id"], pid)

    amigo = random.choice(disponiveis)
    atualizar_sorteio(pid, amigo["id"])

    return render_template("sorteio.html", participante=p, amigo=amigo)
