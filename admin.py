import streamlit as st
import pandas as pd
from common import update_incident, fetch_incidents, fetch_shooter_location

# Sidebar for selecting user type
user_name = st.sidebar.selectbox("Select User", ["Katrina Wilson"])

st.title("Admin Dashboard")

incident_id = st.sidebar.number_input('Incident ID', min_value=1)

# Incident Details
st.header("Incident Details")
incidents = fetch_incidents()
if incidents:
    df = pd.DataFrame(incidents, columns=["Timestamp", "Updated By", "Shooter Location", "Alert Message"])
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
    update_incident(incident_id, "alert_msg", message)
    st.success("Message sent!")

location = st.text_input("Update Shooter's Location")
if st.button("Update Location"):
    update_incident(incident_id, "shooter_location", location)
    st.success("Shooter's location updated!")
