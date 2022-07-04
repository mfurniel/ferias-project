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


@app.route('/ferias/<id_region>')
def ferias(id_region):

    conn = get_dbconnection()

    cur = conn.cursor()
    sqlquery2="SELECT feria.nombre FROM feria INNER JOIN comuna ON feria.comuna = comuna.id and comuna.region=\'" + id_region + "\';"
    cur.execute(sqlquery2)
    row = cur.fetchall()
    nombres=row
    cur.close()

    cur = conn.cursor()
    sqlquery3="SELECT feria.id FROM feria INNER JOIN comuna ON feria.comuna = comuna.id and comuna.region=\'" + id_region + "\';"
    cur.execute(sqlquery3)
    row = cur.fetchall()
    ids=row
    cur.close()


    cur = conn.cursor()
    sqlquery="SELECT feria.direccion FROM feria INNER JOIN comuna ON feria.comuna = comuna.id and comuna.region=\'" + id_region + "\';"
    cur.execute(sqlquery)
    row = cur.fetchall()
    direccion=row
    cur.close()

    cur = conn.cursor()
    sqlquery4="select comuna.nombre from comuna INNER JOIN feria ON feria.comuna=comuna.id where comuna.region=\'" + id_region + "\';"
    cur.execute(sqlquery4)
    row = cur.fetchall()
    comuna=row
    cur.close()
    conn.close()

    return render_template("ferias.html",nombres=nombres,id=ids,direccion=direccion,comuna=comuna)

@app.route('/puestos/<id_feria>', methods=['GET','POST'])
def puestos(id_feria):
    if request.method=='POST':
        idzz=request.form['test']
        print(idzz)
        return redirect(url_for('negocios',id_n=idzz))
    conn = get_dbconnection()
    cur = conn.cursor()
    sqlquery = "select nombre from puesto where puesto.feria=\'" + id_feria + "\';"
    cur.execute(sqlquery)
    row = cur.fetchall()
    nombres=row
    cur.close()
    cur = conn.cursor()
    sqlquery = "select descripcion from puesto where puesto.feria=\'" + id_feria + "\';"
    cur.execute(sqlquery)
    row = cur.fetchall()
    descripcion=row
    cur.close()
    cur = conn.cursor()
    sqlquery = "select id from puesto where puesto.feria=\'" + id_feria + "\';"
    cur.execute(sqlquery)
    row = cur.fetchall()
    ids=row
    # print(ids)
    cur.close()
    conn.close()
    return render_template("puestos.html",nombres=nombres,descripcion=descripcion,ids=ids)

@app.route('/negocio/<id_n>', methods=['GET','POST'])
def negocios(id_n):

    if request.method=='POST':
        if request.form.get('mas')=='+':
           
            conn = get_dbconnection()
            cur=conn.cursor()
            sqlquery="update puesto set likes=likes+1 where id= \'" + id_n + "\';"
            cur.execute(sqlquery)
            conn.commit()
            cur.close()
            conn.close()
        
        else:

            idzz=request.form['comment']
            print(idzz)
            conn = get_dbconnection()
            cur=conn.cursor()
            sqlquery="insert into comentario(id,comentario) values( \'" + id_n + "\' ,\'" + idzz + "\');"
            cur.execute(sqlquery)
            conn.commit()
            cur.close()
            conn.close()

    conn = get_dbconnection()

    cur = conn.cursor()
    sqlquery = "SELECT producto.nombre FROM producto INNER JOIN puestoproducto ON producto.id = puestoproducto.producto where puestoproducto.puesto= \'" + id_n + "\';"
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
    sqlquery3="select * from feriante where rut = \'" + datos[5] + "\';"
    cur.execute(sqlquery3)
    row=cur.fetchone()
    persona=row
    print(persona)
    cur.close()


    cur=conn.cursor()
    sqlquery4="select comentario from comentario where id = \'" + id_n + "\';"
    cur.execute(sqlquery4)
    row=cur.fetchall()
    criticas=row
    print(persona)
    cur.close()

    cur=conn.cursor()
    sqlquery5="select precio from puestoproducto where puestoproducto.puesto=\'" + id_n + "\';"
    cur.execute(sqlquery5)
    row=cur.fetchall()
    precios=row
    print(precios)
    cur.close()


    conn.close()

    return render_template("negocios.html",nombres=nombres,datos=datos,persona=persona,criticas=criticas,precios=precios)

@app.route('/compra')
def compra():
     return render_template("compra.html")

#---------------------carrito?----------------------
