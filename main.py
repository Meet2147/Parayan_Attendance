import streamlit as st
import pandas as pd
import sqlite3
import csv

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

        # Append data to CSV file
        with open('user_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, number, locality])

        st.success("Data saved successfully!")

    else:
        st.error("Please fill in all fields.")

# Optional: Display the data in the app
if st.checkbox("Show data"):
    df = pd.read_sql_query("SELECT * FROM users", conn)
    st.write(df)

# Close the SQLite connection
conn.close()