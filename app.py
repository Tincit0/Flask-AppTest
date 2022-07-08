from flask import Flask,render_template,request,redirect,send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
from pathlib import Path,PurePath
import os

   
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'

mysql.init_app(app)

#Metodo viejo, probablemente borrar comentarios si todo funciona ok
#CARPETA = PurePath('Fullstack Python - Codo a codo', 'Flask', 'SistemaEmpleados', 'Flask-AppTest', 'uploads')
#directory = PurePath('Fullstack Python - Codo a codo', 'Flask', 'SistemaEmpleados', 'Flask-AppTest', 'uploads')
#app.config['CARPETA']=CARPETA

directory=Path() / "uploads"
cwd=Path.cwd()
up_dir=directory.resolve()
print(directory.exists(), directory.is_dir(),cwd, directory)


CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route("/")
def index():
    sql = "SELECT * FROM `sistema`.`empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    #Query para borrar la foto del disco
    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    #Query para borrar las entradas de la base de datos
    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id=request.form['txtID']
    
    sql="UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    datos=(_nombre,_correo,id)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    #Condicion para modificar foto si la hay. Se borra la foto anterior
    
    if _foto.filename!='':
        
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save(str(up_dir)+ '/' + nuevoNombreFoto)
        
        
        cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()
        
    
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

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
    
    if _foto.filename!='':
        nuevoNombreFoto = tiempo+_foto.filename
#        _foto.save(str(directory) + "/" + nuevoNombreFoto)
        _foto.save(str(up_dir)+ '/' +nuevoNombreFoto)

    
    #definimos y lanzamos la query
    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,_correo,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

#genero acceso a la carpeta uploads usando send_from_directory
@app.route('/upload/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__ == '__main__':
    app.run(debug=True)
    
