from crewai import Crew, Process
from crewai.config import load_agents, load_tasks

class ContentCrew(Crew):
    """ContentCrew: wires agents and tasks defined in YAML."""

    # Automatically load agents and tasks from the config folder
    agents = load_agents(__file__)
    tasks = load_tasks(__file__)

    # Execute tasks in sequence
    process = Process.sequential
