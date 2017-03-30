import MySQLdb
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "nisarg",
                           db = "pythonprogram")
    c = conn.cursor()

    return c, conn
