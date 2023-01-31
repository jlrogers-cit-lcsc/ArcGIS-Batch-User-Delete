# (REQUIRED) Establishes a 60-minute authenticated session to an arcgis.com portal

# Import only needed modules from arcgis.gis library for leaner cleaner code
from arcgis.gis import GIS
from arcgis.gis import RoleManager
from arcgis.gis import UserManager

# TO-DO: Implement a loading animation for logins and queries

try:
    portal_url = str(input('Enter AGOL url [https://lcsc.maps.arcgis.com]: ') or 'https://lcsc.maps.arcgis.com')
    user_name = input('Enter username: ')
    gis = GIS('https://lcsc.maps.arcgis.com', user_name)
    print(f'Successfully logged in as: {gis.properties.user.username}')
    print(f'Welcome to {gis.properties.name} ({gis.properties.portalName} {gis.properties.currentVersion})!')
except Exception as e:
    print(e)

# (REQUIRED) Sets up role and user management then compiles a list of all user objects

# Instantiate the RoleManager class on the AGOL connection to retrieve and manage roles
role_mgr = RoleManager(gis)

# RoleId of the role we want to manage
role_id = 'sDz0Iq02sOgMtUkR'

# Use the RoleId to retrieve and save the role as an object for use later
role_obj = role_mgr.get_role(role_id)

# Instantiate the UserManager class on the AGOL connection to retrieve and manage users
user_mgr = UserManager(gis)

# Retrieve the total users in the organization for efficient searching later
# gis.users.search() returns a max of 100 users by default, this overcomes that limitation
num_users = user_mgr.counts('user_type', as_df=False)

# Create a list of all users assigned the role we want to manage
# Searching takes a long time, prepared to wait
users = [user for user in user_mgr.search(query=None, max_users=num_users[0]['count'])]

# (OPTIONAL)
# Retrieve all roles in the AGOL organization
roles = role_mgr.all()

# Display all role IDs and names.
print(f'{"[Role ID]":16} | {"[NAME]"}')
for role in roles:
    print(f'{getattr(role, "role_id", "ROLE ID NOT FOUND"):16} | {getattr(role, "name", "ROLE NAME NOT FOUND")}')
        
# Display the human-readable name of the role set under the role_id variable in the second cell 
print(f'\nRole to Manage: {getattr(role_obj, "name", "ROLE NAME NOT FOUND")} ({getattr(role_obj, "role_id", "ROLE ID NOT FOUND")})\nDescription: {getattr(role_obj, "description", "ROLE DESCRIPTION NOT FOUND")}')

# (OPTIONAL) Display all users in the AGOL organization in csv format
# TO-DO option to export this list to a csv file, as it is, copy and paste
print(f'Total Users: {num_users[0]["count"]}\n')
print("id,fullName,username,email,role")
for user in users:
    print(f'{getattr(user, "id", "NOT FOUND")},{getattr(user, "fullName", "NOT FOUND")},{getattr(user, "username", "NOT FOUND")},{getattr(user, "email", "NOT FOUND")},{getattr(user, "role", "NOT FOUND")}')

# (REQUIRED) Displays all users with the role to delete

# Populate a list of users who have the roleId matching that we want to delete
users_to_delete = [user for user in users if user.roleId == role_id]

# Display a count of the users with the role to delete and 
print(f'Total users with role {role_id}: {len(users_to_delete)}\n')
for user in users_to_delete:
    print('{0}\n{2}\n'.format(
        getattr(user, 'fullName', 'NOT FOUND'),
        getattr(user, 'username', 'NOT FOUND'),
        getattr(user, 'email', 'NOT FOUND'),
        getattr(user, 'role', 'NOT FOUND')))

# Run this cell to delete all users with the role_id set in the second cell
# WARNING!!! ONLY DO THIS IF YOU'VE VERIFIED THE LIST OF USERS IN THE CELL ABOVE!!!

for user in users_to_delete:
    try:
        print(f'Deleting: {user.username}')
        user.delete(reassign_to='LCSCGIS')
        print(f'Successfully deleted: {user.username}')
    except Exception as e:
        print(e)
print('Done!')
