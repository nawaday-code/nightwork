from src.DataObj.settings import Settings
from src.DataObj.path import TrustPath
from src.Util.input.access import AccessDBReader

import datetime


class InfoBOX:
    def __init__(self, access_path, settings_path, holiday_path, target_year=None, target_month=None, start_date=None, end_date=None):
        self.__access_path_obj = TrustPath.from_access_file(access_path)
        self.__settings_path_obj = TrustPath.from_json_file(settings_path)
        self.__holiday_path_obj = TrustPath.from_csv_file(holiday_path)
        
        if target_year is None:
            target_year = datetime.date.today().year
        if target_month is None:
            target_month = datetime.date.today().month
        if start_date is None:
            start_date = self.__get_last_month_date(datetime.date.today())
        if end_date is None:
            end_date = self.__get_next_month_date(datetime.date.today())
        
        self.__member = AccessDBReader.read_member(target_year, target_month, self.__access_path_obj)
        self.__shifts = AccessDBReader.read_shifts(self.__member, start_date, end_date, self.__access_path_obj)
        self.__alpha = AccessDBReader.read_alpha(start_date, end_date, self.__access_path_obj)
        self.__beta = AccessDBReader.read_beta(start_date, end_date, self.__access_path_obj)
        self.__gamma = AccessDBReader.read_gamma(start_date, end_date, self.__access_path_obj)
        self.__settings = Settings(self.__settings_path_obj)

    #日付を変更したいとき、日付が変更された新たなInfoBOXを生成する仕様
    #なぜこのようにしたのかというと、元々のデータを変更不可にして状態を追えるようにする目的があったため
    def change_target_date(self, target_year, target_month, start_date, end_date):
        return cls(self.__access_path_obj, self.__settings_path_obj, self.__holiday_path_obj, target_year, target_month, start_date, end_date)
        

    @property
    def member(self):
        return self.__member

    @property
    def shifts(self):
        return self.__shifts

    @property
    def settings(self):
        return self.__settings

    def get_Nr(self):
        return self.__member.get_Nr()

    def get_Ndaily(self):
        return self.__member.get_Ndaily()

    def get_Nnight(self):
        return self.__member.get_Nnight()

    def get_Nboth(self):
        return self.__member.get_Nboth()

    def get_Ns(self):
        return self.__member.get_Ns()

    def get_G(self):
        return self.__member.get_G()

    def get_Core(self):
        return self.__member.get_Core()

    def get_Core_G(self):
        return self.__member.get_Core_G()

    def get_by_modality(self, assigned_modality):
        return self.__member.get_by_modality(assigned_modality)

    def getlist(self):
        return self.__shifts.getlist

    def get_W(self):
        return self.__settings.get_W()

    def get_day_works(self):
        return self.__settings.get_day_works()

    def get_night_works(self):
        return self.__settings.get_night_works()

    def get_day_and_night_works(self):
        return self.__settings.get_day_and_night_works()

    def get_ake(self):
        return self.__settings.get_ake()

    def get_target_modalities(self):
        return self.__settings.get_target_modalities()

    def get_other(self):
        return self.__settings.get_other()

    def get_dayoff(self):
        return self.__settings.get_dayoff()

    def get_holiday(self):
        return self.__settings.get_holiday()

    def get_modality_acronyms(self):
        return self.__settings.get_modality_acronyms()

    def get_alpha(self):
        return self.__alpha.get_daily_needs()

    def get_beta(self):
        return self.__beta.get_daily_needs()

    def get_gamma(self):
        return self.__gamma.get_daily_needs()
    


    def __get_last_month_date(self, date):
        if date.month == 1:
            last_month_date = datetime.date(date.year - 1, 12, 31)
        else:
            last_month_date = datetime.date(date.year, date.month - 1, 1) - datetime.timedelta(days=1)
        return last_month_date

    def __get_next_month_date(self, date):
        if date.month == 12:
            next_month_date = datetime.date(date.year + 1, 1, 1)
        else:
            next_month_date = datetime.date(date.year, date.month + 1, 1)
        return next_month_date

