import datetime

class UsageTracker:
    def __init__(self):
        self.usage_data = {}

    def track_usage(self, user_id, usage_type, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        self.usage_data[user_id] = usage_type