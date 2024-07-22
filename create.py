import streamlit as st
from common import add_incident

def main():
    if "user" not in st.session_state:
        st.error("Please log in first")
        st.stop()
    
    user_id = st.session_state.user[0]

    st.title("Add an incident")
    incident_status = st.selectbox("Status", ['Current', 'Resolved'])
    incident_desc = st.text_input("Description")

    if st.button("Report"):
        if incident_desc and incident_status:
            incident_id = add_incident(user_id, incident_desc, incident_status)
            # st.session_state.add_incident = True
            st.session_state.incident_id = incident_id
            st.experimental_set_query_params(incident_id=incident_id)
            st.success("Added incident successfully.")
            st.rerun()
        else:
            st.error("Please enter all the details")

if __name__ == '__main__':
    main()