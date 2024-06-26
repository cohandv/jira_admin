# Jira Admin

## Purpose
The purpose of this automation is to backfill our tickets with a defined strategy

## Prerequisites
* python
* pip
* Generate an [jira api token](https://id.atlassian.com/manage-profile/security/api-tokens)

## Execution

```shell
./main.py -ju YOUR_USER@ipsy.com -jt YOUR_JIRA_API_TOKEN -t YOUR_TPM 
Connected to pydev debugger (build 233.13135.95)
```
* Note that by default will dry run making an analysis on your program unless you pass `--run` then will perform changes

## Logic of the backfill
```mermaid
flowchart TD
    A[Enterprise Architect User]-->|Get Program Details|B[Program]
    B --> |Get Projects|C[Project]
    C --> CC(Assign Enterprise architect inherited from program to project)
    CC --> |Get Epics|D[Epic]
    D --> |Foreach Epic in each project|F{Has EACouncil label}
    F --> |No|G(Update epic with label EACouncilReviewed)
    G --> H(End)
    F --> |Yes|I(Create EA follow up tickets)
    I --> |Add EACountil label|J(Added EACouncil label to EA tickets)
    J --> K{Is Epic open}
    K --> |Yes|H
    K --> |No|M(Close EA follow up tickets with Won't Do status)
    M --> H
```

* Note that this is idempotent, it will always produce the same result, it wont duplicate tickets