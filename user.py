import streamlit as st
from common import init_db, ensure_table_exists, update_incident, fetch_incidents, fetch_latest_note

connection = init_db()
ensure_table_exists(connection)

st.title("Oracle Emergency Control User Page")

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

user = st.sidebar.selectbox("Select User", ["John Smith", "Sarah Kim"])

latest_note = fetch_latest_note(connection)
if latest_note:
    st.subheader("Latest Instructions")
    st.write(latest_note)


st.subheader("Shooter Location Updates")
incident_updates = fetch_incidents(connection)

display_data = [
    {
        "location": update["location"],
        "timestamp": update["timestamp"]
    } for update in incident_updates
]

st.table(display_data)

st.subheader("General User Page")
location = st.text_input("Enter Shooter Location (Building and Floor)")

if st.button("Update Location"):
    update_incident(connection, location, user, "")
    st.success("Location updated successfully.")
    st.rerun()

connection.close()