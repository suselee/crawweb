from typing import Optional, Type, Dict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import paramiko # Needs to be installed: pip install paramiko

class ServerMonitorToolInput(BaseModel):
    """Input schema for ServerMonitorTool."""
    host: str = Field(..., description="Hostname or IP address of the server.")
    port: int = Field(22, description="SSH port on the server.")
    username: str = Field(..., description="Username for SSH login.")
    password: Optional[str] = Field(None, description="Password for SSH login. If not provided, private_key_path must be used.")
    private_key_path: Optional[str] = Field(None, description="Path to the private SSH key. If not provided, password must be used.")

class ServerMonitorTool(BaseTool):
    name: str = "Server System Monitor via SSH"
    description: str = "Connects to a server via SSH to collect CPU, memory, disk, network, and process status. Returns data as a dictionary."
    args_schema: Type[BaseModel] = ServerMonitorToolInput

    def _run(self, **kwargs) -> Dict[str, str]:
        host = kwargs.get("host")
        port = kwargs.get("port", 22) 
        username = kwargs.get("username")
        password = kwargs.get("password")
        private_key_path = kwargs.get("private_key_path")

        if not (password or private_key_path) or (password and private_key_path):
            return {"error": "Please provide either a password or a private key path, not both or neither."}

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server_stats: Dict[str, str] = {}

        try:
            connect_args = {
                "hostname": host,
                "port": port,
                "username": username,
                "timeout": 10 
            }
            if private_key_path:
                try:
                    pkey = paramiko.RSAKey.from_private_key_file(private_key_path)
                    connect_args["pkey"] = pkey
                except paramiko.PasswordRequiredException:
                    # client.close() # Client not connected yet
                    return {"error": f"Private key file at {private_key_path} is encrypted and requires a passphrase (not supported)."}
                except FileNotFoundError:
                     # client.close() # Client not connected yet
                     return {"error": f"Private key file not found at {private_key_path}."}
                except Exception as e: # Catch other key-related errors
                    return {"error": f"Error with private key {private_key_path}: {str(e)}"}
            else:
                connect_args["password"] = password
            
            client.connect(**connect_args)
            
            # CPU Usage
            cpu_command = "vmstat 1 2 | tail -1 | awk '{print 100-($15+$16)}'"
            stdin, stdout, stderr = client.exec_command(cpu_command)
            cpu_usage = stdout.read().decode().strip()
            cpu_err = stderr.read().decode().strip()
            server_stats['cpu_usage_percentage'] = cpu_usage if cpu_usage and not cpu_err else "N/A"
            if cpu_err: server_stats['cpu_error'] = cpu_err
            
            # Memory Usage
            mem_command = "free -m | awk '/Mem:/ {printf \"total: %sMB, used: %sMB, free: %sMB, available: %sMB\", $2, $3, $4, $7}'"
            stdin, stdout, stderr = client.exec_command(mem_command)
            mem_usage = stdout.read().decode().strip()
            mem_err = stderr.read().decode().strip()
            server_stats['memory'] = mem_usage if mem_usage and not mem_err else "N/A"
            if mem_err: server_stats['memory_error'] = mem_err

            # Disk Usage (Root filesystem) - using the awk from prompt, but key name from existing code for consistency
            disk_command = "df -h / | tail -n 1 | awk '{printf \"size: %s, used: %s, avail: %s, use_percentage: %s\", $2, $3, $4, $5}'"
            stdin, stdout, stderr = client.exec_command(disk_command)
            disk_usage = stdout.read().decode().strip()
            disk_err = stderr.read().decode().strip()
            server_stats['disk_root'] = disk_usage if disk_usage and not disk_err else "N/A" # Kept key 'disk_root'
            if disk_err: server_stats['disk_error'] = disk_err

            # Network Statistics Summary
            net_command = "ss -s" 
            stdin, stdout, stderr = client.exec_command(net_command)
            net_stats = stdout.read().decode().strip()
            net_err = stderr.read().decode().strip()
            server_stats['network_summary'] = net_stats if net_stats and not net_err else "N/A"
            if net_err: server_stats['network_error'] = net_err
            
            # Top 5 Processes by CPU - using the awk from prompt
            proc_command = "ps aux --sort=-%cpu | head -n 6 | awk 'NR>1 {print $1, $2, $3, $4, $11}'"
            stdin, stdout, stderr = client.exec_command(proc_command)
            proc_list = stdout.read().decode().strip()
            proc_err = stderr.read().decode().strip()
            server_stats['processes_top5_cpu'] = proc_list if proc_list and not proc_err else "N/A"
            if proc_err: server_stats['process_error'] = proc_err

        except paramiko.AuthenticationException:
            server_stats['error'] = "SSH Authentication Failed. Check credentials or SSH server configuration."
        except paramiko.SSHException as e: # Covers various SSH connection issues like host not found, connection refused
            server_stats['error'] = f"SSH Connection Error: {str(e)}"
        # TimeoutError is a subclass of OSError, can be caught by broader Exception or specifically.
        # paramiko.SSHClient.connect already has a timeout parameter. If that expires, it raises socket.timeout, which is an OSError.
        except TimeoutError: # Explicitly catch if needed, though SSHException might cover it.
             server_stats['error'] = f"SSH Connection to {host}:{port} timed out."
        except Exception as e:
            server_stats['error'] = f"An unexpected error occurred in ServerMonitorTool: {str(e)}"
        finally:
            if client:
                client.close()
        return server_stats

if __name__ == '__main__':
    print("Starting ServerMonitorTool example script...")
    # This example part is for local testing by a developer.
    # Ensure paramiko is installed: pip install paramiko

    tool = ServerMonitorTool()

    print("\n--- Testing with Password Authentication ---")
    print("Edit the details below to match your server and credentials.")
    # Replace with your actual server details for password authentication:
    # results_password = tool._run(
    #     host="YOUR_SERVER_IP_OR_HOSTNAME",
    #     port=22,  # Default is 22, change if your SSH server uses a different port
    #     username="YOUR_SSH_USERNAME",
    #     password="YOUR_SSH_PASSWORD"
    # )
    # if results_password:
    #     print("Results (Password Auth):")
    #     for key, value in results_password.items():
    #         print(f"  {key}: {value}")
    # else:
    #     print("Password authentication test skipped or results_password was None/empty.")
    print("Password authentication example commented out by default. Uncomment the section above and fill in details to test.")

    print("\n--- Testing with Private Key Authentication ---")
    print("Edit the details below to match your server and private key path.")
    # Replace with your actual server details and private key path:
    # Make sure your private key file (e.g., id_rsa) is accessible and has correct permissions (e.g., chmod 600 /path/to/your/id_rsa on Linux/macOS).
    # The key should not be password-protected for this example, or you should use an SSH agent that manages the key's passphrase.
    # results_key = tool._run(
    #     host="YOUR_SERVER_IP_OR_HOSTNAME",
    #     port=22,  # Default is 22, change if your SSH server uses a different port
    #     username="YOUR_SSH_USERNAME",
    #     private_key_path="/path/to/your/id_rsa"  # e.g., "/home/user/.ssh/id_rsa" or "C:/Users/YourUser/.ssh/id_rsa"
    # )
    # if results_key:
    #     print("\nResults (Private Key Auth):")
    #     for key, value in results_key.items():
    #         print(f"  {key}: {value}")
    # else:
    #     print("Private key authentication test skipped or results_key was None/empty.")
    print("Private key authentication example commented out by default. Uncomment the section above and fill in details to test.")

    print("\nExample script finished. Manually uncomment and configure the authentication method you wish to test.")
