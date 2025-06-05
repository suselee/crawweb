# SSH Server Monitor Crew (Batch Processing)

This project uses crewAI to monitor server statistics (CPU, memory, disk, network, processes) for multiple Linux servers listed in an Excel file. It processes servers concurrently and generates a single consolidated health report in Markdown.

## Features
- Reads server connection details (hostname, IP, username, password) from `servers.xlsx` located in the project root.
- Processes multiple servers concurrently using asynchronous operations to improve speed.
- Connects to each remote server via SSH using the custom `ServerMonitorTool`.
- Collects CPU, memory, disk, network, and process information for each server.
- Generates a **single, consolidated server health report in Markdown format (`server_status_report.md`)**. This report includes:
    - A dedicated section for each server, identified by its hostname.
    - Detailed metrics for reachable servers.
    - Clear error messages for unreachable servers or those where data collection failed (e.g., "hostname: Unreachable!" or "hostname: Error - [error message]").

## Setup and Configuration

1.  **Create `servers.xlsx`:**
    In the root directory of this project (`ssh_server_monitor_crew/`), create an Excel file named `servers.xlsx`.
    It must contain the following columns (ensure these exact header names):
    - `hostname`: A unique name or identifier for the server (e.g., web-server-01).
    - `ip_address`: The IP address of the server.
    - `username`: The SSH username.
    - `password`: The SSH password. Leave this cell blank if using SSH key-based authentication (not yet implemented in this version, password is required).

2.  **Install Dependencies:**
    Navigate to the `ssh_server_monitor_crew/` directory in your terminal.
    Dependencies are listed in `pyproject.toml`.
    *   **Using Poetry (recommended):**
        ```bash
        poetry install
        ```
    *   **Using pip:**
        ```bash
        pip install crewai crewai-tools paramiko pandas openpyxl langchain-openai # Or your preferred LLM library
        ```

3.  **Configure LLM API Keys (if needed):**
    The example in `src/ssh_server_monitor_crew/crew.py` uses `ChatOpenAI`. If using an LLM that requires an API key (like OpenAI), set it as an environment variable.
    Open/create the `.env` file in the `ssh_server_monitor_crew/` directory and add your key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    If you change the LLM in `crew.py`, adjust environment variables accordingly.

## How to Run

1.  Ensure `servers.xlsx` is created and populated in the `ssh_server_monitor_crew/` directory.
2.  Ensure dependencies and API keys are set up as described above.
3.  Navigate to the `ssh_server_monitor_crew/` directory in your terminal.
4.  Run the main script:
    ```bash
    python src/ssh_server_monitor_crew/main.py
    ```
    (Or if using Poetry: `poetry run python src/ssh_server_monitor_crew/main.py`)

5.  The script will process each server listed in `servers.xlsx` concurrently.
6.  After processing all servers, a consolidated report named `server_status_report.md` will be generated in the `ssh_server_monitor_crew/` project root directory. This file will contain the health status for all processed servers.
