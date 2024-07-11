import streamlit as st
import pandas as pd
from common import update_incident, fetch_incidents, fetch_shooter_location

# Sidebar for selecting user
user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim"])

st.title(f"General User Dashboard - {user}")

incident_id = st.sidebar.number_input('Incident ID', min_value=1)

location = st.text_input("Update Shooter's Location")
if st.button("Update Location"):
    update_incident(incident_id, "shooter_location", location)
    st.success("Shooter's location updated!")

st.header("Shooter's Location")
shooter_location = fetch_shooter_location(incident_id)
if shooter_location:
    st.write(shooter_location)
else:
    st.write("No shooter location available.")

st.header("Messages from Admin")
messages = fetch_incidents()
if messages:
    for msg in messages:
        st.write(f"{msg[0]} - {msg[1]}: {msg[2]} ({msg[3]})")
else:
    st.write("No messages available.")

st.header("Incident Details")
incidents = fetch_incidents()
if incidents:
    df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
    st.table(df)
else:
    st.write("No incident details available.")
