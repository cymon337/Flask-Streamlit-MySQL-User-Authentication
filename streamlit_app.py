import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"  # Change this to your Flask app's URL

def register():
    with st.form("Register"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            response = requests.post(f"{BACKEND_URL}/register", json={"name": name, "email": email, "password": password})
            if response.status_code == 201:
                st.success("Registered successfully. You can now log in.")
            else:
                st.error("Registration failed.")

def login():
    with st.form("Login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
            if response.status_code == 200:
                st.success("Logged in successfully.")
            else:
                st.error("Invalid credentials.")

st.title("User Authentication")

if st.checkbox("Register"):
    register()
else:
    login()
