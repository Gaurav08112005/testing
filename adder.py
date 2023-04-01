import csv
import os.path
from pyrogram import Client

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = int(config[0].split('=')[1].strip())
api_hash = config[1].split('=')[1].strip()

# Create a session folder if it doesn't already exist
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# Load phone numbers from csv file
with open('phone.csv') as f:
    phones = f.read().splitlines()

# Get the group CSV files
group_files = [filename for filename in os.listdir('groups') if filename.endswith('.csv')]

# Check if there are multiple group CSV files
if len(group_files) == 1:
    # Use the only group CSV file if there's only one
    group_file = group_files[0]
else:
    # Ask the user to select a group CSV file if there are multiple
    print("Multiple group CSV files found:")
    for i, filename in enumerate(group_files):
        print(f"{i+1}. {filename}")
    choice = int(input("Enter the number of the group to add members to: "))
    group_file = group_files[choice-1]

# Get the group ID from the group CSV file name
group_id = int(group_file.split('_')[0])

# Load members from the CSV file
members = []
with open(f'groups/{group_file}') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for row in reader:
        members.append(row[0])

for phone_number in phones:
    # Log in and save the session file
    session_name = f'sessions/{phone_number}'
    with Client(session_name, api_id, api_hash) as client:
        client.start()
        print(f"Session file saved for {phone_number} in {session_name}")

        # Add members to the group
        for member in members:
            try:
                client.add_chat_members(group_id, member)
                print(f"Added member {member} to group {group_id} using {phone_number}")
            except Exception as e:
                print(f"Error adding member {member} to group {group_id} using {phone_number}: {str(e)}")

print("Members added to the group.")
