#!/usr/bin/env python
from ssh_server_monitor_crew.crew import ServerMonitorCrew

def run():
    # Inputs will be defined here later, specifying server details
    inputs = {
        'ssh_host': 'YOUR_SERVER_IP',
        'ssh_port': 22,
        'ssh_username': 'YOUR_USERNAME',
        'ssh_password': 'YOUR_PASSWORD', # or None if using key
        'ssh_private_key_path': None # or '/path/to/your/key'
    }
    ServerMonitorCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
