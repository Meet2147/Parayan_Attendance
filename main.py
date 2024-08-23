import streamlit as st
import pandas as pd
import sqlite3
import csv
import os

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

# Define the local CSV file URL
csv_url = 'https://raw.githubusercontent.com/Meet2147/Parayan_Attendance/main/user_data.csv'

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
        file_exists = os.path.isfile(csv_url)
        with open(csv_url, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Number", "Locality"])  # Writing headers if the file does not exist
            writer.writerow([name, number, locality])

        st.success("Data saved successfully!")
    else:
        st.error("Please fill in all fields.")

# Reading the local CSV file
try:
    df = pd.read_csv(csv_url)
    if not df.empty:
        st.write("Data from the local CSV file:")
        st.write(df)
    else:
        st.write("No data found in the local CSV file.")
except Exception as e:
    st.error(f"Error reading CSV file: {e}")

# Optional: Display the data stored in the SQLite database
if st.checkbox("Show data stored locally"):
    df_local = pd.read_sql_query("SELECT * FROM users", conn)
    st.write(df_local)

# Close the SQLite connection
conn.close()
