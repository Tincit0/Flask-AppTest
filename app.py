from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL
from flask import render_template,request
from datetime import datetime
from pathlib import Path,PurePath
   
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'

mysql.init_app(app)


@app.route("/")
def index():
    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (5, 'Juan Pablo', 'juanpablo@gmail.com', 'juanpablo.jpg');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods = ['POST'])
def storage():
    
    #pedimos el form de create.html
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    #bloque para guardar y nombrar la foto q suban
    nuevoNombreFoto=''
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    location = PurePath('Fullstack Python - Codo a codo', 'Flask', 'SistemaEmpleados', 'Flask-AppTest', 'uploads')
    
    if _foto.filename!='':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save(str(location) + "/" + nuevoNombreFoto)
#       _foto.save( + "/" + nuevoNombreFoto)

    
    #definimos y lanzamos la query
    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('empleados/index.html')


if __name__ == '__main__':
    app.run(debug=True)
    
