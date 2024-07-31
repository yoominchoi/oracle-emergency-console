import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import oracledb

def get_db_connection():
    dsn = oracledb.makedsn("localhost", 1521, service_name="freepdb1")
    conn = oracledb.connect(user="user1", password="yoominchoi1234A", dsn=dsn)
    return conn

@st.cache_data
def register_user(login_id, password, user_type, name, phone_num):
    conn = get_db_connection()
    user_type_map = {
        'General': 'G',
        'Admin': 'A'
    }
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (login_id, password, user_type, name, phone_num) VALUES (:1, :2, :3, :4, :5)", 
                   (login_id, password, user_type_map[user_type], name, phone_num))
    conn.commit()
    cursor.close()

def authenticate_user(login_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, user_type FROM users WHERE login_id=:1 AND password=:2", (login_id, password))
    user = cursor.fetchone()
    cursor.close()
    return user

def fetch_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT login_id, name, phone_num, user_type FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users

def fetch_incidents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT incident_id, incident_desc, incident_status, reported_time FROM incidents")
    incidents = cursor.fetchall()
    cursor.close()
    return incidents

def fetch_incident_details(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT i.reported_time, u.name as updated_by, i.shooter_location, i.alert_msg
        FROM incident_details i
        LEFT JOIN users u ON i.updated_by = u.id 
        WHERE incident_id=:1
        ORDER BY i.reported_time DESC
    """, (incident_id, ))
    rows = cursor.fetchall()
    cursor.close()
    # conn.close()
    
    return rows

def update_user(user_id, column, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if value in ['Y', 'N']:
        valid_columns = ['is_safe', 'is_urgent']
        if column not in valid_columns:
            raise ValueError("Invalid column name.")
        query = f"""
            UPDATE users
            SET {column} = :value
            WHERE id = :user_id
        """
        cursor.execute(query, {'value': value, 'user_id': user_id})

    get_people_status()

    conn.commit()
    cursor.close()
    # conn.close()

def get_user_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_safe, is_urgent FROM users WHERE id = :user_id", {'user_id': user_id})
    result = cursor.fetchone()
    conn.close()
    return result
    

def get_people_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Total # of safe users
    cursor.execute("""
        SELECT COUNT(*)
        FROM users u
        WHERE u.user_type = 'G' and u.is_safe = 'Y'
    """)
    safe_count = cursor.fetchone()
    
    # Total # of unsafe users
    cursor.execute("""
        SELECT COUNT(*)
        FROM users u
        WHERE u.user_type = 'G' and u.is_safe = 'N'
    """)
    unsafe_count = cursor.fetchone()

    # rest of the users
    cursor.execute("""
        SELECT COUNT(*)
        FROM users u
        WHERE u.user_type = 'G' and u.is_safe is null
    """)
    rest_safe_count = cursor.fetchone()

    cursor.execute("""
        SELECT name, phone_num
        FROM users u
        WHERE u.user_type = 'G' and u.is_urgent = 'Y'
    """)
    result = cursor.fetchall()

    result = [safe_count[0], unsafe_count[0], rest_safe_count[0], result]
    return result

def get_safe_status_pie_chart(df):
    fig, ax = plt.subplots(figsize=(1,1), facecolor='none')
    colors = ['green','red','gray']
    wedges, _ = ax.pie(df['# of people'],colors=colors, radius=0.5, labels=['']*len(df))

    ax.axis('equal')

    legend_labels = [f'{cat}: {val}' for cat, val in zip(df['Category'], df['# of people'])]
    legend = ax.legend(wedges, legend_labels, title="People Safety Status", loc="center left", bbox_to_anchor=(1,0,0.5,1))

    for text in legend.get_texts():
        text.set_fontsize('small')
        text.set_color('white')

    legend.get_frame().set_facecolor('grey')

    st.pyplot(fig)


def update_incident(incident_id, user_id, column, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    if value != '' and value != None and value != '<NA>':
        if column == "alert_msg" or column == "shooter_location" or column == 'shooter_desc':
            query = f"""
                INSERT INTO incident_details (incident_id, updated_by, {column}) 
                VALUES (:incident_id, :user_id, :value)
            """
            cursor.execute(query, {'incident_id':incident_id, 'value':value, 'user_id':user_id})
        else:
            query = f"""
                UPDATE incident_details 
                SET {column} = :value, updated_by = :user_id, tireported_timemestamp = SYSTIMESTAMP
                WHERE id = (SELECT id FROM incident_details WHERE rownum = 1 ORDER BY reported_time DESC)
            """
            cursor.execute(query, {'value':value, 'user_id':user_id})
    conn.commit()
    if value != '' and value != None and value != '<NA>':
        st.rerun()


def check_login_id_exists(login_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE login_id=:1", (login_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


############# AI ########## (shooter's description)
def fetch_shooter_desc():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT shooter_desc from incident_details i WHERE i.shooter_desc is not null")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]

def save_to_txt(data, file_path):
    with open(file_path, 'w') as file:
        file.write("These are descriptions of a shooter or shooters.\n")
        for line in data:
            file.write(f"{line}\n")


def download_shooter_txt(data):
    if data:        
        instruction = """
                1) Open a new terminal and run commands below to open Jupyter Notebook.
                > ssh -L 8888:localhost:8888 -i <<ssh key file location>> opc@<<public IP Address>>\n
                
                > ssh -L 8888:localhost:8888 -i /Users/yoomchoi/Desktop/emergency_control_app/ssh-key-2024-06-27.key opc@207.211.166.86
                
                > jupyter-lab --no-browser --ip 0.0.0.0 --port 8888

                2) Upload the downloaded shooter_desc.txt file in the 'emergency-console' folder.
                3) Run 'vectorization.ipynb' file.
                4) Copy the result at the end and update the shooter's description in the box below.
                 """
        with st.expander("Instruction to get an updated shooter's final description:", expanded=True):
            st.write(instruction)

        file_path = 'shooter_desc.txt'

        save_to_txt(data, file_path)

        # Provide the downloading link
        with open(file_path, 'r') as file:
            st.download_button('Download Shooter Description Text File', file, file_name=file_path)

    else:
        st.write("No data available")

def update_final_shooter_desc(incident_id, user_id, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    if value != '' and value != None and value != '<NA>':
        query = f"""
            INSERT INTO incident_details (incident_id, updated_by, final_shooter_desc)
            VALUES (:incident_id, :user_id, :value)
        """
        cursor.execute(query, {'incident_id':incident_id, 'value':value, 'user_id': user_id})
    conn.commit()

def fetch_final_shooter_desc(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT final_shooter_desc, reported_time FROM incident_details WHERE incident_id=:1 AND final_shooter_desc is NOT NULL ORDER BY reported_time DESC", (incident_id, ))
    rows = cursor.fetchone()
    cursor.close()
    return rows
