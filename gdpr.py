import getpass
import requests
import json


# search jamf pro users
def search_user(api_url, api_auth, search_username):
    jss_users_api = api_url + '/users/name/' + search_username
    jss_users_response = requests.get(jss_users_api, auth=api_auth, headers={'Accept': 'application/json'})

    if jss_users_response.status_code == 200:
        jss_user = jss_users_response.json()
        print('User found')
        return jss_user['user']


# search jamf pro accounts
def search_account(api_url, api_auth, search_username):
    jss_account_api = api_url + '/accounts/username/' + search_username
    jss_account_response = requests.get(jss_account_api, auth=api_auth, headers={'Accept': 'application/json'})

    if jss_account_response.status_code == 200:
        jss_account = jss_account_response.json()
        print('Account found')
        return jss_account['account']


# search ldap user accounts
def search_ldap_account(api_url, api_auth, search_username):
    ldap_servers_url = api_url + '/ldapservers'
    ldap_servers_response = requests.get(ldap_servers_url, auth=api_auth, headers={'Accept': 'application/json'})

    if ldap_servers_response.status_code == 200:
        ldap_servers = ldap_servers_response.json()
        servers = ldap_servers['ldap_servers']

        ldap_results = []
        for server in servers:
            ldap_server_id = str(server['id'])
            ldap_server_search_url = api_url + '/ldapservers/id/' + ldap_server_id + '/user/' + search_username
            ldap_server_search_response = requests.get(ldap_server_search_url, auth=api_auth, headers={'Accept': 'application/json'})

            if ldap_server_search_response.status_code == 200:
                ldap_server_search_response_json = ldap_server_search_response.json()
                ldap_results.append({server['name']: ldap_server_search_response_json['ldap_users']})
                print('LDAP account found on: ' + server['name'])

        if len(ldap_results) > 0:
            return ldap_results


# get user's mobile devices
def get_mobile_devices(api_url, api_auth, devices):
    mobile_devices = []
    for device in devices:
        device_api_url = api_url + '/mobiledevices/id/' + str(device['id'])
        device_response = requests.get(device_api_url, auth=api_auth, headers={'Accept': 'application/json'})
        device_response_json = device_response.json()
        mobile_devices.append(device_response_json['mobile_device'])

    if len(mobile_devices) > 0:
        print(str(len(mobile_devices)) + ' mobile devices found')
        return mobile_devices


# get user's computers
def get_computers(api_url, api_auth, devices):
    computers = []
    for device in devices:
        device_api_url = api_url + '/computers/id/' + str(device['id'])
        device_response = requests.get(device_api_url, auth=api_auth, headers={'Accept': 'application/json'})
        device_response_json = device_response.json()
        computers.append(device_response_json['computer'])

    if len(computers) > 0:
        print(str(len(computers)) + ' computers found')
        return computers


def main():
    print("GDPR")

    instance = input("Jamf Pro URL:")
    username = input("Jamf Pro Username:")
    password = getpass.getpass("Jamf Pro Password:")

    api_url = 'https://' + instance + '/JSSResource'
    api_auth = (username, password)

    loop = True
    while loop:
        user_data = {}

        search_username = input("Search Username:")

        account_result = search_account(api_url, api_auth, search_username)
        if account_result is not None:
            user_data['account'] = account_result

        ldap_result = search_ldap_account(api_url, api_auth, search_username)
        if ldap_result is not None:
            user_data['ldap'] = ldap_result

        user_result = search_user(api_url, api_auth, search_username)
        if user_result is not None:
            user_data['user'] = user_result

            mobile_devices = user_data['user']['links']['mobile_devices']
            mobile_devices_result = get_mobile_devices(api_url, api_auth, mobile_devices)
            if mobile_devices_result is not None:
                user_data['devices'] = mobile_devices_result

            computers = user_data['user']['links']['computers']
            computers_result = get_computers(api_url, api_auth, computers)
            if computers_result is not None:
                user_data['computers'] = computers_result

        # only write to file if data exists
        if user_data:
            file_name = instance + '_' + search_username + '.json'
            file = open(file_name, 'w')
            file_contents = json.dumps(user_data)
            file.write(file_contents)
            file.close()
            print('Saved: ' + file_name)
        else:
            print('No results found for: ' + search_username)

        again = input('Search new user?: [y/n] ')
        if again == 'n':
            loop = False


if __name__ == '__main__':
    main()
