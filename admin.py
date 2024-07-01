import streamlit as st
from common import init_db, ensure_table_exists, update_incident, fetch_incidents, fetch_latest_note

# initialize db and ensure table exists
connection = init_db()
ensure_table_exists(connection)

# streamlit ui
st.title("Oracle Emergency Control Admin Page")

#refresh every 5 secs
st.markdown(
    """
    <script>
    function refresh() {
        window.location.reload();
    }
    setTimeout(refresh, 5000);
    </script>
    """,
    unsafe_allow_html=True
)

if "note" in st.session_state:
    st.subheader("Latest Instructions or Notes")
    st.write(st.session_state.note)

latest_note = fetch_latest_note(connection)
if latest_note:
    st.subheader("Latest Instruction")
    st.write(latest_note)

# display the incident updates in a table format
st.subheader("Shooter Location Updates")
incident_updates = fetch_incidents(connection)

display_data = [
    {
        "location": update["location"],
        "timestamp": update["timestamp"],
        "updated_by": update["updated_by"]
    } for update in incident_updates
]

st.table(display_data)


st.subheader("Send Update")
location = st.text_input("Enter Shooter Location (Building and Floor)")
note = st.text_area("Enter Instructions")
if st.button("Send Update"):
    update_incident(connection, location, "Admin", note)
    # st.session_state.note = note
    st.success("Update sent successfully.")
    st.rerun() # refresh (for update)

connection.close()