import streamlit as st
from streamlit_database import DBConnection
import time
import requests
import re

# check if the API key is valid
def is_key_valid(api_key):
    return requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={'model': 'text-davinci-003', 'prompt': 'Hello, world!', 'max_tokens': 1}
    ).ok

# create a class for user authentication
class UserAuthentication:
    def __init__(self):
        pass

    # Function to check user login credentials
    def check_login(username):
        conn = DBConnection.create_connection()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = row[0]
            return True
        else:
            st.error("Incorrect username")
            return False

    # Function to logout the user
    def logout_user():
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state.descriptions = []
        st.session_state.captions = []
        st.session_state.methods = []
        st.session_state.draft_val = ''
        st.session_state.descp = ''
        st.session_state.descp_type = 0
        st.session_state.num_cleared = 0
        st.session_state.random_select = 0
        del st.session_state.langchain_messages

    # Function to check if usename registered is an email
    def is_valid_email(email):
        # Regex pattern for validating an email
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # re.match returns None if the pattern does not match
        if re.match(pattern, email):
            return True
        else:
            return False
    
    # Function to register a new user
    def register_user(username):
        # username cannot be empty or only contains spaces
        if username == '' or username.isspace():
            st.error("Username cannot be empty.")
            return False
        else:
            if UserAuthentication.is_valid_email(username):
                username = username.strip()   # remove spaces at the beginning and end of the username
                conn = DBConnection.create_connection()
                cursor = conn.cursor(buffered=True)
                try:
                    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                    conn.commit()
                    return True
                except:
                    st.error("Error creating account. Username may already exists.")
                    return False
                finally:
                    cursor.close()
                    conn.close()
            else:
                st.error("Username must be a valid email address.")
                return False

    # Main function for Streamlit app
    def user_account():
        st.title("User Authentication Service")

        form = st.form(key='user_form')
        username = form.text_input("Username", max_chars=50)
        login = form.form_submit_button("Login")
        signup = form.form_submit_button("Signup")

        if login:
            if UserAuthentication.check_login(username):
                st.success("Logged in successfully!")
                time.sleep(1)
                st.session_state["logged_in"] = True
                st.rerun()   # rerun the app

        if signup:
            if UserAuthentication.register_user(username):
                if UserAuthentication.check_login(username):
                    st.success(f"Account created for {username}!")
                    time.sleep(1)
                    st.session_state["logged_in"] = True
                    st.rerun()   # rerun the app