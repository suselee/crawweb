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
            allow_delegation=False
            #llm=ChatOpenAI(model_name="gpt-4", temperature=0.7) # Example LLM
        )
    @agent
    def report_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator_agent'],
            verbose=True,
            allow_delegation=False
        )

    @task
    def monitor_task(self) -> Task:
        return Task(
            config=self.tasks_config['monitor_server_task'],
            agent=self.server_admin_agent()
            # Inputs for the task will be passed during kickoff
        )
    
    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            agent=self.report_generator_agent(),
            context=[self.monitor_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ServerMonitorCrew crew"""
        return Crew(
            agents=self.agents, # Automatically populated by @agent decorator
            tasks=self.tasks, # Automatically populated by @task decorator
            process=Process.sequential,
            verbose=True
        )
