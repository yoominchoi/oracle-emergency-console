import streamlit as st
from common import init_db, ensure_table_exists, update_incident, fetch_incidents, fetch_latest_note
from streamlit_js_eval import streamlit_js_eval


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

def send_location(lat, lon):
    location = f"Lat: {lat}, Lon: {lon}"
    update_incident(connection, location, user)
    st.success("Location updated successfully")
    st.rerun()

# get gps location
if st.button("Use GPS to update location"):
    gps_location = streamlit_js_eval(js_code="navigator.geolocation.getCurrentPosition((position) => { return {lat: position.coords.latitude, lon: position.coords.longitude}; });", key="gps_location")
    if gps_location:
        send_location(gps_location['lat'], gps_location['lon'])

if st.button("Update Location"):
    update_incident(connection, location, user, "")
    st.success("Location updated successfully.")
    st.rerun()

connection.close()