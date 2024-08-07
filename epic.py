from config import JIRA_EA_SOLUTION_FIELD, JIRA_LABELS, JIRA_TICKETS_SUMMARIES, JIRA_EA_ARCHITECT_FIELD, \
    JIRA_TICKETS_ASSIGNEE
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

    def _create_ticket(self, summary_type, summary, description=None, close_ticket_action=False):
        ticket = self.get_ticket_by_summary(summary, self.key)
        if not ticket:
            assignee = self.sol_architect if JIRA_TICKETS_ASSIGNEE[
                                                 summary_type] == "SA" and self.sol_architect else self.ea_architect
            new_ticket_id = self.create_ticket(self.key, summary, assignee, description)
            if close_ticket_action:
                self.close_ticket(new_ticket_id)
            print(f'{self.spacing}{self.action_spacing}Newly created ticket for {summary}: {new_ticket_id}')
        else:
            print(f'{self.spacing}{self.action_spacing}Existing ticket for {summary}: {ticket["key"]}')

    def process_considered_and_open(self):
        print(f"{self.print_title()}:")
        for summary in JIRA_TICKETS_SUMMARIES.keys():
            self._create_ticket(summary, JIRA_TICKETS_SUMMARIES[summary],
                                "This task is automatically created to review the "
                                "parent Epic to evaluate "
                                "if its in EA scope or not. \n"
                                "When in scope we just have to add the EACouncil label on the epic \n"
                                "When it is not in scope we should fill and attach the following "
                                "[template|https://docs.google.com/spreadsheets/d/1tNEywpwpJwiigvJ_45CBAk63oY331O8yTRlYo7PoXpM/edit?usp=sharing]\n"
                                "Acceptance criteria\n\n"
                                "- The above categorization done")

    def fix_ea_architect(self):
        try:
            self.change_ea_architect(self.key, self.ea_architect)
            print(f"{self.spacing}     Added EA {self.ea_architect['emailAddress']} to epic: {self.key}")
        except Exception as e:
            print(e)

    def process_not_reviewed(self):
        self._create_ticket("PENDING_REVIEW", JIRA_TICKETS_SUMMARIES["PENDING_REVIEW"])

    def process_update_artifacts(self):
        self._create_ticket("EA_ARTIFACTS", JIRA_TICKETS_SUMMARIES["EA_ARTIFACTS"],
                            description=f"This task is automatically created to update EA artifacts related to the Epic "
                                        f"Read more about EA artifacts and how to update them ["
                                        f"here|https://ipsycorp.atlassian.net/wiki/spaces/EA/pages/3700555928/EA"
                                        f"+Repository+Runbook]"
                                        f"Acceptance criteria "
                                        f"- EA defines a list of affected artifacts (they must exist)"
                                        f"- SA updates the artifacts")

    def process_not_considered(self):
        print(f"{self.print_title()}:")
        self._remove_label(JIRA_LABELS["PENDING_REVIEW"])
        self._add_label(JIRA_LABELS["CLOSED_NOT_CONSIDERED"])

    def process_considered_and_closed(self):
        print(f"{self.print_title()}:")
        for summary in JIRA_TICKETS_SUMMARIES.keys():
            self._create_ticket(summary, JIRA_TICKETS_SUMMARIES[summary], True)
