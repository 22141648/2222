from netmiko import ConnectHandler

def ssh_connect_and_configure():
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',  # Enable password
    }

    hardening_template = 'hardening_template.txt'  # File with Cisco hardening recommendations
    syslog_server_ip = '192.168.56.102'  # Replace with your actual syslog server IP

    try:
        # Establish the SSH connection
        net_connect = ConnectHandler(**device)

        # Enter enable mode
        net_connect.enable()

        # Change the hostname
        config_commands = ['hostname SecureRouter']
        net_connect.send_config_set(config_commands)

        # Get the running configuration
        running_config = net_connect.send_command('show running-config')

        # Save running config to a file
        with open('SecureRouter_running_config.txt', 'w') as f:
            f.write(running_config)

        # Compare with the hardening template
        compare_hardening(running_config, hardening_template)

        # Configure syslog server
        configure_syslog(net_connect, syslog_server_ip)

        # Disconnect
        net_connect.disconnect()

        print("Hostname changed, running config saved, hardening comparison complete, and syslog configured.")
    
    except Exception as e:
        print(f"Failed to connect via SSH: {str(e)}")

def compare_hardening(running_config, hardening_template):
    """Compare running config against hardening template."""
    try:
        with open(hardening_template, 'r') as template_file:
            template_lines = template_file.read().splitlines()

        # Check for missing hardening configurations
        missing_config = []
        for line in template_lines:
            if line not in running_config:
                missing_config.append(line)

        # Report missing configuration lines
        if missing_config:
            print("The following hardening configurations are missing:")
            for line in missing_config:
                print(f"- {line}")
        else:
            print("The running configuration complies with the hardening template.")

    except FileNotFoundError:
        print("Hardening template file not found. Please ensure 'hardening_template.txt' exists.")

def configure_syslog(net_connect, syslog_server_ip):
    """Configure syslog server on the device."""
    syslog_commands = [
        f'logging host {syslog_server_ip}',  # Set syslog server IP
        'logging trap informational',       # Set logging level
        'service timestamps log datetime'   # Timestamp log messages
    ]

    # Send configuration to device
    output = net_connect.send_config_set(syslog_commands)
    print("Syslog configuration applied:\n", output)

# Run the SSH connection and configuration
ssh_connect_and_configure()
