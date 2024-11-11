import os
import pg8000
import pandas as pd
import streamlit as st

# Set a simple password
PASSWORD = os.environ["APP_PASSWORD"]

# Create a password input field in Streamlit
password = st.text_input("Enter Password", type="password")
if password != PASSWORD:
    st.warning("Incorrect password")
    st.stop()
else:
    st.success("Access granted!")


# Function to establish a database connection
def get_database_connection():
    db_connection = pg8000.connect(
        database=os.environ["SUPABASE_DB_NAME"],
        user=os.environ["SUPABASE_USER"],
        password=os.environ["SUPABASE_PASSWORD"],
        host=os.environ["SUPABASE_HOST"],
        port=os.environ["SUPABASE_PORT"]
    )
    return db_connection

# Function to fetch data from the 'exam_results' table in Supabase
def fetch_data_from_supabase():
    # Connect to the database
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    # SQL query to select all data from the 'exam_results' table
    db_query = "SELECT * FROM exam_results whhere date = '2024-11-07';"
    db_cursor.execute(db_query)

    # Fetch all rows and convert to a DataFrame
    rows = db_cursor.fetchall()
    column_names = [desc[0] for desc in db_cursor.description]  # Get column names
    data = pd.DataFrame(rows, columns=column_names)

    # Close the connection
    db_cursor.close()
    db_connection.close()

    return data

# Streamlit interface for displaying data
st.title("View Exam Results Data")

# Fetch and display data from Supabase
data = fetch_data_from_supabase()

# Display the data in a table format
st.write("Exam Results Data:")
st.dataframe(data)  # Interactive table for easier navigation
