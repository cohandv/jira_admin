import requests
from requests.auth import HTTPBasicAuth

from config import JIRA_USER, JIRA_URL, JIRA_API_TOKEN


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