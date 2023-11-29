import datetime
import calendar

class DateArray:
    def __init__(self, dateArray):
        assert all(isinstance(day, datetime.date) for day in dateArray), "コンストラクタ引数はdatetime.dateのリストでなければなりません"
        self.__dateArray = dateArray
    
    @classmethod
    def from_month(cls, year, month):
        _, last_day = calendar.monthrange(year, month)
        return cls([datetime.date(year, month, day=day) for day in range(1, last_day + 1)])

    @property
    def value(self):
        return self.__dateArray

class DateObject:
    def __init__(self, select_days, closed_days, holidays):
        assert isinstance(select_days, DateArray), "select_daysはDateArrayオブジェクトでなければなりません"
        assert isinstance(closed_days, DateArray), "closed_daysはDateArrayオブジェクトでなければなりません"
        assert isinstance(holidays, DateArray), "holidaysはDateArrayオブジェクトでなければなりません"
        self.__select_days = select_days
        self.__closed_days = closed_days
        self.__holidays = holidays

    @property
    def select_days(self):
        return self.__select_days
    
    @property
    def closed_days(self):
        return self.__closed_days

    @property
    def holidays(self):
        return self.__holidays

