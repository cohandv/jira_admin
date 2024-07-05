import requests
from requests.auth import HTTPBasicAuth

from config import JIRA_LABELS, JIRA_URL, JIRA_EA_ARCHITECT_FIELD, \
    JIRA_CLOSE_TRANSITION, JIRA_PROJECT

class jira:
    user = None
    api_token = None
    run = False

    def __init__(self, key, obj=None):
        self.key = key
        self.type = self.__class__.__name__.lower()
        self.spacing = ""
        self.spacing += "\t\t" if self.type == "project" else ""
        self.spacing += "\t\t\t\t" if self.type == "epic" else ""
        if obj is not None:
            fields = obj["fields"]
            self.name = fields["summary"]
            self.status = fields["status"]["name"].lower()
            self.labels = list(map(lambda x: x.lower(), fields["labels"]))
            self.ea_label = JIRA_LABELS["CONSIDERED"].lower() in self.labels
            self.review_pending = JIRA_LABELS["PENDING_REVIEW"].lower() in self.labels
        else:
            self.name = None
            self.status = None
            self.labels = []
        self.obj = obj

    @classmethod
    def set_attributes(cls, user, api_token, run):
        cls.run = run
        cls.user = user
        cls.api_token = api_token

    def print_title(self):
        return f"{self.spacing} - {self.type} [{self.key}] {self.name}"

    def get_parent_query(self):
        return f"parent={self.key}"

    def get_auth(self):
        return HTTPBasicAuth(jira.user, jira.api_token)

    def close_ticket(self, issue_id):
        if jira.run:
            transition_data = {
                "transition": {
                    "id": JIRA_CLOSE_TRANSITION
                }
            }

            # Make the request to perform the transition
            response = requests.post(f"{JIRA_URL}/3/issue/{issue_id}/transitions",
                                     auth=self.get_auth(),
                                     json=transition_data)
            response.raise_for_status()
        else:
            print(f"{self.spacing}\t Ignoring close ticket")

    def get_tickets(self, jql):
        """
        Get all project tickets for the given query
        :param jql:  jira query
        :return:
        """
        start_at = 0
        max_results = 50
        total = 100
        total_issues = []
        while total != 0:
            r = requests.get(
                f"{JIRA_URL}/2/search?jql={jql}&startAt={start_at}&maxResults={max_results}",
                auth=self.get_auth())
            r.raise_for_status()
            data = r.json()
            total = data['total'] if data['total'] == data['maxResults'] else 0
            start_at += data['total']
            total_issues += data['issues']

        return total_issues

    def get_ticket_by_summary(self, summary, parent):
        """
        Get all tickets for the given summary
        :param summary:   value
        :return:
        """
        return next(iter(self.get_tickets(f'summary~"{summary}" AND parent={parent}')), None)

    def change_label(self, issue_id, operation):
        if jira.run:
            json_data = {
                "update": {
                    "labels": operation
                }
            }
            response = requests.put(f"{JIRA_URL}/3/issue/{issue_id}",
                                    json=json_data,
                                    auth=self.get_auth())
            response.raise_for_status()
        else:
            print(f"{self.spacing}\t Ignoring change label ticket")

    def change_ea_architect(self, issue_id, value):
        if jira.run:
            json_data = {
                "fields": {
                    JIRA_EA_ARCHITECT_FIELD: value
                }
            }
            response = requests.put(f"{JIRA_URL}/3/issue/{issue_id}",
                                    json=json_data,
                                    auth=self.get_auth())
            response.raise_for_status()
        else:
            print(f"{self.spacing}\t Ignoring change ea architect to project ticket")

    def create_ticket(self, epic, title, asignee, description) -> str:
        if jira.run:
            ticket = {
                "fields": {
                    "description": description,
                    "project":
                        {
                            "key": JIRA_PROJECT
                        },
                    "assignee": asignee,
                    "customfield_10008": epic,
                    "summary": title,
                    "issuetype": {
                        "name": "Task"
                    },
                    "labels": [
                        JIRA_LABELS["CONSIDERED"]
                    ]
                }
            }
            r = requests.post(f"{JIRA_URL}/2/issue", json=ticket, auth=self.get_auth())
            r.raise_for_status()
            ticket_number = r.json()["key"]
            return ticket_number
        else:
            print(f"{self.spacing}\t Ignoring creating ticket")
            return "AR-000"
