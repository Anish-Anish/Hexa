class Reservation:
    def __init__(self, reservation_id=None, customer_id=None, vehicle_id=None, start_date=None, end_date=None, total_cost=None, status=None):
        self.__reservation_id = reservation_id
        self.__customer_id = customer_id
        self.__vehicle_id = vehicle_id
        self.__start_date = start_date
        self.__end_date = end_date
        self.__total_cost = total_cost
        self.__status = status

    @property
    def reservation_id(self):
        return self.__reservation_id

    @reservation_id.setter
    def reservation_id(self, value):
        self.__reservation_id = value

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    @property
    def total_cost(self):
        return self.__total_cost

    @total_cost.setter
    def total_cost(self, value):
        self.__total_cost = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def calculate_total_cost(self):
        pass
