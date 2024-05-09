import datetime

class ContributionTracker:
    def __init__(self):
        self.contributions = {}

    def track_contribution(self, user_id, contribution_type, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        self.contributions[user_id] = contribution_type