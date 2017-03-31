import MySQLdb
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "12345",
                           db = "document_tracking")
    c = conn.cursor()

    return c, conn
