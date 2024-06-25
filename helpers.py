import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_USER, JIRA_URL, JIRA_API_TOKEN, JIRA_PROJECT, JIRA_CLOSE_TRANSITION


def get_tickets(jql):
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
            auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))
        r.raise_for_status()
        data = r.json()
        total = data['total'] if data['total'] == data['maxResults'] else 0
        start_at += data['total']
        total_issues += data['issues']

    return total_issues


def get_ticket_by_summary(summary):
    """
    Get all tickets for the given summary
    :param summary:   value
    :return:
    """
    return next(iter(get_tickets(f'summary~"{summary}"')), None)


def change_label(issue_id, operation):
    json_data = {
        "update": {
            "labels": operation
        }
    }
    response = requests.put(f"{JIRA_URL}/3/issue/{issue_id}",
                            json=json_data,
                            auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))
    response.raise_for_status()


def close_ticket(issue_id):
    transition_data = {
        "transition": {
            "id": JIRA_CLOSE_TRANSITION
        }
    }

    # Make the request to perform the transition
    response = requests.post(f"{JIRA_URL}/3/issue/{issue_id}/transitions",
                                        auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN),
                                        json=transition_data)
    response.raise_for_status()

def create_ticket(epic, title, asignee, status) -> str:
    ticket = {
        "fields": {
            "project":
                {
                    "key": JIRA_PROJECT
                },
            "assignee": asignee,
            "customfield_10008": epic,
            "summary": title,
            "issuetype": {
                "name": "Task"
            }
        }
    }
    r = requests.post(f"{JIRA_URL}/2/issue", json=ticket, auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))
    r.raise_for_status()
    ticket_number = r.json()["key"]
    return ticket_number
