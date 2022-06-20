from flask import Flask, render_template
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
