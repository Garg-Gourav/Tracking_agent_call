from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
import os

app = Flask(__name__)

# Path to the Excel file
excel_file = 'Tracking_agent_call/agent.xlsx'

# Try to load the file, or create it if it doesn't exist
if os.path.exists(excel_file):
    try:
        response_df = pd.read_excel(excel_file)
        print(f"Loaded existing Excel file: {excel_file}")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        response_df = pd.DataFrame(columns=['Agent Number', 'Response'])
else:
    response_df = pd.DataFrame(columns=['Agent Number', 'Response'])
    print(f"Created new DataFrame with columns: {response_df.columns}")

# Route to capture agent's response (1 for yes, 2 for no)
@app.route("/gather", methods=['POST'])
def gather():
    try:
        # Capture the digit pressed by the agent
        digits = request.form.get('Digits')  # Get the digit pressed by the agent
        agent_number = request.form.get('To')  # Get the agent's phone number

        # Debug logs to verify incoming data
        print(f"Digits received: {digits}")
        print(f"Agent number received: {agent_number}")

        # Initialize Twilio response
        resp = VoiceResponse()

        # Convert the digit into a human-readable response
        if digits == '1':
            response = 'Yes'
            resp.say('Thank you for confirming your presence.')
        elif digits == '2':
            response = 'No'
            resp.say('Thank you for letting us know.')
        else:
            response = 'Invalid'
            resp.say('Invalid response. Please press 1 if you are at the location, or press 2 if you are not.')

        # Log the response in the DataFrame
        global response_df
        new_row = pd.DataFrame({'Agent Number': [agent_number], 'Response': [response]})
        print(f"New row to add: {new_row}")

        response_df = pd.concat([response_df, new_row], ignore_index=True)

        # Save the DataFrame to Excel
        print("Saving data to Excel...")
        response_df.to_excel(excel_file, index=False)
        print(f"Data saved to {excel_file}")

        # Respond to Twilio with the appropriate message
        return str(resp)

    except Exception as e:
        print(f"Error handling response: {e}")
        return "Error", 500

if __name__ == "__main__":
    app.run(debug=True)
