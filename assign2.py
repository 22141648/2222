import re
from netmiko import ConnectHandler

# Define the Cisco device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # IP address of the Cisco device
    'username': 'cisco',       # Username
    'password': 'cisco',       # Password
    'secret': 'cisco',         # Enable password
}

# Connect to the device
net_connect = ConnectHandler(**device)
net_connect.enable()

# Retrieve the running configuration
running_config = net_connect.send_command('show running-config')

# Cisco hardening checks - basic examples (You can extend this list)
hardening_recommendations = {
    'no-ip-domain-lookup': r'no ip domain-lookup',
    'password-encryption': r'enable secret',  # Check for password encryption
    'banner': r'banner motd',  # Check for banner message
    'logging': r'logging host',  # Ensure syslog is enabled
}

def compare_hardening(running_config, recommendations):
    comparison_results = {}
    
    for key, pattern in recommendations.items():
        match = re.search(pattern, running_config)
        if match:
            comparison_results[key] = 'Configured'
        else:
            comparison_results[key] = 'Not Configured'
    
    return comparison_results

# Compare running config with hardening recommendations
comparison = compare_hardening(running_config, hardening_recommendations)

# Output results
print("Hardening Comparison Results:")
for config, status in comparison.items():
    print(f"{config}: {status}")

# Task 2: Configure Syslog for event logging
syslog_server = '192.168.1.100'  # Replace with the actual syslog server IP
syslog_port = '514'  # Default syslog port

# Configure syslog on the Cisco device
config_commands = [
    f'logging {syslog_server}',
    f'logging trap informational',  # Adjust logging severity level as needed
    f'logging source-interface Vlan1',  # Replace with the correct interface
]

# Send commands to the device
output = net_connect.send_config_set(config_commands)
print("\nSyslog Configuration Output:")
print(output)

# Close the connection
net_connect.disconnect()
