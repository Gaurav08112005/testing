import csv
import os
import pyrogram
from pyrogram import Client
from pyrogram.api.errors import Unauthorized

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = config[0]
api_hash = config[1]
phone_number = config[2]

# Create a session folder if it doesn't already exist
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# Start the client session
session_name = f'sessions/{phone_number}'
client = Client(session_name, api_id, api_hash)
client.start(phone_number)

# Get the group ID from the group link
group_link = input("Enter the group link: ")
chat = client.get_chat(group_link)

# Get all members of the group
def get_members(online_filter):
    members = []
    try:
        for member in client.iter_chat_members(chat.id, filter=online_filter):
            members.append(member)
    except Unauthorized:
        client.send_code(phone_number)
        code = input("Enter the code you received: ")
        client.sign_in(phone_number, code)
        for member in client.iter_chat_members(chat.id, filter=online_filter):
            members.append(member)
    return members

# Ask user for filter option
print("Select filter option:")
print("1. Online Users")
print("2. All Users")
option = int(input("Enter your choice: "))

if option == 1:
    online_filter = "online"
else:
    online_filter = None

# Get the members of the group based on the selected filter
members = get_members(online_filter)

# Save the member information to a CSV file with the group title and filter type
filename = f"{chat.title.replace(' ', '_')}_{online_filter or 'all_members'}.csv"
if not os.path.exists('members'):
    os.makedirs('members')
filename = os.path.join('members', filename)
with open(filename, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["User ID", "First Name", "Last Name", "Username"])
    for member in members:
        writer.writerow([member.user.id, member.user.first_name, member.user.last_name, member.user.username])

print(f"Member information saved to {filename}. Total members: {len(members)}")
