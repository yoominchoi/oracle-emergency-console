import streamlit as st
import pandas as pd
from common import update_final_shooter_desc, fetch_final_shooter_desc, fetch_incidents, fetch_incident_details, fetch_shooter_desc, download_shooter_txt, update_incident, fetch_incident_details, update_user_status, get_user_status, get_people_status, get_safe_status_pie_chart
import time
from datetime import datetime

def main():
    if "user" not in st.session_state:
        st.error("Please log in first.")
        st.rerun()

    user = st.session_state.user
    ######################################################################################################
    # user information - ((id) 1, (name) 'Katrina Wilson', (user_type) 'A')
    ######################################################################################################
    # Admin User
    if user[2] == 'A':     
        st.title(f"Admin {user[1]}'s Dashboard")

        st.sidebar.title("Incidents")
        incidents = fetch_incidents()

        if incidents:
            incident_ids = [str(incident[0]) for incident in incidents]
            selected_incident_id = st.sidebar.selectbox("Select Incident", incident_ids)
            if selected_incident_id:
                incident_details = fetch_incident_details(selected_incident_id)
                if incident_details:
                    admin_col1, admin_col2 = st.columns(2)                    
                    
                    with admin_col1:
                        # Send Alert Messages to Users
                        st.header("Send Alert Messages")
                        messages = fetch_incident_details(selected_incident_id)
                        # Find the most recent message that is not null
                        for msg in messages:
                            if msg[3] is not None:
                                msg = msg
                                break
                        if msg:
                            original_datetime = datetime.strptime(str(msg[0]), "%Y-%m-%d %H:%M:%S.%f")
                            converted_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            highlighted_msg_text = f'<span style="background-color: #FDFD96; color: black;">{msg[3]} ({converted_datetime_str})</span>'
                            st.markdown(highlighted_msg_text, unsafe_allow_html=True)
                        else:
                            st.write("No messages available.")

                        # Updating an alert message
                        message = st.text_area("Send Message to Users")
                        if st.button("Send"):
                            update_incident(1, user[0], "alert_msg", message)
                            st.success("Message sent!")
                        
                        # Shooter's Final Description
                        st.header("Send Final Shooter's Description")
                        final_shooter_desc = fetch_final_shooter_desc(selected_incident_id)
                        # st.write(final_shooter_desc[0] + ' (Updated: '+ str(final_shooter_desc[1])+ ')')
                        original_datetime = datetime.strptime(str(final_shooter_desc[1]), "%Y-%m-%d %H:%M:%S")
                        converted_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        highlighted_final_shooter_desc = f'<span style="background-color: #FDFD96; color: black;">{final_shooter_desc[0]} \n(Updated: {converted_datetime_str})</span>'
                        st.markdown(highlighted_final_shooter_desc, unsafe_allow_html=True)
                        # Download text file of shooter's descriptions + Instruction
                        data = fetch_shooter_desc()
                        download_shooter_txt(data)

                        new_final_shooter_desc = st.text_input("Please do not update the final description if you did not follow the instruction above. \n Update the final description of the shooter.")
                        if st.button("Update", key="admin_update_final_shooter_desc"):
                            if user[0] and selected_incident_id and new_final_shooter_desc:
                                update_final_shooter_desc(selected_incident_id, user[0], new_final_shooter_desc)
                                st.success("Shooter's final description updated.")
                                st.rerun()

                        # Shooter's Location
                        st.header("Add Shooter's Location & Description")
                        # incident[0]: timestamp, incident[1]: updated_by, incident[2]: shooter_location, incident[3]: alert_msg
                        df = pd.DataFrame(incident_details, columns=["Reported Time", "Updated By", "Shooter Location", "Alert Message"])
                        df = df[df["Shooter Location"].notnull()]  # Filter out rows where Shooter Location is null
                        df.drop(columns=['Alert Message'], axis=1, inplace=True)
                        if not df.empty:
                            st.table(df.head(3))
                            # Adding shooter's location
                            location = st.text_input("Add Shooter's Location")
                            if st.button("Add", key="admin_add_location"):
                                if user[0] and selected_incident_id and location:
                                    update_incident(selected_incident_id, user[0], "shooter_location", location)
                                    st.success("Shooter's location updated!")
                                else:
                                    st.error("Error occurred.")
                            
                            # Adding shooter's description
                            shooter_desc = st.text_input("Add Shooter's Description")
                            if st.button("Add", key="admin_add_shooter_desc"):
                                update_incident(selected_incident_id, user[0], "shooter_desc", shooter_desc)
                                st.success("Shooter's description updated!")
                        else:
                            st.write("No incident details available.")

                    with admin_col2:
                        # People Status Pie Chart
                        result = get_people_status()

                        data1 = {'Category': ['Safe', 'Unsafe', 'Not responded'], '# of people': result[:3]}
                        df1 = pd.DataFrame(data1)
                        st.header("Safety Status Check")
                        get_safe_status_pie_chart(df1)

                        # Urgent List
                        st.header("Urgent List")
                        df2 = pd.DataFrame(result[3], columns=["Name", "Phone Number"])
                        st.write(df2)
                else:
                    st.write("No incident details available.")
            else:
                st.write("No incident available.")
        else:
            st.write("No incident available.")

    ######################################################################################################
    # General User
    elif user[2] == 'G':
        st.title(f"Incident Details for {user[1]}")

        st.sidebar.title("Incidents")
        incidents = fetch_incidents()
        if incidents:
            incident_ids = [str(incident[0]) for incident in incidents]
            selected_incident_id = st.sidebar.selectbox("Select Incident", incident_ids)
        
            if selected_incident_id:
                incident_details = fetch_incident_details(selected_incident_id)
                if incident_details:
                    
                    # Message from Admin
                    messages = fetch_incident_details(selected_incident_id)

                    for msg in messages:
                        if msg[3] is not None:
                            msg = msg
                            break
                    if msg:
                        original_datetime = datetime.strptime(str(msg[0]), "%Y-%m-%d %H:%M:%S.%f")
                        converted_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M:%S")

                        st.header('Alert Message from Admin')
                        highlighted_msg_text = f'<span style="background-color: #FDFD96; color: black;">{msg[3]} ({converted_datetime_str})</span>'
                        st.markdown(highlighted_msg_text, unsafe_allow_html=True)
                    else:
                        st.write("No messages available.")

                    # Shooter's Final Description
                    st.header('Updated Shooter Final Description')
                    final_shooter_desc = fetch_final_shooter_desc(selected_incident_id)
                    original_datetime = datetime.strptime(str(final_shooter_desc[1]), "%Y-%m-%d %H:%M:%S")
                    converted_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    highlighted_final_shooter_desc = f'<span style="background-color: #FDFD96; color: black;">{final_shooter_desc[0]} \n(Updated: {converted_datetime_str})</span>'
                    st.markdown(highlighted_final_shooter_desc, unsafe_allow_html=True)

                    # Shooter's Location
                    st.header("Shooter's Location")
                    ######################################################################################################
                    # incident[0]: timestamp, incident[1]: updated_by, incident[2]: shooter_location, incident[3]: alert_msg
                    ######################################################################################################
                    df = pd.DataFrame(incident_details, columns=["Reported Time", "Updated By", "Shooter Location", "Alert Message"])
                    df = df[df["Shooter Location"].notnull()]  # Filter out rows where Shooter Location is null
                    df.drop(columns=['Alert Message'], axis=1, inplace=True)
                    df.drop(columns=['Updated By'], axis=1, inplace=True)
                    if not df.empty:
                        st.table(df.head(3))
                    else:
                        st.write("No incident details available.")
                else:
                    st.write("No incident details available.")

                # Updating Shooter's Location
                location = st.text_input("Update Shooter's Location")
                if st.button("Update", key="location_update"):
                    update_incident(selected_incident_id, user[0], "shooter_location", location)
                    st.success("Shooter's location updated!")

                st.header("Witnessed shooter?")
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
                    <button style="background-color: green; border: none; width: 50px; height: 40px; border-radius: 10%;" data-selected="{selected}" onclick="window.location.href += '&{key}={label.lower()}'; return false;">
                        {label}
                    </button>
                    """
                    st.markdown(button_html, unsafe_allow_html=True)

                # Check if it is safe
                st.header("Are you safe?")
                col1, col2 = st.columns(2)
                with col1:
                    if is_safe == 'Y':
                        colored_button("Yes", key="safe_yes", selected="true")
                    else:
                        if st.button("Yes", key="safe_yes"):
                            update_user_status(user[0], "is_safe", 'Y')
                            st.rerun()
                with col2:
                    if is_safe == 'N':
                        colored_button("No", key="safe_no", selected="true")
                    else:
                        if st.button("No", key="safe_no"):
                            update_user_status(user[0], "is_safe", 'N')
                            st.rerun()

                if is_safe == 'N':
                    # Check if it is urgent
                    st.header("Is it an urgent situation?")
                    col3, col4 = st.columns(2)
                    with col3:
                        if is_urgent == 'Y':
                            colored_button("Yes", key="urgent_yes", selected="true")
                        else:
                            if st.button("Yes", key="urgent_yes"):
                                update_user_status(user[0], "is_urgent", 'Y')
                                st.rerun()
                    with col4:
                        if is_urgent == 'N':
                            colored_button("No", key="urgent_no", selected="true")
                        else:
                            if st.button("No", key="urgent_no"):
                                update_user_status(user[0], "is_urgent", 'N')
                                st.rerun()
            else:
                st.sidebar.write("No incident details available.")
        else:
                st.sidebar.write("No incidents available.")

    time.sleep(10)
    st.rerun()

if __name__ == "__main__":
    main()