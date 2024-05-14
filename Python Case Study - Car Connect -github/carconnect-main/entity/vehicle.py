class Vehicle:
    def __init__(self, vehicle_id=None, model=None, make=None, year=None, color=None, registration_number=None, availability=None, daily_rate=None):
        self.__vehicle_id = vehicle_id
        self.__model = model
        self.__make = make
        self.__year = year
        self.__color = color
        self.__registration_number = registration_number
        self.__availability = availability
        self.__daily_rate = daily_rate

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def make(self):
        return self.__make

    @make.setter
    def make(self, value):
        self.__make = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def registration_number(self):
        return self.__registration_number

    @registration_number.setter
    def registration_number(self, value):
        self.__registration_number = value

    @property
    def availability(self):
        return self.__availability

    @availability.setter
    def availability(self, value):
        self.__availability = value

    @property
    def daily_rate(self):
        return self.__daily_rate

    @daily_rate.setter
    def daily_rate(self, value):
        self.__daily_rate = value
