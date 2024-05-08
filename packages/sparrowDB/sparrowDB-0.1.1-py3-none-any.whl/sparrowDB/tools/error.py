class SparrowValidTimeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = "Invalid valid time"
        else:
            self.error_message = error_message
        super().__init__(self.error_message)
