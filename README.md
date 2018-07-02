GDPR Script

This script is used to gather all personal information related to a specific user within Jamf Pro along with any devices their account is tied to as they may also contain more personal information.

Locations where personal information can be found in the API & Required Jamf Pro account permissions in order to retrieve all data:

| Resource                             | Permission |
| ------------------------------------ | ------------------------------- |
| /accounts/username/[username]        | Jamf Pro User Accounts & Groups |
| /ldapservers/id/[id]/user/[username] | LDAP Servers |
| /users/name/[username]               | Users |
| /computers/id/[id]                   | Computers |
| /mobiledevices/id/[id]               | Mobile Devices |

The script looks through these API endpoints for a specified username and outputs the results to a JSON file.

In order to run the script you must have a Jamf Pro account with permissions to access the API.

When running the script, it will ask for the Jamf Pro instance you want to get information out of along with an account to be used to authenticate and access the API with. You will then will be prompted to enter a username to search for and if results are found the will be saved to a file.

Example running:
```
$ python3 gdpr.py

Jamf Pro URL:example-url.com
Jamf Pro Username:admin
Jamf Pro Password:********
Search Username:username
User found
LDAP account found on: ldap.server.com
2 mobile devices found
2 computers found
Saved: example-url.com_username.json
Search new user?: [y/n] n
```
