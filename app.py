import streamlit as st
import register
import login
import user

def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Register"])

        if page == "Register":
            register.main()
        elif page == "Login":
            login.main()
    else:
        user.main()

if __name__ == '__main__':
    main()
