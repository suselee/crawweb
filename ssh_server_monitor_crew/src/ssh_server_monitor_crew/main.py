#!/usr/bin/env python
from ssh_server_monitor_crew.crew import ServerMonitorCrew

def run():
    # Inputs will be defined here later, specifying server details
    inputs = {
        'ssh_host': '192.168.0.155',
        'ssh_port': 22,
        'ssh_username': 'topwalk',
        'ssh_password': 'topwalk123', # or None if using key
        'ssh_private_key_path': None # or '/path/to/your/key'
    }
    ServerMonitorCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
