from config import JIRA_EA_SOLUTION_FIELD
from jira import jira


class Epic(jira):
    def __init__(self, obj):
        super().__init__(obj["key"], obj)
        self.sol_architect = obj["fields"][JIRA_EA_SOLUTION_FIELD]

    def print_title(self):
        return f"Epic [{self.key}] {self.name}"

    def process_considered_and_open(self):
        print(f"- {self.print_title()} - CONSIDERED AND OPEN")

    def process_not_considered(self):
        print(f"- {self.print_title()} - NOT CONSIDERED WITHOUT EACOUNCIL LABEL")

    def process_considered_and_closed(self):
        print(f"- {self.print_title()} - CONSIDERED BUT CLOSED")