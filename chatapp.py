import streamlit as st
import json
import os
import time

# Dummy Credentials for Login
USER_CREDENTIALS = {
    'sri': 'sri123',
    'div': 'div123'
}

# Page Configuration
st.set_page_config(page_title="Chat App with Login", layout="centered")
st.title("💬 Chat App")

CHAT_FILE = 'chat_data.json'

# Initialize Chat File if Not Exists
def initialize_chat_file():
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'w') as file:
            json.dump([], file)

initialize_chat_file()

# Read Messages from File
def read_messages():
    with open(CHAT_FILE, 'r') as file:
        return json.load(file)

# Write Message to File
def write_message(username, message):
    messages = read_messages()
    messages.append({'username': username, 'message': message})
    with open(CHAT_FILE, 'w') as file:
        json.dump(messages, file)

# Clear Chat File
def clear_chat():
    with open(CHAT_FILE, 'w') as file:
        json.dump([], file)

# Session Management for Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = None

# Login Page
if not st.session_state['logged_in']:
    st.subheader("🔐 Please Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    def login():
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

    # Login using button or Enter key
    if st.button("Login") or (st.session_state.get('login_username') and st.session_state.get('login_password') and st.session_state.get('login_username') in USER_CREDENTIALS and USER_CREDENTIALS[st.session_state.get('login_username')] == st.session_state.get('login_password')):
        login()
else:
    # Chat Section
    st.subheader(f"Welcome {st.session_state['username']}! Start chatting below")

    # Display Chat Messages
    messages = read_messages()
    for msg in messages:
        st.write(f"**{msg['username']}**: {msg['message']}")

    # Input for New Message
    def send_message():
        user_input = st.session_state.chat_input.strip()
        if user_input:
            write_message(st.session_state['username'], user_input)
            st.session_state.chat_input = ""
            st.rerun()

    # Message input with Enter key or Send button
    st.text_input("Type your message", key="chat_input", on_change=send_message)
    if st.button("Send"):
        send_message()

    # Logout Button
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

    # Clear Chat Button
    if st.button("Clear Chat"):
        clear_chat()
        st.rerun()

    # Auto-refresh Chat Every 2 Seconds
    time.sleep(2)
    st.rerun()
