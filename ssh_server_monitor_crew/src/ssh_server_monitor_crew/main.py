#!/usr/bin/env python
from ssh_server_monitor_crew.crew import ServerMonitorCrew
import pandas as pd
import os
import math # For math.isnan
import asyncio
import concurrent.futures
import traceback # Added import
import ast # Added import

# Global variable to store results for the next step (consolidated reporting)
# Defined here so it's accessible by run() and also by the main block if needed before run()
global_results_for_reporting = []

# Helper function to run a single crew instance (synchronous)
def run_crew_for_server(server_inputs):
    hostname = server_inputs.get('hostname_for_reporting', server_inputs.get('ssh_host'))
    print(f"Initiating data collection for server: {hostname} ({server_inputs.get('ssh_host')})...")
    try:
        crew_instance = ServerMonitorCrew()
        monitor_task_object = crew_instance.monitor_task()

        crew_to_run = crew_instance.crew(specific_tasks=(monitor_task_object,))
        server_data_kickoff_output = crew_to_run.kickoff(inputs=server_inputs) # This is a CrewOutput object

        extracted_data = None
        if server_data_kickoff_output and hasattr(server_data_kickoff_output, 'tasks_output') and server_data_kickoff_output.tasks_output:
            task_output = server_data_kickoff_output.tasks_output[0] # We ran only one task
            raw_string_output = task_output.raw

            if raw_string_output:
                try:
                    extracted_data = ast.literal_eval(raw_string_output)
                    if not isinstance(extracted_data, dict):
                        print(f"Warning: Parsed output for {hostname} is not a dict (type: {type(extracted_data)}). Raw: {raw_string_output[:200]}...")
                        extracted_data = {'parsing_issue': f'Expected dict, got {type(extracted_data)}', 'raw_content': raw_string_output}
                except (ValueError, SyntaxError) as e:
                    print(f"Warning: Could not parse raw_output for {hostname} as dict ('{str(e)}'). Using raw string. Raw: {raw_string_output[:200]}...")
                    extracted_data = {'parsing_error': f'Could not parse as dict: {str(e)}', 'raw_content': raw_string_output}
            else:
                extracted_data = {'error': f'Task output (raw) was empty or None for server {hostname}.'}

        elif server_data_kickoff_output and hasattr(server_data_kickoff_output, 'raw_output') and server_data_kickoff_output.raw_output:
            raw_string_output = server_data_kickoff_output.raw_output
            print(f"Warning: Using CrewOutput.raw_output for {hostname}. Raw: {raw_string_output[:200]}...")
            try:
                extracted_data = ast.literal_eval(raw_string_output)
                if not isinstance(extracted_data, dict):
                     extracted_data = {'parsing_issue': f'Expected dict from CrewOutput.raw_output, got {type(extracted_data)}', 'raw_content': raw_string_output}
            except (ValueError, SyntaxError) as e:
                 extracted_data = {'parsing_error': f'Could not parse CrewOutput.raw_output as dict for {hostname}: {str(e)}', 'raw_content': raw_string_output}
        else:
            extracted_data = {'error': f'No valid output (tasks_output or raw_output) from crew execution for server {hostname}.'}

        print(f"Data collection finished for {hostname}. Extracted data type: {type(extracted_data)}. Data snippet: {str(extracted_data)[:200]}...")
        return {'hostname': hostname, 'data': extracted_data}

    except Exception as e:
        print(f"--- Error processing server {hostname} ---")
        traceback.print_exc()
        error_message = f'Failed to process server {hostname} during crew kickoff or data extraction due to: {str(e)}'
        return {'hostname': hostname, 'data': {'error': error_message, 'details': str(e), 'traceback': traceback.format_exc()}}

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

    all_server_inputs_for_processing = []
    skipped_servers_info = []
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

        inputs_for_this_server = {
            'ssh_host': ip_address,
            'ssh_port': 22,
            'ssh_username': username,
            'ssh_password': password,
            'ssh_private_key_path': None,
            'hostname_for_reporting': hostname
        }
        all_server_inputs_for_processing.append(inputs_for_this_server)
    # End of Excel reading and input prep

    current_results = [] # Use a local variable within run()
    current_results.extend(skipped_servers_info) # Add info about servers skipped due to bad input

    if not all_server_inputs_for_processing:
        print("No valid server configurations found in Excel to process for data collection.")
    else:
        max_workers = min(len(all_server_inputs_for_processing), 10)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            loop = asyncio.get_event_loop()
            async_tasks = [loop.run_in_executor(executor, run_crew_for_server, server_input_data) for server_input_data in all_server_inputs_for_processing]

            results_from_tasks = await asyncio.gather(*async_tasks)
            current_results.extend(results_from_tasks)

    global_results_for_reporting = current_results # Assign to global variable at the end

    print("\n--- Aggregated Server Results (for debugging/next step) ---")
    # for result in global_results_for_reporting:
    #     print(f"Hostname: {result.get('hostname')}, Data: {result.get('data')}")

    print(f"\nConcurrent processing complete. {len(df)} server(s) read from Excel, {len(global_results_for_reporting)} result entries obtained (includes skipped/errors).")
    # Note: The 'server_status_report.md' is no longer overwritten by each server's individual report task
    # because only monitor_task is run per server. The consolidated report is generated next.

    print("\n--- Initiating Consolidated Report Generation ---")
    if global_results_for_reporting:
        report_inputs = {
            'server_data_list': global_results_for_reporting,
        }

        print("Passing aggregated data to the reporting agent...")
        try:
            reporting_crew_instance = ServerMonitorCrew()
            generate_report_task_object = reporting_crew_instance.generate_report_task() # Get task object

            # Create crew with ONLY the generate_report_task
            report_crew_object = reporting_crew_instance.crew(specific_tasks=(generate_report_task_object,))
            final_report_status = report_crew_object.kickoff(inputs=report_inputs)

            print(f"Consolidated report generation complete. Report saved to 'server_status_report.md'.")
            # print(f"Final report content preview (first 500 chars):\n{final_report_status[:500]}")
        except Exception as e:
            print("--- Error during consolidated report generation ---")
            traceback.print_exc() # Add this line
            # print(f"Error during consolidated report generation: {str(e)}") # Redundant
            # For debugging, print the type of data being passed if error persists
            if 'server_data_list' in report_inputs:
                for item_idx, item in enumerate(report_inputs['server_data_list']):
                    if 'data' in item and not isinstance(item['data'], (dict, str, int, float, bool, list, type(None))): # Allow NoneType as well
                         print(f"Item {item_idx} ('{item.get('hostname')}') in server_data_list has problematic type for 'data': {type(item['data'])}")
    else:
        print("No server data collected or all servers skipped, skipping consolidated report generation.")

if __name__ == "__main__":
    # global_results_for_reporting is already defined at the module level
    asyncio.run(run())
