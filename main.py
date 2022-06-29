from flask import Flask, render_template, request,redirect,url_for
import psycopg2

app=Flask(__name__)

#--------------Conexion con la base de datos----------------------
def get_dbconnection():
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "newuser"
    PSQL_PASS = "newuser"
    PSQL_DB = "feria"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    return conn
#--------------Fin----------------------

#------------------------------------ejemplo------------------------------------------
# @app.route('/')
# def index():
#     conn = get_dbconnection()               #Conexión a la base de datos.
#     cur = conn.cursor()
#     cur.execute("select nombre from region;")    #Query a base de datos de mails
#     rows = cur.fetchall()                   #Obtención de tuplas (con una única columna)
#     nombres = rows
#     cur.close()                             #Desconexión a la base de datos.
#     conn.close()

#     return render_template("index.html",nombres=nombres)
#-----------------------------------fin------------------------------------------

#-----------------------------------Principal------------------------------------------

@app.route('/')
def index():
    return render_template("index.html")

#-----------------------------------fin------------------------------------------

@app.route('/regiones')
def regiones():
    return render_template("regiones.html")


@app.route('/ferias')
def ferias():
    conn = get_dbconnection()
    cur = conn.cursor()
    sqlquery = "select nombre from feria;"
    cur.execute(sqlquery)
    row = cur.fetchall()
    nombres=row
    cur.close()
    conn.close()
    return render_template("ferias.html",nombres=nombres)

@app.route('/puestos', methods=['GET','POST'])
def puestos():
    if request.method=='POST':
        idzz=request.form['test']
        print(idzz)
        return redirect(url_for('negocios',id_n=idzz))
    conn = get_dbconnection()
    cur = conn.cursor()
    sqlquery = "select nombre from puesto;"
    cur.execute(sqlquery)
    row = cur.fetchall()
    nombres=row
    cur.close()
    cur = conn.cursor()
    sqlquery = "select descripcion from puesto;"
    cur.execute(sqlquery)
    row = cur.fetchall()
    descripcion=row
    cur.close()
    cur = conn.cursor()
    sqlquery = "select id from puesto;"
    cur.execute(sqlquery)
    row = cur.fetchall()
    ids=row
    # print(ids)
    cur.close()
    conn.close()
    return render_template("puestos.html",nombres=nombres,descripcion=descripcion,ids=ids)

@app.route('/negocio/<id_n>', methods=['GET','POST'])
def negocios(id_n):
    asa=id_n
    conn = get_dbconnection()

    cur = conn.cursor()
    sqlquery = "SELECT producto.nombre FROM producto INNER JOIN puestoproducto ON producto.id = puestoproducto.producto INNER JOIN puesto ON puestoproducto.puesto = \'" + id_n + "\';"
    #sqlquery = "select nombre from producto;"
    cur.execute(sqlquery)
    row = cur.fetchall()
    nombres=row
    cur.close()

    cur=conn.cursor()
    sqlquery2="select * from puesto where id = \'" + id_n + "\';"
    cur.execute(sqlquery2)
    row=cur.fetchone()
    datos=row
    print(datos)
    cur.close()

    cur=conn.cursor()
    sqlquery2="select * from feriante where rut = \'" + datos[5] + "\';"
    cur.execute(sqlquery2)
    row=cur.fetchone()
    persona=row
    print(persona)
    cur.close()

    conn.close()

    return render_template("negocios.html",nombres=nombres,datos=datos,persona=persona)

#---------------------carrito?----------------------
