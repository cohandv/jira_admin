from config import JIRA_FINISHED_STATES, JIRA_LABELS
from epic import Epic
from jira import jira


class Project(jira):
    def __init__(self, obj, ea_architect):
        super().__init__(obj["key"], obj)
        self.epics = []
        self.ea_architect = ea_architect
        # TODO: Assign EA to project as part of JP ask
        self._load_epics()

    def _load_epics(self):
        """
        Get all project tickets for the given program
        :return:
        """
        epic_tickets = self.get_tickets(self.get_parent_query())
        self.epics = list(map(lambda x: Epic(x, self.key, self.ea_architect), epic_tickets))

    def fix_ea_architect(self):
        self.change_ea_architect(self.key, self.ea_architect)
        print(f"{self.spacing}     Added EA {self.ea_architect['emailAddress']} to project: {self.key}")
        for epic in self.epics:
            epic.fix_ea_architect()

    def update_epics(self):
        print(f"{self.print_title()} - Evaluating {len(self.epics)} epics")
        if len(self.epics) > 0:
            # print(f"{self.spacing}   * CONSIDERED TO REVIEW")
            # # Projects with review pending label but without review ticket
            # for epic in [epic for epic in self.epics if epic.review_pending and epic.status not in JIRA_FINISHED_STATES]:
            #     epic.process_not_reviewed()
            #
            # print(f"{self.spacing}   * NOT CONSIDERED WITHOUT EACOUNCIL LABEL")
            # # Projects not considered at origin
            # for epic in [epic for epic in self.epics if not epic.ea_label]:
            #     epic.process_not_considered()
            #
            # # # Projects closed considered
            # print(f"{self.spacing}   * CONSIDERED BUT CLOSED")
            # for epic in [epic for epic in self.epics if epic.ea_label and epic.status in JIRA_FINISHED_STATES]:
            #     epic.process_considered_and_closed()
            #
            # # # Projects open considered
            # print(f"{self.spacing}   * CONSIDERED AND OPEN")
            # for epic in [epic for epic in self.epics if epic.ea_label and epic.status not in JIRA_FINISHED_STATES]:
            #     epic.process_considered_and_open()
            # # Projects open considered
            print(f"{self.spacing}   * CONSIDERED AND OPEN - Backfill for update EA Repo")
            for epic in [epic for epic in self.epics if epic.ea_label and epic.status not in JIRA_FINISHED_STATES ]:
                if (epic.sol_architect is not None
                        and JIRA_LABELS["CLOSED_NOT_CONSIDERED"].lower() not in epic.labels
                        and JIRA_LABELS["CONSIDERED"].lower() in epic.labels):
                    epic.process_update_artifacts()


