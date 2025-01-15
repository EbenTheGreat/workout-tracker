# Import necessary libraries
import requests
import os
import gspread
from dotenv import load_dotenv
from datetime import datetime
from google.oauth2.service_account import Credentials

# Load environment variables from the .env file
load_dotenv()

# Constants
WORKOUT_API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
APP_ID = os.getenv("APP_ID")  # Nutritionix API App ID from environment variables
APP_KEY = os.getenv("APP_KEY")  # Nutritionix API App Key from environment variables
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Replace with your Google Sheet ID
QUERY_PROMPT = "What exercise did you do?\n"

# Initialize Google Sheets API credentials
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Open the target Google Sheet by ID
sheet = client.open_by_key(GOOGLE_SHEET_ID)
workout_sheet = sheet.sheet1  # Access the first worksheet

# Get the current date and time
current_date = datetime.now().strftime("%d/%m/%Y")  # Format: DD/MM/YYYY
current_time = datetime.now().strftime("%H:%M")  # Format: HH:MM (24-hour format)

# Prepare headers for the Nutritionix API request
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "Content-Type": "application/json"
}

# Prompt the user to enter their exercise details
exercise_query = input(QUERY_PROMPT)

# Prepare the payload for the Nutritionix API request
data = {
    "query": exercise_query
}

# Make a POST request to the Nutritionix API
response = requests.post(url=WORKOUT_API_ENDPOINT, json=data, headers=headers)

# Extract the list of exercises from the API response
workout_data = response.json().get("exercises", [])

# Loop through each exercise in the response and append it to the Google Sheet
for exercise in workout_data:
    # Prepare a row with exercise details
    row = [
        current_date,
        current_time,
        exercise["name"].title(),
        exercise["duration_min"],
        exercise["nf_calories"]
    ]

    # Append the row to the Google Sheet
    workout_sheet.append_row(row)

    # Print confirmation for each added row
    print(f"Added to sheet: {row}")


