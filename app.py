import streamlit as st
import register
import login
import dashboard
# import create

def main():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "registered" not in st.session_state:
        st.session_state.registered = False

    if st.session_state.user is None:
        st.sidebar.title("Navigation")
        
        if st.session_state.registered:
            st.session_state.registered = False
            login.main()
        else:
            page = st.sidebar.radio("Go to", ["Login", "Register"])

            if page == "Login":
                login.main()
            elif page == "Register":
                register.main()
    else:
        # st.sidebar.title("Navigation")
        # page = st.sidebar.radio("Go to", ["Dashboard", "Report a New Incident" ])
        # if page == "Report a New Incident":
        #     create.main()
        # else:
            # query_params = st.query_params()
            # if "incident_id" in query_params:
        dashboard.main()



if __name__ == '__main__':
    main()
