import sys
import getpass
import requests
import json

instance = input("Jamf Pro URL:")
username = input("Jamf Pro Username:")
password = getpass.getpass("Jamf Pro Password:")

loop = True
while loop:
	search_username = input("Search Username:")

	file_name = instance+'_'+search_username+'.json'
	file = open(file_name, 'w')
	user_data = {}

	api_url = 'https://'+instance+'/JSSResource'

	# search jamf pro users
	jss_users_api = api_url+'/users/name/'+search_username
	jss_users_response = requests.get(jss_users_api, auth=(username, password), headers={'Accept': 'application/json'})

	if jss_users_response.status_code == 200:
		jss_user = jss_users_response.json()
		user_data['user'] = jss_user['user']
		print(jss_user)

		# user's mobile devices
		mobile_devices = []
		for device in jss_user['user']['links']['mobile_devices']:
			print(device['id'])
			device_api_url = api_url+'/mobiledevices/id/'+str(device['id'])
			device_response = requests.get(device_api_url, auth=(username, password), headers={'Accept': 'application/json'})
			device_response_json = device_response.json()
			mobile_devices.append(device_response_json['mobile_device'])

		if len(mobile_devices) > 0:
			user_data['devices'] = mobile_devices

		# user's computers
		computers = []
		for device in jss_user['user']['links']['computers']:
			print(device['id'])
			device_api_url = api_url+'/computers/id/'+str(device['id'])
			device_response = requests.get(device_api_url, auth=(username, password), headers={'Accept': 'application/json'})
			device_response_json = device_response.json()
			computers.append(device_response_json['computer'])

		if len(computers) > 0:
			user_data['computers'] = computers

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
				print(server['name'])
				print(ldap_server_search_response_json['ldap_users'])

	if len(ldap_results) > 0:
		user_data['ldap'] = ldap_results

	file_contents = json.dumps(user_data)
	file.write(file_contents)
	file.close()

	again = input('Search new user?: [y/n] ')
	if again == 'n':
		loop = False
