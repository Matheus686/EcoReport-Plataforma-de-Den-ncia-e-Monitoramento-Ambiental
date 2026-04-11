import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS denuncias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    cep TEXT,
    localizacao TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    descricao TEXT,
    imagem TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("PRAGMA table_info(denuncias)")
colunas = [coluna[1] for coluna in cursor.fetchall()]

if "imagem" not in colunas:
    cursor.execute("ALTER TABLE denuncias ADD COLUMN imagem TEXT")

conexao.commit()
conexao.close()

print("Banco criado/atualizado com sucesso!")
