import streamlit as st
from common import update_incident, fetch_incident, fetch_latest_note

# Sidebar for selecting user type
user_type = st.sidebar.selectbox("Select User Type", ["Admin", "General User"])

if user_type == "Admin":
    st.title("Admin Dashboard")

    incident_id = st.sidebar.number_input('Incident ID', min_value=1)
    
    message = st.text_area("Send Message to General Users")
    if st.button("Send"):
        update_incident(incident_id, "alert_msg", message)
        print(incident_id, message)
        st.success("Message sent!")

    location = st.text_input("Update Shooter's Location")
    if st.button("Update Location"):
        update_incident(incident_id, "shooter_location", location)
        st.success("Shooter's location updated!")

    st.header("Messages to General Users")
    messages = fetch_latest_note()
    if messages:
        st.write(messages)
    else:
        st.write("No messages available.")

    st.header("Incident Details")
    incident = fetch_incident()
    if incident:
        st.write(incident)
    else:
        st.write("No incident details available.")
else:
    st.write("Switch to general.py for General User functionalities.")
