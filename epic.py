from config import JIRA_EA_SOLUTION_FIELD, JIRA_LABELS, JIRA_TICKETS_SUMMARIES, JIRA_EA_ARCHITECT_FIELD
from helpers import change_label, create_ticket, get_ticket_by_summary, close_ticket
from jira import jira


class Epic(jira):
    def __init__(self, obj, ea_architect):
        super().__init__(obj["key"], obj)
        self.sol_architect = obj["fields"][JIRA_EA_SOLUTION_FIELD]
        self.ea_architect = ea_architect
        self.action_spacing = "\t* "

    def add_label(self, label):
        operation = [
            {
                "add": f"{label}"
            }
        ]
        change_label(self.key, operation)
        print(f"{self.spacing}{self.action_spacing}Added label: {label}")

    def _remove_label(self, label):
        operation = [
            {
                "remove": f"{label}"
            }
        ]
        change_label(self.key, operation)
        print(f"{self.spacing}{self.action_spacing}Removed label: {label}")

    def process_considered_and_open(self):
        pass
        print(f"{self.print_title()}:")
        self.add_label("pepelepu")

    def process_not_considered(self):
        pass
        print(f"{self.print_title()}:")
        self._remove_label(JIRA_LABELS["PENDING_REVIEW"])
        self.add_label(JIRA_LABELS["CLOSED_NOT_CONSIDERED"])

    def process_considered_and_closed(self):
        print(f"{self.print_title()}:")
        ticket = get_ticket_by_summary(JIRA_TICKETS_SUMMARIES["ASSIGN_SA"])
        if not ticket:
            new_ticket_id = create_ticket(self.key, JIRA_TICKETS_SUMMARIES["ASSIGN_SA"], self.ea_architect, "Done")
            close_ticket(new_ticket_id)
            print(f'{self.spacing}{self.action_spacing}Newly created ticket for {JIRA_TICKETS_SUMMARIES["ASSIGN_SA"]}: {new_ticket_id}')
        else:
            print(f'{self.spacing}{self.action_spacing}Existing ticket for {JIRA_TICKETS_SUMMARIES["ASSIGN_SA"]}: {ticket["key"]}')