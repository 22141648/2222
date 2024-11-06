from netmiko import ConnectHandler
import re

# Define device connection details
device = {
    'device_type': 'cisco_ios',  
    'host': '192.168.56.101',    
    'username': 'cisco',        
    'password': 'cisco',       
    'secret': 'cisco',          
}

# Connect to the device
net_connect = ConnectHandler(**device)
net_connect.enable()

# Define the hardening checks and the required configurations
hardening_checks = {
    'password_security': {
        'command': 'show running-config | include password',
        'check': [
            {'regex': r'password\s+.+', 'config': 'enable secret 5 $<secure_password>'}
        ]
    },
    'exec_timeout': {
        'command': 'show running-config | include exec-timeout',
        'check': [
            {'regex': r'exec-timeout\s+\d+\s+\d+', 'config': 'exec-timeout 5 0'}
        ]
    },
    'syslog_config': {
        'command': 'show running-config | include logging',
        'check': [
            {'regex': r'logging\s+\d+\.\d+\.\d+\.\d+', 'config': 'logging 192.168.56.10'}
        ]
    }
}

# Function to check configuration and apply missing hardening settings
def check_and_apply_hardening():
    for key, value in hardening_checks.items():
        print(f"Checking {key}...")
        current_config = net_connect.send_command(value['command'])
        
        for check in value['check']:
            # Check if the regex pattern exists in the current configuration
            match = re.search(check['regex'], current_config)
            
            if not match:
                print(f"{key} is not configured. Applying configuration...")
                # Apply the recommended configuration
                net_connect.send_config_set([check['config']])
                print(f"Applied configuration: {check['config']}")
            else:
                print(f"{key} is already configured.")

# Run the hardening checks and apply configurations
check_and_apply_hardening()

# Enable syslog configuration
print("Configuring syslog...")
syslog_config = hardening_checks['syslog_config']['check'][0]['config']
net_connect.send_config_set([syslog_config])

# Save the configuration
print("Saving the configuration...")
net_connect.send_command('write memory')

# Disconnect from the device
net_connect.disconnect()

print("Network device hardening and syslog configuration completed.")
