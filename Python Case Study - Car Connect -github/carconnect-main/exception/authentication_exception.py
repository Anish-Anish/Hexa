class AuthenticationException(Exception):
    def __init__(self, message="Authentication error"):
        self.message = message
        super().__init__(self.message)