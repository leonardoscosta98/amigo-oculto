from database import get_conn

def listar_confraternizacoes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM confraternizacoes ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return data

def criar_confraternizacao(nome):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO confraternizacoes (nome) VALUES (%s) RETURNING id", (nome,))
    _id = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return _id

def listar_participantes(cid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM participantes WHERE confraternizacao_id=%s ORDER BY nome", (cid,))
    data = cur.fetchall()
    conn.close()
    return data

def cadastrar_participante(nome, cid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO participantes (nome, confraternizacao_id)
        VALUES (%s, %s)
        RETURNING id
    """, (nome, cid))
    _id = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return _id

def get_participante(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM participantes WHERE id=%s", (pid,))
    data = cur.fetchone()
    conn.close()
    return data

def atualizar_sorteio(pid, amigo_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE participantes
        SET ja_sorteou = TRUE, amigo_id = %s 
        WHERE id = %s
    """, (amigo_id, pid))
    conn.commit()
    conn.close()

def participantes_disponiveis(cid, pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM participantes
        WHERE confraternizacao_id=%s
        AND id != %s
        AND id NOT IN (
            SELECT amigo_id FROM participantes
            WHERE amigo_id IS NOT NULL AND confraternizacao_id=%s
        )
    """, (cid, pid, cid))
    data = cur.fetchall()
    conn.close()
    return data
