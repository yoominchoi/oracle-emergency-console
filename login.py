import streamlit as st
from common import authenticate_user

def main():
    st.title("Login")

    login_id = st.text_input("ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(login_id, password)
        if user:
            st.session_state.user = user
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid ID or password.")


if __name__ == "__main__":
    main()