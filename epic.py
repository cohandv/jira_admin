from config import JIRA_EA_SOLUTION_FIELD, JIRA_LABELS, JIRA_TICKETS_SUMMARIES, JIRA_EA_ARCHITECT_FIELD
from jira import jira


class Epic(jira):
    def __init__(self, obj, project_key, ea_architect):
        super().__init__(obj["key"], obj)
        self.sol_architect = obj["fields"][JIRA_EA_SOLUTION_FIELD]
        self.ea_architect = ea_architect
        self.project_key = project_key
        self.action_spacing = "\t* "

    def _add_label(self, label):
        operation = [
            {
                "add": f"{label}"
            }
        ]
        self.change_label(self.key, operation)
        print(f"{self.spacing}{self.action_spacing}Added label: {label}")

    def _remove_label(self, label):
        operation = [
            {
                "remove": f"{label}"
            }
        ]
        self.change_label(self.key, operation)
        print(f"{self.spacing}{self.action_spacing}Removed label: {label}")

    def _create_ticket(self, summary, close_ticket_action=False):
        ticket = self.get_ticket_by_summary(summary, self.key)
        if not ticket:
            new_ticket_id = self.create_ticket(self.key, summary, self.ea_architect)
            if close_ticket_action:
                self.close_ticket(new_ticket_id)
            print(f'{self.spacing}{self.action_spacing}Newly created ticket for {summary}: {new_ticket_id}')
        else:
            print(f'{self.spacing}{self.action_spacing}Existing ticket for {summary}: {ticket["key"]}')

    def process_considered_and_open(self):
        print(f"{self.print_title()}:")
        for summary in JIRA_TICKETS_SUMMARIES.keys():
            self._create_ticket(JIRA_TICKETS_SUMMARIES[summary])

    def process_not_considered(self):
        print(f"{self.print_title()}:")
        self._remove_label(JIRA_LABELS["PENDING_REVIEW"])
        self._add_label(JIRA_LABELS["CLOSED_NOT_CONSIDERED"])

    def process_considered_and_closed(self):
        print(f"{self.print_title()}:")
        for summary in JIRA_TICKETS_SUMMARIES.keys():
            self._create_ticket(JIRA_TICKETS_SUMMARIES[summary], True)