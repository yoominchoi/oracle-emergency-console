import streamlit as st
from common import register_user

def main():
    st.title("User Registration")
    user_type = st.selectbox("User Type", ['Admin', 'General'])
    login_id = st.text_input("ID")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    phone_num = st.text_input("Phone Number")

    if st.button("Register"):
        if login_id and password and name and phone_num:
            register_user(login_id, password, user_type, name, phone_num)
            st.success("User registered successfully")
            st.experimental_rerun()
        else:
            st.error("Please enter all the details for the registration.")
    
    # st.write('## Registered Users')
    # users = fetch_users()
    # user_type_map = {
    #     'G': 'General',
    #     'A': 'Admin'
    # }
    # for usr in users:
    #     st.write(f"LoginID: {usr[0]}, User Type: {user_type_map[usr[0]]}, Name: {usr[1]}, Phone Number: {usr[2]}")

if __name__ == '__main__':
    main()
