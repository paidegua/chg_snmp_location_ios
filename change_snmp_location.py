# Python Script used to update the SNMP location on Cisco IOS devices.
# Date March 31 2020 using MS Visual Studio
# Contributors on GitHub, shepherdjay, sudoursa and paidegua

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
import csv
import getpass

# Prompt user for credentials
# Creds are stored for use during the device configuration phase
username = getpass.getuser()
password = getpass.getpass()

# Define the Commands to run on the cisco device
def update_snmp_location(username, password, ip_address, new_location):
    device = {
        "device_type": 'cisco_ios',
        "host": ip_address,
        "username": username,
        "password": password,
    }
    net_connect = ConnectHandler(**device)

    net_connect.find_prompt()

    output = net_connect.send_command("show run | inc snmp-server location")

    print(output)

    config_commands = [f'snmp-server location {new_location}']

    output = net_connect.send_config_set(config_commands)

    print(output)

    output = net_connect.send_command("show run | inc snmp-server location")

    print(output)

    net_connect.save_config()

# Read and append the CSV file to define the IP and SNMP Location of the device.
list_of_devices = []

with open(r'C:\Users\lajeff\PycharmProjects\Cisco_Automation\devices.csv') as File:
	reader = csv.DictReader(File, delimiter=';')
	for row in reader:
		list_of_devices.append(row)

# Execute the script function to update the devices
# Actions for exceptions (errors) defined
for device in list_of_devices:
    try:
       update_snmp_location(ip_address=device['ip'],username=username,password=password,new_location=device['location'])
    except NetmikoTimeoutException:
        print(f"Device {device['ip']} failed with Timeout")
    except NetmikoAuthenticationException as e:
        print(e)

print("Done, Finished, Finite, Termina")
