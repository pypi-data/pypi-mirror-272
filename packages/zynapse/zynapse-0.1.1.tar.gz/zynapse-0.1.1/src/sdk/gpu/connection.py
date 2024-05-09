# import ray
from fabric import Connection

class Cluster:
    def __init__(self, cluster_address, username, password):
        self.cluster_address = cluster_address
        self.username = username
        self.password = password
        self.conn = Connection(self.cluster_address, user=self.username, connect_kwargs={'password': self.password})

    def connect(self):
        self.conn.connect()

    def distribute_task(self, task):
        # TODO Use ray to distribute the task across the cluster
        pass

    def disconnect(self):
        self.conn.close()