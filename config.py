import os

# Inputs
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Settings
JIRA_URL = os.getenv("JIRA_URL", "https://ipsycorp.atlassian.net/rest/api")
JIRA_FINISHED_STATES = ["done", "cancelled", "rejected", "won't do", "abandoned"]
JIRA_EA_ARCHITECT_FIELD = "customfield_10450"
JIRA_EA_SOLUTION_FIELD = "customfield_10451"

JIRA_LABELS = {
    "CLOSED_NOT_CONSIDERED": "EACouncilReviewed",
    "CONSIDERED": "EACouncil"
}

JIRA_PROJECT = "AR"

JIRA_TICKETS_SUMMARIES = {
    "ASSIGN_SA": "Assign solution architect",
    "SOLUTION_DESIGN": "Develop solution design",
    "EA_RETRO": "Run EA retro and share learnings"
}