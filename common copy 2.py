import cx_Oracle
from datetime import datetime
import time

def init_db():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="freepdb1")
    # connection = cx_Oracle.connect(user="myuser", password="yoominchoi1234A", dsn=dsn)
    connection = cx_Oracle.connect(user="system", password="yoominchoi1234A", dsn=dsn)
    return connection


#Function to update the incident
def update_incident(connection, location, user, note):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO INCIDENT_UPDATES (location, timestamp, updated_by, note)
            VALUES (:location, :timestamp, :updated_by, :note)
        """, location=location, timestamp=datetime.now(), updated_by=user, note=note)
    connection.commit()

def fetch_incidents(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT location, timestamp, updated_by FROM INCIDENT_UPDATES ORDER BY timestamp DESC")
        rows = cursor.fetchall()
    return [{"location": row[0], "timestamp": row[1].strftime("%Y-%m-%d %H:%M:%S"), "updated_by": row[2]} for row in rows]

def fetch_latest_note(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT note from INCIDENT_UPDATES WHERE note IS NOT NULL ORDER BY timestamp DESC FETCH FIRST 1 ROW ONLY")
        row = cursor.fetchone()
    return row[0] if row else None
