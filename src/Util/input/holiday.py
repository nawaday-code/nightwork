import csv
import datetime

from src.DataObj.path import *    
from src.DataObj.calender import DateArray


class JapanHoliday():
    """
    内閣府が公表している「平成29年（2017年）から平成31年（2019年）国民の祝日等
    （いわゆる振替休日等を含む）」のCSVを使用して
    入力された日付('2017-01-01' %Y-%m-%d形式)が土、日、休日か判定するクラス
    """
    @staticmethod
    def _read_holiday(path_obj, encoding='cp932'):

        """
        CSVファイルを読み込み、self.holidaysに以下の形式のdictをListに格納する
        {'2017-01-09': {'day': '2017-01-09', 'name': '成人の日'}}
        CSVファイルがないとIOErrorが発生する
 
        :param path: 祝日と祝日名が記入されたCSVファイル。ヘッダーが必要
        :param encoding: CSVファイルのエンコーディング
        :return: DateArrayオブジェクト
        """
        holidays = {}
        tokai_holidays = [['01-02','東海大休日'],['01-03','東海大休日'],['11-01','建学の日'],
                          ['12-29','東海大休日'],['12-30','東海大休日'],['12-31','東海大休日']]
        with open(path_obj.value, encoding=encoding, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # CSVのヘッダーを飛ばす
            for row in reader:
                day_str, name = row[0], row[1]
                day = datetime.datetime.strptime(day_str, '%Y/%m/%d')
                day_str = datetime.datetime.strftime(day, '%Y-%m-%d')
                holidays[day_str] = {'day': day_str, 'name': name}

        for y in range(datetime.datetime.today().year -3, datetime.datetime.today().year +3):
            for arr in tokai_holidays:
                day = datetime.datetime.strptime(str(y) + '-'+str(arr[0]), '%Y-%m-%d')
                day_str = datetime.datetime.strftime(day, '%Y-%m-%d')                     
                holidays[day_str] = {'day': day_str, 'name':arr[1]}
        return DateArray(list(holidays.values()))
        
    def is_holiday(self, day_str):
        """
        土、日、祝日か判定する
        :param day_str: '2018-03-01'の%Y-%m-%dのstrを受け取る。
                        形式が違うとValueErrorが発生
        :return: 土、日、祝日ならTrue, 平日ならFalse
        """
        try:
            day = datetime.datetime.strptime(day_str, '%Y-%m-%d')
            week_num = self.get_weekNum(day)
            if day.weekday() >= 6 or (day.weekday() == 5 and (week_num == 2 or week_num == 4)):
                return True
        except ValueError:
            print('日付は2018-03-01 %Y-%m-%dの形式で入力してください')
            raise ValueError
        day = datetime.datetime.strptime(day_str, '%Y-%m-%d')
        day_str = datetime.datetime.strftime(day, '%Y-%m-%d')                     
        if day_str in self._holidays:
            return True
        return False
 
    # def get_holiday_dict(self):
    #     """
    #     祝日を一覧化したdictを返す
    #     {'2017-01-09': {'day': '2017-01-09', 'name': '成人の日'},
    #      '2017-02-11': {'day': '2017-02-11', 'name': '建国記念の日'},...}
    #     """
    #     return self._holidays
    
    def get_weekNum(self, _date:datetime.datetime):
        divmod_=divmod(_date.day,7) #日付を7で割って商と余りを取得

        if divmod_[0] == 0:
            week_num = 1
        elif divmod_[1] == 0:
            week_num = divmod_[0]
        else:
            week_num = divmod_[0] + 1
        
        return week_num
