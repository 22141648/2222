from netmiko import ConnectHandler

# Define device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',     # Update with your device's IP
    'username': 'cisco',          # Update with your username
    'password': 'cisco',          # Update with your password
    'secret': 'cisco',            # Enable password
}

# Hardening configuration recommendations
recommended_configurations = [
    "ip access-list extended INFRASTRUCTURE_ACL",
    "permit tcp host 192.168.56.10 any eq 22",      # Example SSH access
    "permit tcp host 192.168.56.10 any eq 443",     # Example HTTPS access
    "permit icmp any any echo-reply",               # ICMP Packet Filtering
    "deny icmp any any",                            # Deny other ICMP
    "deny ip any any fragments",                    # Filter IP Fragments
    "deny ip any any option-type 1",                # Filter IP Options
    "deny ip any any ttl eq 1",                     # Filter on TTL Value
    "permit ip any any",                            # Permit remaining traffic
]

# Syslog configuration commands
syslog_commands = [
    "logging host 192.168.56.200",  # Replace with your syslog server IP
    "logging trap informational",
    "logging on"
]

# Function to connect and retrieve the running configuration
def get_running_config(device):
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        running_config = connection.send_command("show running-config")
        connection.disconnect()
        return running_config.splitlines()
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

# Function to load hardening advice from file
def load_hardening_standard(filename="hardening_advice.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Hardening file '{filename}' not found.")
        return None

# Function to compare configurations and identify missing commands
def compare_configs(running_config, recommendations):
    missing_config = [cmd for cmd in recommendations if cmd not in running_config]
    if missing_config:
        print("The following recommended configurations are missing:")
        for line in missing_config:
            print(line)
    else:
        print("Running configuration meets hardening standards.")
    return missing_config

# Function to apply missing configurations to the device
def apply_missing_config(device, missing_config):
    if not missing_config:
        print("No configuration changes needed.")
        return
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        output = connection.send_config_set(missing_config)
        connection.disconnect()
        print("Missing configurations applied successfully.")
        print(output)
    except Exception as e:
        print(f"Error applying configurations: {e}")

# Function to configure syslog on the device
def configure_syslog(device, syslog_commands):
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        output = connection.send_config_set(syslog_commands)
        connection.disconnect()
        print("Syslog configuration applied successfully.")
        print(output)
    except Exception as e:
        print(f"Error configuring syslog: {e}")

# Main program execution
if __name__ == "__main__":
    # Step 1: Retrieve running config
    running_config = get_running_config(device)
    if not running_config:
        exit("Failed to retrieve running configuration. Exiting.")
    
    # Step 2: Compare with hardening recommendations
    missing_config = compare_configs(running_config, recommended_configurations)
    
    # Step 3: Apply missing configurations if needed
    if missing_config:
        apply_missing_config(device, missing_config)
    
    # Step 4: Configure syslog for event logging and monitoring
    configure_syslog(device, syslog_commands)
