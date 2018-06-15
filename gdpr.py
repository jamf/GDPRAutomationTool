import sys
import getpass
import requests

instance=input("Jamf Pro URL:")
username=input("Jamf Pro Username:")
password=getpass.getpass('Jamf Pro Password:')
search_username=input("Search Username:")

api_url = 'https://'+instance+'/JSSResource'

# search jamf pro users
jss_users_api=api_url+'/users/name/'+search_username
jss_users_response = requests.get(jss_users_api, auth=(username, password), headers={'Accept': 'application/json'})

if jss_users_response.status_code == 200:
    jss_user = jss_users_response.json()
    print(jss_user)

# search jamf pro user accounts
jss_account_api=api_url+'/accounts/username/'+search_username
jss_account_response = requests.get(jss_account_api, auth=(username, password), headers={'Accept': 'application/json'})

if jss_account_response.status_code == 200:
    jss_account = jss_account_response.json()
    print(jss_account)

# search ldap user accounts
ldap_servers_url=api_url+'/ldapservers'
ldap_servers_response = requests.get(ldap_servers_url, auth=(username, password), headers={'Accept': 'application/json'})

if ldap_servers_response.status_code == 200:
    ldap_servers = ldap_servers_response.json()
    servers = ldap_servers['ldap_servers']

    for server in servers:
        print(server['name'])
        ldap_server_id = str(server['id'])
        ldap_server_search_url = api_url+'/ldapservers/id/'+ldap_server_id+'/user/'+search_username
        ldap_server_search_response = requests.get(ldap_server_search_url, auth=(username, password), headers={'Accept': 'application/json'})

        if ldap_server_search_response.status_code == 200:
            ldap_server_search_response_json = ldap_server_search_response.json()
            print(ldap_server_search_response_json)
