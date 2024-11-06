import difflib
from netmiko import ConnectHandler

# Device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # IP address of the Cisco device
    'username': 'cisco',       # Username
    'password': 'cisco',       # Password
    'secret': 'cisco'          # Enable password
}

def connect_to_device(device):
    """
    Establish SSH connection to the device.
    """
    connection = ConnectHandler(**device)
    connection.enable()
    return connection

def get_running_config(connection):
    """
    Retrieve the running configuration from the device.
    """
    return connection.send_command("show running-config")

def compare_with_hardening_guide(running_config, hardening_guide_file):
    """
    Compare the running configuration with Cisco hardening advice.
    """
    with open(hardening_guide_file, 'r') as file:
        hardening_guide = file.read()

    # Generate and display differences
    diff = difflib.unified_diff(
        running_config.splitlines(),
        hardening_guide.splitlines(),
        fromfile="Running Config",
        tofile="Hardening Guide",
        lineterm=''
    )

    differences = '\n'.join(diff)
    if differences:
        print("\nDifferences between Running Config and Hardening Guide:\n")
        print(differences)
    else:
        print("No differences found between the running config and hardening guide.")

def enable_syslog(connection, syslog_server="192.168.56.102"):
    """
    Configure the network device to enable syslog for event logging.
    """
    syslog_config = [
        f"logging host {syslog_server}",
        "logging trap informational"
    ]
    connection.send_config_set(syslog_config)
    print(f"Syslog configured to log to {syslog_server}")

# Main function to execute the tasks
def main():
    # Connect to the device
    connection = connect_to_device(device)

    # Task 1: Compare running-config with Cisco hardening guide
    running_config = get_running_config(connection)
    hardening_guide_file = "cisco_hardening_guide.txt"  # Path to your hardening guide
    compare_with_hardening_guide(running_config, hardening_guide_file)

    # Task 2: Enable Syslog
    syslog_server = "192.168.56.102"  # IP address of your syslog server
    enable_syslog(connection, syslog_server)

    # Disconnect from the device
    connection.disconnect()

if __name__ == "__main__":
    main()
