import streamlit as st
from common import update_incident, fetch_latest_note, fetch_shooter_location

# Sidebar for selecting user
user = st.sidebar.selectbox("Select User", ["General User 1", "General User 2"])

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
messages = fetch_latest_note()
if messages:
    st.write(messages)
else:
    st.write("No messages available.")
