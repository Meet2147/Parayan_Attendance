import streamlit as st
import pandas as pd
import sqlite3

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

# Load existing data from the SQLite database into a DataFrame
df = pd.read_sql_query("SELECT name, number, locality FROM users", conn)

# Streamlit UI
st.title('User Information Form')

# Input fields
name = st.text_input("Enter your Name")
number = st.text_input("Enter your Phone Number")
locality = st.selectbox("Select your Locality", ["Ghatkopar West", "Ghatkopar East"])

# Button to submit the form
if st.button("Submit"):
    if name and number and locality:
        # Create a new DataFrame with the input data
        new_data = pd.DataFrame({
            'Name': [name],
            'Number': [number],
            'Locality': [locality]
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Insert data into the SQLite database
        c.execute('INSERT INTO users (name, number, locality) VALUES (?, ?, ?)', (name, number, locality))
        conn.commit()

        st.success("Data saved successfully!")
    else:
        st.error("Please fill in all fields.")

# Display the DataFrame
if not df.empty:
    st.write("Collected Data:")
    st.write(df)
else:
    st.write("No data available.")

# Option to download the data as a CSV file
if not df.empty:
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='user_data.csv',
        mime='text/csv',
    )

# Optional: Display the data stored in the local SQLite database
if st.checkbox("Show data stored locally"):
    df_local = pd.read_sql_query("SELECT * FROM users", conn)
    st.write(df_local)

# Close the SQLite connection
conn.close()
