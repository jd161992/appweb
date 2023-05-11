from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jd161992'
app.config['MYSQL_BD'] = 'prestamo'
mysql = MySQL(app)


app.secret_key = 'mysecretkey'



@app.route('/')
def index():
    now = datetime.now()
    date = now.date().strftime("%d/%m/%Y")
    #arriba prueba de capturar la hora y la fecha actual (solo cuando se acrualice) debo poner con javascrip que sea dinamic
    time = now.time().strftime("%H:%M")
    cur = mysql.connection.cursor()
    cur.execute("USE prestamo")
    cur.execute("select * from cliente")
    data = cur.fetchall()
    return render_template ('index.html', sqlclientes = data, fecha = date, hora = time)


@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("USE prestamo")

        if cedula.isnumeric:
            cur.execute('insert into cliente (CEDULA, NOMBRE, APELLIDO, TELEFONO, DIRECCION) VALUES (%s, %s, %s, %s, %s)',
            (cedula, nombre, apellido, telefono, direccion))
            mysql.connection.commit()
            flash("CLIENTE GUARDADO CON EXITO")
            return redirect(url_for("index"))

        else:
            #AQUI DEBO PONER LA FUNCION DE LOS ERRORES. EN CASO DE QUE SE REPITA LA LLAVE PRIMARIA Y EN CASO DE QUE SEA SRT
            return redirect(url_for("index"))

    
    return "agregar contacto"

@app.route('/destroy/<int:cedula>')
def destroy(cedula):
    cur = mysql.connection.cursor()
    cur.execute("USE prestamo")
    cur.execute("DELETE FROM cliente WHERE CEDULA = '{0}'".format(int(cedula)))
    mysql.connection.commit()
    return redirect (url_for('index'))

@app.route('/editar/<int:cedula>')
def obtenerdatoeditar(cedula):
    cur = mysql.connection.cursor()
    cur.execute("USE prestamo")
    cur.execute("SELECT * FROM cliente WHERE CEDULA = '{0}'".format(int(cedula)))
    data = cur.fetchall()
    print (data[0])
    return render_template ("editar.html", clientedata = data[0])
                

@app.route('/actualizar/<int:cedula>', methods=['POST'])
def actualizar(cedula):
    if request.method == "POST":
        CEDULA = request.form['cedula']
        NOMBRE = request.form['nombre']
        APELLIDO = request.form['apellido']
        TELEFONO = request.form['telefono']
        DIRECCION = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("USE prestamo")
        cur.execute("update cliente set nombre = %s, apellido = %s, telefono = %s, direccion = %s WHERE cedula = %s" ,(NOMBRE,APELLIDO,TELEFONO,DIRECCION,CEDULA))
        mysql.connection.commit()
    flash("ACTUALZIADO CORRECTAMENTE")
    return redirect (url_for("index"))

@app.route('/modal')
def modal():
    return render_template("modal.html")


if __name__== '__main__':
    app.run(debug=True)