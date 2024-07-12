import streamlit as st
import json
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Function to read service account credentials from JSON file
def read_service_account_secret():
    file_path = "streamlitgs-0c166fb61174.json"  # Adjust this path accordingly
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None
    
    with open(file_path) as f:
        return json.load(f)

# Function to connect to Google Sheets
def connect_to_gsheets():
    service_account_info = read_service_account_secret()
    if service_account_info is None:
        return None

    try:
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

# Function to download data from Google Sheets
def download_data(client, spreadsheet_id, worksheet_name):
    if client is None:
        return None
    
    try:
        sheet = client.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        return data
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Spreadsheet not found with ID: {spreadsheet_id}")
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Worksheet not found with name: {worksheet_name}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return None

# Streamlit app
def main():
    st.title("Dashboard GS")

    # Connect to Google Sheets
    gsheets_client = connect_to_gsheets()

    # Define your spreadsheet ID and worksheet name
    spreadsheet_id = '1w2r3wLti31AqbH8huSzxpOa5fQ0Mp658YPTYuJ0AvT4'  # Replace with your spreadsheet ID
    worksheet_name = 'Sheet1'  # Replace with your worksheet name

    # Download the data
    if st.button("Refresh Data"):
        data = download_data(gsheets_client, spreadsheet_id, worksheet_name)
    else:
        data = None

    # Display the data in a tabular format
    if data:
        df = pd.DataFrame(data)
        st.write(df)
    else:
        st.write("No data found or unable to fetch data.")

if __name__ == "__main__":
    main()
