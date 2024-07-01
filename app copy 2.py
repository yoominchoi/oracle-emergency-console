import streamlit as st
import cx_Oracle
from datetime import datetime

# dummy data (initially reported data)
incident_updates = [
    {
        "Location": "500 Oracle Pathway Building 200 Floor 3",
        "Timestamp": "2024-06-30 08:40:37",
        # "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Updated By": "John Smith"
    }
]

#Function to update the incident
def update_incident(location, user):
    global incident_updates
    new_update= {
        "Location": location,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Updated By": user
    }
    # incident_updates.append(new_update)
    # incident_updates = sorted(incident_updates, key=lambda x: x["Timestamp"], reverse=True)
    incident_updates.insert(0, new_update)

#Streamlit UI
st.title("Oracle Emergency Control App")

#Login as a user
user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim", "Katrina Wilson Admin"])

st.subheader("Shooter Location Updates")
# if incident_updates:
#     st.table(incident_updates)

if user == "Katrina Wilson Admin":
    st.header("Admin User Page")
    display_data = [
        {
            "Location": update["Location"],
            "Timestamp": update["Timestamp"],
            "Updated By": update["Updated By"]
        } for update in incident_updates
    ]

else:
     display_data = [
        {
            "Location": update["Location"],
            "Timestamp": update["Timestamp"]
        } for update in incident_updates
    ]
st.table(display_data)

if user != "Katrina Wilson Admin":
    location = st.text_input("Enter Shooter Location (Building and Floor)")
    if st.button("Update Location"):
        update_incident(location, user)
        st.success("Location updated successfully.")