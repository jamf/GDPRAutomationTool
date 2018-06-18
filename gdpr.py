import sys
import getpass
import requests
import json

instance = input("Jamf Pro URL:")
username = input("Jamf Pro Username:")
password = getpass.getpass("Jamf Pro Password:")

api_url = 'https://'+instance+'/JSSResource'

loop = True
while loop:
	user_data = {}
	search_username = input("Search Username:")

	# search jamf pro users
	jss_users_api = api_url+'/users/name/'+search_username
	jss_users_response = requests.get(jss_users_api, auth=(username, password), headers={'Accept': 'application/json'})

	if jss_users_response.status_code == 200:
		jss_user = jss_users_response.json()
		user_data['user'] = jss_user['user']
		print('User found')

		# user's mobile devices
		mobile_devices = []
		for device in jss_user['user']['links']['mobile_devices']:
			device_api_url = api_url+'/mobiledevices/id/'+str(device['id'])
			device_response = requests.get(device_api_url, auth=(username, password), headers={'Accept': 'application/json'})
			device_response_json = device_response.json()
			mobile_devices.append(device_response_json['mobile_device'])

		if len(mobile_devices) > 0:
			user_data['devices'] = mobile_devices
			print(str(len(mobile_devices))+' mobile devices found')

		# user's computers
		computers = []
		for device in jss_user['user']['links']['computers']:
			device_api_url = api_url+'/computers/id/'+str(device['id'])
			device_response = requests.get(device_api_url, auth=(username, password), headers={'Accept': 'application/json'})
			device_response_json = device_response.json()
			computers.append(device_response_json['computer'])

		if len(computers) > 0:
			user_data['computers'] = computers
			print(str(len(computers))+' computers found')

	# search jamf pro user accounts
	jss_account_api=api_url+'/accounts/username/'+search_username
	jss_account_response = requests.get(jss_account_api, auth=(username, password), headers={'Accept': 'application/json'})

	if jss_account_response.status_code == 200:
		jss_account = jss_account_response.json()
		user_data['account'] = jss_account['account']
		print(jss_account)

	# search ldap user accounts
	ldap_servers_url = api_url+'/ldapservers'
	ldap_servers_response = requests.get(ldap_servers_url, auth=(username, password), headers={'Accept': 'application/json'})

	if ldap_servers_response.status_code == 200:
		ldap_servers = ldap_servers_response.json()
		servers = ldap_servers['ldap_servers']

		ldap_results = []
		for server in servers:
			ldap_server_id = str(server['id'])
			ldap_server_search_url = api_url+'/ldapservers/id/'+ldap_server_id+'/user/'+search_username
			ldap_server_search_response = requests.get(ldap_server_search_url, auth=(username, password), headers={'Accept': 'application/json'})

			if ldap_server_search_response.status_code == 200:
				ldap_server_search_response_json = ldap_server_search_response.json()
				ldap_results.append({server['name']: ldap_server_search_response_json['ldap_users']})
				print('LDAP account found on: '+server['name'])

	if len(ldap_results) > 0:
		user_data['ldap'] = ldap_results

	# only write to file if data exists
	if user_data:
		file_name = instance+'_'+search_username+'.json'
		file = open(file_name, 'w')
		file_contents = json.dumps(user_data)
		file.write(file_contents)
		file.close()
		print('Saved: '+file_name)
	else:
		print('No results found for: '+search_username)

	again = input('Search new user?: [y/n] ')
	if again == 'n':
		loop = False
