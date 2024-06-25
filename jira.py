from config import JIRA_LABELS


class jira:
    def __init__(self, key, obj=None):
        self.key = key
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

    def get_parent_query(self):
        return f"parent={self.key}"