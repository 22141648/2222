from netmiko import ConnectHandler
import difflib

def get_running_config(device_params):
    # Connect to the device and retrieve the running configuration
    connection = ConnectHandler(**device_params)
    connection.enable()
    running_config = connection.send_command("show running-config")
    connection.disconnect()
    return running_config

def compare_config(running_config, hardening_config_file):
    # Read hardening recommendations from file
    with open(hardening_config_file, "r") as file:
        hardening_config = file.read()
    
    # Compare configurations
    diff = difflib.unified_diff(
        hardening_config.splitlines(),
        running_config.splitlines(),
        fromfile="Hardening Config",
        tofile="Running Config",
        lineterm=""
    )
    comparison_result = "\n".join(diff)
    
    if comparison_result:
        print("Differences found between running configuration and hardening recommendations:")
        print(comparison_result)
        with open("config_comparison_report.txt", "w") as report:
            report.write(comparison_result)
        print("Comparison report saved to config_comparison_report.txt")
    else:
        print("The running configuration matches the hardening recommendations.")

def configure_syslog(device_params, syslog_server_ip):
    # Connect to the device and configure syslog
    connection = ConnectHandler(**device_params)
    connection.enable()
    
    # Syslog configuration commands
    syslog_commands = [
        "configure terminal",
        f"logging host {syslog_server_ip}",
        "logging trap informational",
        "end"
    ]
    connection.send_config_set(syslog_commands)
    print(f"Syslog configured with server {syslog_server_ip}")
    
    # Close the connection
    connection.disconnect()

# Device connection details
device_params = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

# Path to the Cisco hardening recommendations file
hardening_config_file = "cisco_hardening_config.txt"

# Syslog server IP address
syslog_server_ip = "192.168.1.100"

# Retrieve the running config
running_config = get_running_config(device_params)

# Compare the running config against the hardening recommendations
compare_config(running_config, hardening_config_file)

# Configure syslog on the device
configure_syslog(device_params, syslog_server_ip)
