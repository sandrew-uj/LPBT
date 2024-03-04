class DBSRecordNotFound(Exception):
    def __init__(self, message="Record not found in the database."):
        self.message = message
        super().__init__(self.message)
