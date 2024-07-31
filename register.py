import streamlit as st
from common import register_user, check_login_id_exists

def main():
    st.title("User Registration")
    user_type = st.selectbox("User Type", ['Admin', 'General'])
    name = st.text_input("Name")
    login_id = st.text_input("ID")
    password = st.text_input("Password", type="password")
    phone_num = st.text_input("Phone Number")

    if st.button("Register"):
        if login_id and password and name and phone_num:
            if check_login_id_exists(login_id):
                st.error("ID already exists. Please choose another ID.")
            register_user(login_id, password, user_type, name, phone_num)
            st.success("User registered successfully")
            st.session_state.registered = True
            st.rerun()
        else:
            st.error("Please enter all the details for the registration.")
    
if __name__ == '__main__':
    main()
