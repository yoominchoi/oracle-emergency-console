import streamlit as st
import pandas as pd
from common import fetch_users, update_incident, fetch_incidents
# import json

# Sidebar for selecting user
# user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim"])
users = fetch_users()
user_dict = {user_id: (name, user_type) for user_id, name, user_type in users}

user_id = st.sidebar.selectbox("Select User", list(user_dict.keys()))
user_name, user_type = user_dict[user_id]

#######################
# Admin User
if user_type == 'A':
    st.title("Admin Dashboard")

    incident_id = st.sidebar.number_input('Incident ID', min_value=1)

    # Incident Details
    st.header("Incident Details")
    incidents = fetch_incidents()
    # incident[0]: timestamp, incident[1]: updated_by, incident[2]: shooter_location, incident[3]: alert_msg
    if incidents:
        df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
        df = df[df["Shooter Location"].notnull()]  # Filter out rows where Shooter Location is null
        df.drop(columns=['Alert Message'], axis=1, inplace=True)
        if not df.empty:
            st.table(df.head(3))
        else:
            st.write("No incident details available.")
    else:
        st.write("No incident details available.")

    # Already sent message
    st.header("Messages to Users")
    messages = fetch_incidents()
    # find the most recent message that is not null
    for msg in messages:
        if msg[3] is not None:
            msg = msg
            break
    if msg:
        st.write(f"{msg[3]} ({msg[0]})")
    else:
        st.write("No messages available.")
    
    # Updating an alert message
    message = st.text_area("Send Message to General Users")
    if st.button("Send"):
        update_incident(user_id, "alert_msg", message)
        st.success("Message sent!")
    
    # Updating shooter's location
    location = st.text_input("Update Shooter's Location")
    if st.button("Update Location"):
        update_incident(user_id, "shooter_location", location)
        st.success("Shooter's location updated!")

#######################
# General User
elif user_type == 'G':
    st.title(f"General User {user_name}")

    incident_id = st.sidebar.number_input('Incident ID', min_value=1)

    st.header("Incident Details")
    incidents = fetch_incidents()
    if incidents:
        df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
        df = df[df["Shooter Location"].notnull()]  # Filter out rows where Shooter Location is null
        df.drop(columns=['Alert Message'], axis=1, inplace=True)
        df.drop(columns=['Updated By'], axis=1, inplace=True)
        if not df.empty:
            st.table(df.head(3))
    else:
        st.write("No incident details available.")

    # Message from Admin
    st.header("Messages from Admin")
    messages = fetch_incidents()
    # find the most recent message that is not null
    for msg in messages:
        if msg[3] is not None:
            msg = msg
            break
    if msg:
        st.write(f"{msg[3]} ({msg[0]})")
    else:
        st.write("No messages available.")

    # Updating Shooter's Location
    location = st.text_input("Update Shooter's Location")
    if st.button("Update"):
        update_incident(user_id, "shooter_location", location)
        st.success("Shooter's location updated!")