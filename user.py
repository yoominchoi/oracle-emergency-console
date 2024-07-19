import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from common import fetch_incidents, fetch_incident_details, fetch_shooter_desc, download_shooter_txt, update_incident, fetch_incident_details, update_user, get_user_status, get_people_status, get_safe_status_pie_chart
# import json

# Sidebar for selecting user
# user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim"])

def main():
    if "user" not in st.session_state:
        st.error("Please log in first.")
        st.experimental_rerun()

    user = st.session_state.user
    ######################################################################################################
    # user >> ((id) 1, (name) 'Katrina Wilson', (user_type) 'A')
    st.title(f"Welcome {user[1]}")
    
    ######################################################################################################
    # Admin User
    if user[2] == 'A':
        print('useruseruseruseruseruseruser', user)
        st.write("You have admin priveleges.")
        
        # if user_type == 'A':
        st.title("Admin Dashboard")

        st.sidebar.title("Incidents")
        incidents = fetch_incidents()

        if incidents:
            incident_ids = [str(incident[0]) for incident in incidents]
            selected_incident_id = st.sidebar.selectbox("Select Incident", incident_ids)
        
            if selected_incident_id:
                incident_details = fetch_incident_details(selected_incident_id)
                if incident_details:
                    st.write(f"### Incident ID: {incident_details[0]}")
                    st.write(f"**Description:** {incident_details[1]}")
                    st.write(f"**Status:** {incident_details[2]}")

                    # Incident Details
                    st.header("Incident Details")
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
                    messages = fetch_incident_details()
                    # find the most recent message that is not null
                    for msg in messages:
                        if msg[3] is not None:
                            msg = msg
                            break
                    if msg:
                        st.write(f"{msg[3]} ({msg[0]})")
                    else:
                        st.write("No messages available.")
                    
                    # People Status Pie Chart
                    result = get_people_status()

                    data1 = {'Category': ['Safe', 'Unsafe', 'Not responded'], '# of people': result[:3]}
                    df1 = pd.DataFrame(data1)
                    st.title("Safety check")
                    get_safe_status_pie_chart(df1)
                    # st.write(df1)
                    
                    df2 = pd.DataFrame(result[3], columns=["Name", "Phone Number"])
                    st.title("Urgent List")
                    st.write(df2)

                    # Updating an alert message
                    message = st.text_area("Send Message to General Users")
                    if st.button("Send"):
                        update_incident(1, user[0], "alert_msg", message)
                        st.success("Message sent!")
                    
                    # Updating shooter's location
                    location = st.text_input("Update Shooter's Location")
                    if st.button("Update Location"):
                        if user[0] and selected_incident_id and location:
                            print('incident_id', selected_incident_id)
                            update_incident(selected_incident_id, user[0], "shooter_location", location)
                            st.success("Shooter's location updated!")
                        else:
                            st.error("Error occurred.")

                    # Updating shooter's description
                    shooter_desc = st.text_input("Update Shooter's Description")
                    if st.button("Update", key="shooter_desc_update"):
                        update_incident(selected_incident_id, user[0], "shooter_desc", shooter_desc)
                        st.success("Shooter's description updated!")
                    data = fetch_shooter_desc()

                    download_shooter_txt(data)

                ######################################################################################################
                # General User
                elif user[2] == 'G':
                    st.title(f"General User {user[1]}")

                    st.header("Incident Details")
                    incidents = fetch_incident_details()
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
                    messages = fetch_incident_details()
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
                    if st.button("Update", key="location_update"):
                        update_incident(selected_incident_id, user[0], "shooter_location", location)
                        st.success("Shooter's location updated!")

                    st.header("Witness shooter?")
                    shooter_desc = st.text_input("Update Shooter's Description")
                    if st.button("Update", key="shooter_desc_update"):
                        update_incident(selected_incident_id, user[0], "shooter_desc", shooter_desc)
                        st.success("Shooter's description updated!")

                    is_safe, is_urgent = get_user_status(user[0])

                    # Style for buttons
                    button_style = """
                    <style>
                        .stButton>button {
                            background-color: lightgray;
                            color: black;
                        }
                        .stButton>button[data-selected="true"] {
                            background-color: green;
                            color: white;
                        }
                    </style>
                    """
                    st.markdown(button_style, unsafe_allow_html=True)

                    # Helper function to create buttons with state
                    def colored_button(label, key, selected):
                        button_html = f"""
                        <button data-selected="{selected}" onclick="window.location.href += '&{key}={label.lower()}'; return false;">
                            {label}
                        </button>
                        """
                        st.markdown(button_html, unsafe_allow_html=True)

                    # Check if it is safe
                    st.header("Safe?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if is_safe == 'Y':
                            colored_button("Yes", key="safe_yes", selected="true")
                        else:
                            if st.button("Yes", key="safe_yes"):
                                update_user(user[0], "is_safe", 'Y')
                                st.experimental_rerun()
                    with col2:
                        if is_safe == 'N':
                            colored_button("No", key="safe_no", selected="true")
                        else:
                            if st.button("No", key="safe_no"):
                                update_user(user[0], "is_safe", 'N')
                                st.experimental_rerun()

                    if is_safe == 'N':
                        # Check if it is urgent
                        st.header("Urgent?")
                        col3, col4 = st.columns(2)
                        with col3:
                            if is_urgent == 'Y':
                                colored_button("Yes", key="urgent_yes", selected="true")
                            else:
                                if st.button("Yes", key="urgent_yes"):
                                    update_user(user[0], "is_urgent", 'Y')
                                    st.experimental_rerun()
                        with col4:
                            if is_urgent == 'N':
                                colored_button("No", key="urgent_no", selected="true")
                            else:
                                if st.button("No", key="urgent_no"):
                                    update_user(user[0], "is_urgent", 'N')
                                    st.experimental_rerun()
        else:
            st.sidebar.write("No incidents available.")


if __name__ == "__main__":
    main()