from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

@app.route('/cursos/', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM curso"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []

        for fila in datos:
            curso = {
                'codigo': fila[0],
                'nombre': fila[1],
                'creditos': fila[2]
            }

            cursos.append(curso)

        return jsonify({
            'cursos': cursos,
            'mensaje': 'Cursos listados'
        })
    except Exception as ex:
        return jsonify({
            'mensaje': 'Error'
        })

@app.route('/cursos/<codigo>/', methods=['GET'])
def mostrar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql_select = f"SELECT * FROM curso WHERE codigo = {codigo}"
        cursor.execute(sql_select)
        registro = cursor.fetchone()

        if registro is None:
            return jsonify({ 'mensaje': 'Curso no encontrado' })

        curso = {
            'codigo': registro[0],
            'nombre': registro[1],
            'creditos': registro[2]
        }

        return jsonify({ 
            'mensaje': 'Curso encontrado',
            'curso': curso
        })
    except Exception as ex:
        return jsonify({ 'mensaje': 'Error' })

@app.route('/cursos/', methods=['POST'])
def agregar_curso():
    try:
        cursor = conexion.connection.cursor()
        codigo = request.json['codigo']
        sql_select = f"SELECT * FROM curso WHERE codigo = {codigo}"
        cursor.execute(sql_select)
        registro = cursor.fetchone()

        if registro is None:
            nombre = request.json['nombre']
            creditos = request.json['creditos']
            sql_insert = f"INSERT INTO curso VALUES ('{codigo}', '{nombre}', {creditos})"
            cursor.execute(sql_insert)
            conexion.connection.commit()

            return jsonify({ 'mensaje': 'El curso se ha agregado' })

        return jsonify({ 'mensaje': 'El curso ya existe en la base de datos' })
    except Exception as ex:
        return jsonify({ 'mensaje': 'Error' })

@app.route('/cursos/<codigo>/', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql_select = f"SELECT * FROM curso WHERE codigo = {codigo}"
        cursor.execute(sql_select)
        registro = cursor.fetchone()

        if registro is None: 
            return jsonify({ 'mensaje': 'El curso no existe' })

        sql_delete = f"DELETE FROM curso WHERE codigo = {codigo}"
        cursor.execute(sql_delete)
        conexion.connection.commit()

        return jsonify({ 'mensaje': 'El curso se ha eliminado' })
    except Exception as ex:
        return jsonify({ 'mensaje': 'Error' })

@app.route('/cursos/<codigo>/', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        slq_select = f"SELECT * FROM curso WHERE codigo = {codigo}"
        cursor.execute(slq_select)
        registro = cursor.fetchone()

        if registro is None:
            return jsonify({ 'mensaje': 'El curso no existe' })

        nombre = request.json['nombre']
        creditos = request.json['creditos']
        sql_update = f"UPDATE curso SET nombre = '{nombre}', creditos = {creditos} WHERE codigo = {codigo}"
        cursor.execute(sql_update)
        conexion.connection.commit()

        return jsonify({ 'mensaje': 'Se ha actualizado un curso' })
    except Exception as ex:
        return jsonify({ 'mensaje': 'Error' })

def pagina_no_encontrada(error):
    return '<h1>La pagina que intentas buscar no existe...</h1>', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()