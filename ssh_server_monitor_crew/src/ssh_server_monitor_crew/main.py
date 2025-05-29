#!/usr/bin/env python
from ssh_server_monitor_crew.crew import ServerMonitorCrew
import pandas as pd
import os
import math # For math.isnan
import asyncio
import concurrent.futures

# Global variable to store results for the next step (consolidated reporting)
global_results_for_reporting = []

# Helper function to run a single crew instance (synchronous)
def run_crew_for_server(server_inputs):
    hostname = server_inputs.get('hostname_for_reporting', server_inputs.get('ssh_host'))
    print(f"Initiating data collection for server: {hostname} ({server_inputs.get('ssh_host')})...")
    try:
        crew_instance = ServerMonitorCrew()
        # This kickoff is synchronous. It will block this thread, but other threads in the pool can run.
        server_data_output = crew_instance.crew().kickoff(inputs=server_inputs)
        print(f"Data collection finished for {hostname}.")
        return {'hostname': hostname, 'data': server_data_output}
    except Exception as e:
        error_message = f'Failed to process server {hostname} due to: {str(e)}'
        print(error_message)
        return {'hostname': hostname, 'data': {'error': error_message}}

async def run():
    global global_results_for_reporting # Allow assignment to the global variable

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    excel_file_path = os.path.join(project_root, 'servers.xlsx')

    if not os.path.exists(excel_file_path):
        print(f"Error: Excel file not found at {excel_file_path}")
        print("Please create 'servers.xlsx' in the project root directory (ssh_server_monitor_crew/) with columns: hostname, ip_address, username, password.")
        return

    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    required_columns = ['hostname', 'ip_address', 'username', 'password']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Excel file ('{excel_file_path}') must contain the columns: {', '.join(required_columns)}")
        return
    
    print(f"Found {len(df)} servers in '{os.path.basename(excel_file_path)}'. Starting concurrent processing...")
    
    all_server_inputs = []
    skipped_servers_info = [] # To store info about servers skipped before processing
    for index, row in df.iterrows():
        hostname = str(row['hostname']).strip()
        ip_address = str(row['ip_address']).strip()
        username = str(row['username']).strip()
        password_val = row['password']
        password = None if (pd.isna(password_val) or (isinstance(password_val, float) and math.isnan(password_val)) or str(password_val).strip() == "") else str(password_val)

        if not ip_address or not username:
            print(f"Skipping server {hostname} due to missing IP address or username in Excel row.")
            skipped_servers_info.append({'hostname': hostname, 'data': {'error': 'Missing IP address or username in Excel row.'}})
            continue

        inputs = {
            'ssh_host': ip_address,
            'ssh_port': 22,
            'ssh_username': username,
            'ssh_password': password,
            'ssh_private_key_path': None, 
            'hostname_for_reporting': hostname 
        }
        all_server_inputs.append(inputs)

    current_results = [] # Use a local variable within run()
    current_results.extend(skipped_servers_info) # Add info about servers skipped due to bad input

    if not all_server_inputs: # Check if there are any valid server inputs to process
        print("No valid server configurations found in Excel to process.")
    else:
        max_workers = min(len(all_server_inputs), 10) 
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(executor, run_crew_for_server, server_input_data) for server_input_data in all_server_inputs]
            
            results_from_tasks = await asyncio.gather(*tasks)
            current_results.extend(results_from_tasks)

    global_results_for_reporting = current_results # Assign to global variable at the end

    print("\n--- Aggregated Server Results (for debugging/next step) ---")
    # for result in global_results_for_reporting:
    #     print(f"Hostname: {result.get('hostname')}, Data: {result.get('data')}")

    print(f"\nConcurrent processing complete. {len(df)} server(s) read from Excel, {len(global_results_for_reporting)} result entries obtained (includes skipped/errors).")
    print("The current 'server_status_report.md' is likely overwritten by the last processed server by the existing crew structure.")
    print("This will be addressed in the consolidated reporting step.")

    print("\n--- Initiating Consolidated Report Generation ---")
    if global_results_for_reporting:
        # Prepare inputs for the consolidated reporting task
        # The 'generate_report_task' will be updated to handle this structure.
        report_inputs = {
            'server_data_list': global_results_for_reporting,
            # We might not need other ssh_ specific inputs here if the task
            # is purely about formatting the already collected data.
            # The task description for 'generate_report_task' will guide the agent.
        }
        
        print("Passing aggregated data to the reporting agent...")
        try:
            # We use the same crew structure. The agent/task logic will differentiate.
            # The 'generate_report_task' in tasks.yaml will be updated to expect 'server_data_list'.
            # Its output_file is already server_status_report.md
            reporting_crew = ServerMonitorCrew() # Fresh instance for clarity or can reuse
            final_report_status = reporting_crew.crew().kickoff(inputs=report_inputs)
            
            # The kickoff for a task that specifies output_file usually returns the content of the file.
            print(f"Consolidated report generation complete. Report saved to 'server_status_report.md'.")
            # print(f"Final report content preview (first 500 chars):\n{final_report_status[:500]}") 
        except Exception as e:
            print(f"Error during consolidated report generation: {e}")
    else:
        print("No server data collected, skipping consolidated report generation.")

if __name__ == "__main__":
    asyncio.run(run())
