from flask import Flask, render_template, request, redirect, url_for
from models import (
    listar_confraternizacoes, criar_confraternizacao,
    listar_participantes, cadastrar_participante,
    get_participante, participantes_disponiveis, atualizar_sorteio,
    editar_confraternizacao, get_confraternizacao, quem_tirou, existe_sorteio_realizado
)
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", lista=listar_confraternizacoes())

@app.route("/nova", methods=["POST"])
def nova():
    nome = request.form["nome"].strip()
    if not nome:
        return redirect(url_for("home"))

    _id = criar_confraternizacao(nome)
    return redirect(url_for("ver_confraternizacao", cid=_id))


@app.route("/c/<int:cid>")
def ver_confraternizacao(cid):
    conf = get_confraternizacao(cid)
    return render_template(
        "confraternizacao.html",
        cid=cid,
        conf=conf,
        participantes=listar_participantes(cid)
    )


@app.route("/c/<int:cid>/add", methods=["POST"])
def add_participante(cid):
    nome = request.form["nome"]
    cadastrar_participante(nome, cid)
    return redirect(url_for("ver_confraternizacao", cid=cid))

@app.route("/c/<int:cid>/editar", methods=["POST"])
def editar(cid):
    novo_nome = request.form["nome"]
    editar_confraternizacao(cid, novo_nome)
    return redirect(url_for("home"))

@app.route("/sorteio/<int:pid>")
def sorteio(pid):
    p = get_participante(pid)
    cid = p["confraternizacao_id"]

    if p["ja_sorteou"]:
        return render_template("sorteio.html", participante=p, amigo=None, cid=cid)

    disponiveis = participantes_disponiveis(cid, pid)

    if len(disponiveis) % 2 == 1 and len(disponiveis) > 1:
       pessoa_que_tirou_ele = quem_tirou(pid)
       if pessoa_que_tirou_ele:
           disponiveis = [d for d in disponiveis if d["id"] != pessoa_que_tirou_ele]

    if len(disponiveis) == 0:
        return render_template(
            "sorteio.html",
            participante=p,
            amigo=None,
            cid=cid,
            erro="Não há mais participantes disponíveis para sortear."
        )

    amigo = random.choice(disponiveis)
    atualizar_sorteio(pid, amigo["id"])

    return render_template("sorteio.html", participante=p, amigo=amigo, cid=cid)



