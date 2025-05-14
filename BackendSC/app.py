from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/agregar')
def pagina_agregar():
    return render_template('agregar.html')

@app.route('/ver')
def pagina_ver():
    return render_template('ver_notas.html')


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante TEXT,
            materia TEXT,
            nota REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/notas', methods=['GET'])
def get_notas():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    notas = conn.cursor().execute('SELECT * FROM notas').fetchall()
    conn.close()
    return jsonify([dict(nota) for nota in notas])

@app.route('/api/agregar', methods=['POST'])
def agregar_nota():
    data = request.json
    conn = sqlite3.connect('database.db')
    conn.execute(
        'INSERT INTO notas (estudiante, materia, nota) VALUES (?, ?, ?)',
        (data['estudiante'], data['materia'], data['nota'])
    )
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Nota guardada'})

if __name__ == '_main_':
    init_db()
    app.run(debug=True, host='0.0.0.0')

print("Este archivo se está ejecutando")

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    init_db()
    app.run(debug=True, host='0.0.0.0')