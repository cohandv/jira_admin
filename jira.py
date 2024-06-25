from config import JIRA_LABELS


class jira:
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
        else:
            self.name = None
            self.status = None
            self.labels = []
        self.obj = obj

    def print_title(self):
        return f"{self.spacing} - {self.type} [{self.key}] {self.name}"

    def get_parent_query(self):
        return f"parent={self.key}"
