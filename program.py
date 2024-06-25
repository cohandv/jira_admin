from config import JIRA_EA_ARCHITECT_FIELD
from helpers import get_tickets
from jira import jira
from project import Project


class Program(jira):
    def __init__(self, key):
        programs = get_tickets(f"id={key}")
        program_obj = programs[0] if len(programs) > 0 else None
        super().__init__(key, program_obj)
        self.ea_architect = program_obj["fields"][JIRA_EA_ARCHITECT_FIELD]
        self.projects = []
        self._load_projects()

    def _load_projects(self):
        """
        Get all project tickets for the given program
        :return:
        """
        proj_tickets = get_tickets(self.get_parent_query())
        self.projects = list(map(lambda x: Project(x), proj_tickets))

    def review_projects(self):
        print(f"Updating program {self.key}, there are {len(self.projects)} projects")
        for project in self.projects:
            project.update_epics()
