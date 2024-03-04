class NoAvailablePorts(Exception):
    def __init__(self, message="There is no available ports for webhook now"):
        self.message = message
        super().__init__(self.message)