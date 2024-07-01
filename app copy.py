import streamlit as st
import cx_Oracle
from datetime import datetime

# dummy data (initially reported data)
incident_data = {
    "incident_type": "active shooter",
    "location": "500 Oracle Pathway Building 200 Floor 3",
    "timestamp": datetime.now(),
    "who_did_update": "John Smith"
}

#Function to update the incident
def update_incident(connection, location, who_did_update):
    if connection is None:
        st.write("No database connection")
        return
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE incidents
                SET location = :location, timestamp = CURRENT_TIMESTAMP, who_did_update = :who_did_update
                WHERE incident_id = (SELECT incident_id FROM incidents ORDER BY timestamp DESC FETCH FIRST 1 ROWS ONLY)   
                   """, {"location": location, "who_did_update": who_did_update})
    connection.commit()
    cursor.close()

def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="freepdb1")
    connection = None
    try:
        connection = cx_Oracle.connect(user="test01", password="yoominchoi1234A", dsn=dsn)
        print("Successfully connected to the database")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error connecting to the database: {error.message}")
    return connection

# # Database connection details
# dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
# # connection = cx_Oracle.connect(user="yoominchoi", password="yoominchoi1234A", dsn=dsn)
# connection = None

# try:
#     connection = cx_Oracle.connect(user="test01", password="yoominchoi1234A", dsn="localhost/orclpdb1")
#     st.write("Successfully connected to your database.")
# except cx_Oracle.DatabaseError as e:
#     error, = e.args
#     st.write(f"Error connecting to the database: {error.message}")

# Function to fetch incidents
def fetch_incidents(connection):
    if connection is None:
        st.write("No database connection")
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
    data = cursor.fetchall()
    cursor.close()
    return data

# Function to insert a new incident
def insert_incident(connection, incident_type, location, who_did_update):
    if connection is None:
        st.write("No database connection")
        return
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO incidents (incident_type, location, who_did_update)
                   VALUES (:incident_type, :location, :who_did_update)
                   """, {"incident_type": incident_type, "location": location, "who_did_update": who_did_update})
    connection.commit()
    cursor.close()

#Streamlit UI
st.title("Oracle Emergency Control App")
# get the database connection
connection = get_db_connection()

#Login as a user
user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim", "Katrina Wilson Admin"])

if user == "Katrina Wilson (admin)":
    st.header("Admin User Page")
    incident_type = st.selectbox("Incident Type", ["active shooter", "fire", "natural disaster", "medical emergency"])
    location = st.text_input("Location")
    if st.button("Report Incident"):
        insert_incident(connection, incident_type, location, user)
        st.success("Incident Reported Successfully.")
    
    st.subheader("Incident List")
    incidents = fetch_incidents(connection)
    for incident in incidents:
        st.write(f"Type: {incident[2]}, Location: {incident[3]}, Time: {incident[1]}, Updated by: {incident[4]}")
    st.subheader("Urgent Help Needed List")
    # need more details lataer

else:
    st.header("General User Page")
    st.write(f"Welcome, {user}!")
    incidents = fetch_incidents(connection)
    if incidents:
        latest_incident = incidents[0]
        st.write(f"Incident Type: {latest_incident[2]}")
        st.write(f"Last Updated Location: {latest_incident[3]}")
        st.write(f"Last Updated Time: {latest_incident[1]}")
        st.write(f"Updated By: {latest_incident[4]}")
    else:
        st.write("No incidents reported yet.")

    incident_type = st.selectbox("Incident Type", ["active shooter", "fire evacuation", "natural disaster", "other"])
    location = st.text_input("Enter Shooter Location (Building and Floor)")
    
    if st.button("Update Location"):
        update_incident(connection, location, user)
        st.success("Location updated successfully.")
    if st.button("Urgent Help Needed"):
        # more details later
        st.warning("Urgent help request sent.")
    
    # Close the database connection when the script ends
    st.write("Closeing database connection.")
    if connection:
        connection.close()