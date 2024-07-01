import cx_Oracle

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="freepdb1")
connection = None

try:
    connection = cx_Oracle.connect(user="sys", password="yoominchoi1234A", dsn=dsn, mode=cx_Oracle.SYSDBA)
    print("successful")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print(f"Error: {error.message}")

if connection:
    connection.close()
