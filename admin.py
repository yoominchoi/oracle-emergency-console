import streamlit as st
import pandas as pd
from common import fetch_users, update_incident, fetch_incidents, fetch_shooter_location

# Sidebar for selecting user type
# user_name = st.sidebar.selectbox("Select User", ["Katrina Wilson"])

users = fetch_users()
user_dict = {user_id: (name, user_type) for user_id, name, user_type in users}

user_id = st.sidebar.selectbox("Select User ID", list(user_dict.keys()))
user_name, user_type = user_dict[user_id]

