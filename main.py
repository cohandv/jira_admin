#!/usr/bin/env python3
import click
from jira import jira
from program import Program


@click.command(help='Backfills EA work onto existing epics')
@click.option('--tpm', '-t', required=False, help="TPM-1234 your program TPM you'are assigned to")
@click.option('--jira-user', '-ju', required=True, help="Your JIRA username you have access to")
@click.option('--jira-token', '-jt', required=True, help="Your JIRA username token you have created")
@click.option('--dry-run/--run', default=True, required=False,
              help="If provided will sort alphabetically ascending or descending")
def complete(tpm, jira_user, jira_token, dry_run):
    if tpm:
        tpms = [tpm]
    else:
        tpms = ['TPM-931','TPM-897','TPM-903','TPM-939','TPM-898','TPM-914','TPM-924','TPM-910','TPM-926','TPM-906','TPM-948','TPM-950']
    for iter_tpm in tpms:
        jira.set_attributes(jira_user, jira_token, not dry_run)
        p = Program(iter_tpm)
        p.review_projects()


if __name__ == "__main__":
    complete()
