# importando modulo sqlite para python
import sqlite3

# Conectando-se ao banco de dados de cadastro (ou criando um novo se não existir)
conn = sqlite3.connect("cadastro.db")

# Criando uma tabela chamada 'pessoas' com colunas 'id', 'nome' e 'idade'
conn.execute('''CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                idade INTEGER
            )''')

# Função para criar um novo registro
def criar_registro(nome, idade):
    conn.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?)", (nome, idade))
    conn.commit()

# Função para ler todos os registros
def ler_registros():
    cursor = conn.execute("SELECT id, nome, idade FROM pessoas")
    for row in cursor:
        print(f"ID: {row[0]}, Nome: {row[1]}, Idade: {row[2]}")


# Exemplo de uso
criar_registro("Larissa", 25)
criar_registro("Vinicius", 30)
ler_registros()


# Fechando a conexão com o banco de dados
conn.close()