import datetime
import calendar


class DateObject:
    def __init__(self, year, month, closed_days, holidays):
        assert isinstance(year, int), "yearは整数でなければなりません"
        assert isinstance(month, int), "monthは整数でなければなりません"
        assert all(isinstance(day, datetime.date) for day in closed_days), "closed_daysはdatetime.dateオブジェクトのリストでなければなりません"
        assert all(isinstance(day, datetime.date) for day in holidays), "holidaysはdatetime.dateオブジェクトのリストでなければなりません"
        self.__selectDate = datetime.date(year, month, day=1)
        self.__closed_days = closed_days
        self.__holidays = holidays

    @property
    def selectDate(self):
        return self.__selectDate

    
    
    def get_month_dates(self):
        month_dates = []
        _, last_day = calendar.monthrange(self.__selectDate.year, self.__selectDate.month)
        for i in range(1, last_day + 1):
            month_dates.append(self.__selectDate.replace(day=i))
        return month_dates

