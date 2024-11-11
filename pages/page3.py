import os
import streamlit as st
import pandas as pd
import pg8000
from io import BytesIO
import zipfile

# Set a simple password
PASSWORD = os.environ["APP_PASSWORD"]

# Create a password input field in Streamlit
password = st.text_input("Enter Password", type="password")
if password != PASSWORD:
    st.warning("Incorrect password")
    st.stop()
else:
    st.success("Access granted!")
