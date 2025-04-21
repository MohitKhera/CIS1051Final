import os
from dotenv import load_dotenv

import streamlit as st
import pyrebase
from datetime import datetime
import requests

load_dotenv()

firebaseConfig = {
    'apiKey': os.getenv("API_KEY"),
    'authDomain': os.getenv("AUTH_DOMAIN"),
    'projectId': os.getenv("PROJECT_ID"),
    'databaseURL': os.getenv("DATABASE_URL"),
    'storageBucket': os.getenv("STORAGE_BUCKET"),
    'messagingSenderId': os.getenv("MESSAGING_SENDER_ID"),
    'appId': os.getenv("APP_ID"),
    'measurementId': os.getenv("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

st.sidebar.title("App")

dropbox = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])
email = st.sidebar.text_input("Please enter your email address")
password = st.sidebar.text_input("Please enter your password")

if dropbox == 'Sign up':
    handle = st.sidebar.text_input("Please enter your email address", value = "Default")
    submit = st.sidebar.button("Create Account")
    if submit:
        signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebaseConfig['apiKey']}"
        check = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(signup_url, json=check)
        answer = response.json()
        if "error" in answer:   
          if answer["error"]["message"] == "EMAIL_EXISTS":
              st.warning("This email is already registered.")
        else:
          user = auth.sign_in_with_email_and_password(email,password)
          db.child(user['localId']).child("Handle").set(handle)
          db.child(user['localId']).child("ID").set(user['localId'])
          st.title("Welcome" + handle)
          st.info("Please Login")
if dropbox == 'Login':
    login = st.sidebar.button('Login')
    if login:
        login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebaseConfig['apiKey']}"
        check = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(login_url, json=check)
        answer = response.json()
        if "error" in answer:
            st.error("Invalid email or password.")
        else:
            st.session_state['user'] = answer
            st.success("Login successful!")
            st.switch_page("pages/Research.py")