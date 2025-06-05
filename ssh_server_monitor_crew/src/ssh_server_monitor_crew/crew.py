from typing import List, Optional, Tuple # Updated import
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
#from langchain_openai import ChatOpenAI # Or any other LLM you prefer

# Import the custom tool
# Assuming server_monitor_tool.py is in src/ssh_server_monitor_crew/tools/
from .tools.server_monitor_tool import ServerMonitorTool

@CrewBase
class ServerMonitorCrew():
    """ServerMonitorCrew a crew to monitor server stats via SSH."""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Initialize the custom tool
    server_tool = ServerMonitorTool()

    @agent
    def server_admin_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['server_admin'],
            tools=[self.server_tool], # Pass the tool to the agent
            verbose=True,
            allow_delegation=False,
            #llm=ChatOpenAI(model_name="gpt-4", temperature=0.7) # Example LLM
        )

    @agent
    def report_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator_agent'],
            verbose=True,
            allow_delegation=False,
            #llm=ChatOpenAI(model_name="gpt-4", temperature=0.7) # Or your chosen LLM
        )

    @agent
    def report_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator_agent'],
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model_name="gpt-4", temperature=0.7) # Or your chosen LLM
        )

    @task
    def monitor_task(self) -> Task:
        return Task(
            config=self.tasks_config['monitor_server_task'],
            agent=self.server_admin_agent(),
            # Inputs for the task will be passed during kickoff
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            agent=self.report_generator_agent()
            # No explicit context needed here, as 'server_data_list' will be in the inputs
            # passed during the specific kickoff for this task from main.py
        )

    @crew
    def crew(self, specific_tasks: Optional[Tuple[Task, ...]] = None) -> Crew: # Updated signature
        """Creates the ServerMonitorCrew crew.
        Can be initialized with a specific tuple of tasks to run, # Updated docstring
        otherwise defaults to all tasks defined in the crew.
        """
        tasks_to_run = specific_tasks if specific_tasks is not None else self.tasks
        return Crew(
            agents=self.agents,
            tasks=tasks_to_run,
            process=Process.sequential,
            verbose=True 
        )
