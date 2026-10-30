from db import check_connection, fetch_members

print(check_connection())

members = fetch_members()

for member in members:
    print(member)