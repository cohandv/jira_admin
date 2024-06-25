from config import JIRA_EA_SOLUTION_FIELD
from helpers import change_label
from jira import jira


class Epic(jira):
    def __init__(self, obj):
        super().__init__(obj["key"], obj)
        self.sol_architect = obj["fields"][JIRA_EA_SOLUTION_FIELD]

    def add_label(self, label):
        operation = [
            {
                "add": f"{label}"
            }
        ]
        change_label(self.key, operation)
        print(f"{self.spacing}\t* Added label: {label}")

    def process_considered_and_open(self):
        print(f"{self.print_title()}:")
        self.add_label("pepelepu")

    def process_not_considered(self):
        print(f"{self.print_title()}:")
        self.add_label("pepelepu")

    def process_considered_and_closed(self):
        print(f"{self.print_title()}:")
        self.add_label("pepelepu")