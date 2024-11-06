from netmiko import ConnectHandler

def ssh_connect():
    device = {
        'device_type': 'cisco_ios',  # Device type for SSH
        'host': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',  # Enable password
    }

    hardening_checks = [
        'service password-encryption',   # Password encryption should be enabled
        'no ip http server',             # HTTP server should be disabled
        'no ip source-route',            # Source routing should be disabled
        'logging buffered 4096'          # Buffer logging enabled (example)
    ]

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

        # Check running configuration against hardening guidelines
        for check in hardening_checks:
            if check not in running_config:
                print(f"[WARNING] Missing recommended configuration: '{check}'")
            else:
                print(f"[PASSED] Hardening check '{check}' found.")

        # Enable syslog configuration
        syslog_config_commands = [
            'logging host 192.168.56.200',   # Replace with your syslog server IP
            'logging trap informational',    # Set syslog level to informational
            'logging facility local7'        # Use a local facility
        ]
        net_connect.send_config_set(syslog_config_commands)

        print("Syslog configuration commands sent to device.")

        # Save running config to a file
        with open('SecureRouter_running_config.txt', 'w') as f:
            f.write(running_config)

        # Disconnect
        net_connect.disconnect()

        print("Hostname changed to SecureRouter, hardening check complete, and running config saved.")
    
    except Exception as e:
        print(f"Failed to connect via SSH: {str(e)}")

# Run the SSH connection
ssh_connect()
