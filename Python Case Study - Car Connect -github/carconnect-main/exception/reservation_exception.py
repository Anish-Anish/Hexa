class ReservationException(Exception):
    def __init__(self, message="Reservation error"):
        self.message = message
        super().__init__(self.message)