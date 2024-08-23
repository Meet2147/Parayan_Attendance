import streamlit as st
import pandas as pd
import sqlite3
import csv
import os
import requests
from io import StringIO

# Initialize connection to SQLite database
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          name TEXT, 
          number TEXT, 
          locality TEXT)
          ''')
conn.commit()

# Retrieve the CSV URL from environment variables
csv_url = os.getenv('CSV_URL')

# Function to load CSV data from GitHub
def load_original_data():
    response = requests.get(csv_url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

# Streamlit UI
st.title('User Information Form')

# Input fields
name = st.text_input("Enter your Name")
number = st.text_input("Enter your Phone Number")
locality = st.selectbox("Select your Locality", ["Ghatkopar West", "Ghatkopar East"])

# Button to submit the form
if st.button("Submit"):
    if name and number and locality:
        # Insert data into the SQLite database
        c.execute('INSERT INTO users (name, number, locality) VALUES (?, ?, ?)', (name, number, locality))
        conn.commit()

        # Append data to the local CSV file
        # local_csv_url = csv_url
        file_exists = os.path.isfile(csv_url)
        with open(csv_url, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Number", "Locality"])  # Write headers if the file does not exist
            writer.writerow([name, number, locality])

        st.success("Data saved successfully!")
    else:
        st.error("Please fill in all fields.")

# Reading the CSV file from GitHub using the custom function
df = load_original_data()
if df is not None:
    if not df.empty:
        st.write("Data from the GitHub CSV file:")
        st.write(df)
    else:
        st.write("No data found in the GitHub CSV file.")

# Optional: Display the data stored in the local SQLite database
if st.checkbox("Show data stored locally"):
    df_local = pd.read_sql_query("SELECT * FROM users", conn)
    st.write(df_local)

# Close the SQLite connection
conn.close()
