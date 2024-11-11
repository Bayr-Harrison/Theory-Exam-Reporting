import os
import pg8000
import pandas as pd
import streamlit as st

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
    db_query = "SELECT * FROM exam_results where date = '2024-11-07';"
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
st.title("View and Filter Exam Results Data")

# Fetch data from Supabase
data = fetch_data_from_supabase()

# Sidebar filters
st.sidebar.header("Filter Data")

# Filter by 'Exam'
exam_options = data['exam'].unique()
selected_exam = st.sidebar.multiselect("Select Exam(s):", exam_options, default=exam_options)

# Filter by 'Result'
result_options = data['result'].unique()
selected_result = st.sidebar.multiselect("Select Result(s):", result_options, default=result_options)

# Filter by Date Range
min_date = data['date'].min()
max_date = data['date'].max()
start_date, end_date = st.sidebar.date_input("Date Range:", [min_date, max_date])

# Apply filters to the data
filtered_data = data[
    (data['exam'].isin(selected_exam)) &
    (data['result'].isin(selected_result)) &
    (data['date'] >= pd.to_datetime(start_date)) &
    (data['date'] <= pd.to_datetime(end_date))
]

# Display the filtered data in a table format
st.write("Filtered Exam Results Data:")
st.dataframe(filtered_data)  # Interactive table
