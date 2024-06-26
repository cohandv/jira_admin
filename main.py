#!/usr/bin/env python3
import click
from jira import jira
from program import Program


@click.command(help='Backfills EA work onto existing epics')
@click.option('--tpm', '-t', required=True, help="TPM-1234 your program TPM you'are assigned to")
@click.option('--jira-user', '-ju', required=True, help="Your JIRA username you have access to")
@click.option('--jira-token', '-jt', required=True, help="Your JIRA username token you have created")
@click.option('--dry-run/--run', default=True, required=False,
              help="If provided will sort alphabetically ascending or descending")
def complete(tpm, jira_user, jira_token, dry_run):
    jira.set_attributes(jira_user, jira_token, not dry_run)
    p = Program(tpm)
    p.review_projects()


if __name__ == "__main__":
    complete()
