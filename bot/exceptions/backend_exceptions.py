class BackendDead(Exception):
    def __init__(self, message="Backend is offline or have an error"):
        self.message = message
        super().__init__(self.message)
