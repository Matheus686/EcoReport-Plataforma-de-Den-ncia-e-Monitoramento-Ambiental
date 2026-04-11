from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("database.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def garantir_coluna_imagem():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("PRAGMA table_info(denuncias)")
    colunas = [coluna["name"] for coluna in cursor.fetchall()]

    if "imagem" not in colunas:
        cursor.execute("ALTER TABLE denuncias ADD COLUMN imagem TEXT")

    conexao.commit()
    conexao.close()

@app.route("/")
def index():
    garantir_coluna_imagem()
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM denuncias")
    total = cursor.fetchone()["total"]
    conexao.close()
    return render_template("index.html", total=total)

@app.route("/reportar", methods=["GET", "POST"])
def reportar():
    garantir_coluna_imagem()

    if request.method == "POST":
        tipo = request.form.get("tipo")
        cep = request.form.get("cep")
        localizacao = request.form.get("localizacao")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        descricao = request.form.get("descricao")

        imagem = request.files.get("imagem")
        caminho_imagem = None

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            pasta_upload = os.path.join("static", "uploads")
            os.makedirs(pasta_upload, exist_ok=True)

            caminho_arquivo = os.path.join(pasta_upload, nome_arquivo)
            imagem.save(caminho_arquivo)

            caminho_imagem = caminho_arquivo.replace("\\", "/")

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO denuncias (tipo, cep, localizacao, latitude, longitude, descricao, imagem)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (tipo, cep, localizacao, latitude, longitude, descricao, caminho_imagem)
        )

        conexao.commit()
        conexao.close()

        return redirect("/mapa")

    return render_template("reportar.html")

@app.route("/mapa")
def mapa():
    garantir_coluna_imagem()
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM denuncias ORDER BY id DESC")
    denuncias = cursor.fetchall()
    conexao.close()
    return render_template("mapa.html", denuncias=denuncias)

if __name__ == "__main__":
    garantir_coluna_imagem()
    app.run(debug=True)
