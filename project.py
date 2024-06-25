from config import JIRA_FINISHED_STATES
from epic import Epic
from helpers import get_tickets
from jira import jira


class Project(jira):
    def __init__(self, obj):
        super().__init__(obj["key"], obj)
        self.epics = []
        self._load_epics()

    def _load_epics(self):
        """
        Get all project tickets for the given program
        :return:
        """
        epic_tickets = get_tickets(self.get_parent_query())
        self.epics = list(map(lambda x: Epic(x), epic_tickets))

    def search_for_epic(self):
        pass

    def update_epics(self):
        print(f"{self.print_title()} - Evaluating their epics {len(self.epics)}")
        print(f"{self.spacing}   * NOT CONSIDERED WITHOUT EACOUNCIL LABEL")
        # # Projects not considered at origin
        for epic in [epic for epic in self.epics if not epic.ea_label]:
            epic.process_not_considered()
        pass

        # Projects closed considered
        print(f"{self.spacing}   * CONSIDERED BUT CLOSED")
        for epic in [epic for epic in self.epics if epic.ea_label and epic.status in JIRA_FINISHED_STATES]:
            epic.process_considered_and_closed()
        pass

        # # Projects open considered
        print(f"{self.spacing}   * CONSIDERED AND OPEN")
        for epic in [epic for epic in self.epics if epic.ea_label and epic.status not in JIRA_FINISHED_STATES]:
            epic.process_considered_and_open()
        pass

