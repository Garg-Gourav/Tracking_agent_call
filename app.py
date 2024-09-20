import subprocess
from twilio.rest import Client
import time
# Twilio credentials
account_sid = '***'  # Replace with your Twilio Account SID
auth_token = '***'    # Replace with your Twilio Auth Token
twilio_phone_number = '***'  # Replace with your Twilio phone number

# Initialize Twilio Client
client = Client(account_sid, auth_token)

# Agent details (place with the specific number)
agent_name = 'g*******g'
agent_number = '+91******0'  # Replace with the agent's phone number (include country code)
service_location = '***a'
time_slot = '10:00 PM'


# Function to make a call and ask for agent confirmation
def make_automated_call(agent_name, agent_number, service_location, time_slot):
    twiml = f'<Response><Say>Hello {agent_name}, you are scheduled for a service at {service_location} at {time_slot}. Please press 1 if you are at the location. Press 2 if you are not.</Say><Gather action="https://2d5e-103-253-150-1.ngrok-free.app/gather" numDigits="1"/></Response>'

    call = client.calls.create(
        to=agent_number,
        from_=twilio_phone_number,
        twiml=twiml
    )
    print(f"Call placed to {agent_name} at {agent_number} for service at {service_location} at {time_slot}")

    return call.sid

# Make a call to the agent
make_automated_call(agent_name, agent_number, service_location, time_slot)
