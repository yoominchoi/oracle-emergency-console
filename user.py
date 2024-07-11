import streamlit as st
import pandas as pd
from common import fetch_users, update_incident, fetch_incidents, fetch_shooter_location

# Sidebar for selecting user
# user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim"])
users = fetch_users()
user_dict = {user_id: (name, user_type) for user_id, name, user_type in users}

user_id = st.sidebar.selectbox("Select User", list(user_dict.keys()))
user_name, user_type = user_dict[user_id]

if user_type == 'A':
    st.title("Admin Dashboard")

    incident_id = st.sidebar.number_input('Incident ID', min_value=1)

    # Incident Details
    st.header("Incident Details")
    incidents = fetch_incidents()
    if incidents:
        df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
        alert_msg = df['Alert Message']
        print(alert_msg)
        df.drop(columns=['Alert Message'], axis=1, inplace=True)
        st.table(df)
    else:
        st.write("No incident details available.")

    # Message to users
    st.header("Messages to Users")
    messages = fetch_incidents()
    if messages:
        for msg in messages:
            st.write(f"{msg[3]} ({msg[0]} - {msg[1]})")
    else:
        st.write("No messages available.")

    message = st.text_area("Send Message to General Users")
    if st.button("Send"):
        update_incident(user_id, "alert_msg", message)
        st.success("Message sent!")

    location = st.text_input("Update Shooter's Location")
    if st.button("Update Location"):
        update_incident(user_id, "shooter_location", location)
        st.success("Shooter's location updated!")
elif user_type == 'G':
    st.title(f"General User {user_name}")

    incident_id = st.sidebar.number_input('Incident ID', min_value=1)

    st.header("Incident Details")
    incidents = fetch_incidents()
    if incidents:
        # df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
        # st.table(df)
        df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
        alert_msg = df['Alert Message']
        df.drop(columns=['Alert Message'], axis=1, inplace=True)
        st.table(df)
    else:
        st.write("No incident details available.")

    # Message from Admin
    st.header("Messages from Admin")
    messages = fetch_incidents()
    if messages:
        for msg in messages:
            st.write(f"{msg[3]} ({msg[0]} - {msg[1]})")
    else:
        st.write("No messages available.")

    # Updating Shooter's Location
    location = st.text_input("Update Shooter's Location")
    if st.button("Update"):
        update_incident(user_id, "shooter_location", location)
        st.success("Shooter's location updated!")