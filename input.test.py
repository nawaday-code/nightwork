from src.DataObj.settings import Settings
from src.DataObj.path import TrustPath
from src.Util.input.access import AccessDBReader

import datetime

access_path = TrustPath.from_access_file("C:\\Users\\unawa\\デスクトップ\\prog\\nightwork\\next勤務表\\shifttable.accdb")
setting_path = TrustPath.from_json_file("C:\\Users\\unawa\\デスクトップ\\prog\\nightwork\\next勤務表\\settings\\settings.json")

target_date = datetime.date(2023, 12, 1)

member = AccessDBReader.read_member(target_date.year, target_date.month, access_path)
shifts = AccessDBReader.read_shifts(member,target_date, access_path)
settings = Settings(setting_path)





# import sys
# sys.path.append('/Users/nawayuuki/ProgramSpace/nightwork/nightwork/src')
# from src.Util.input import *

# def test_input_methods():
    
#     assert hasattr(AccessDBReader, 'get_all_staff_and_skills'), "AccessDBReaderには 'get_all_staff_and_skills' メソッドがありません"
#     assert hasattr(AccessDBReader, 'get_shifts'), "AccessDBReaderには 'get_shifts' メソッドがありません"
    
#     # メソッドの戻り値をテストする
#     reader = AccessDBReader()
#     staff_and_skills = reader.get_all_staff_and_skills()
#     assert len(staff_and_skills.person_list) > 0, "'get_all_staff_and_skills' は空のリストを返しました"
#     print(staff_and_skills.person_list[0].staffname)
    
#     from datetime import date
#     shifts = reader.get_shifts(staff_and_skills, date.today())
#     assert len(shifts.getlist) > 0, "'get_shifts' は空のリストを返しました"
#     for i in range(min(120, len(shifts.getlist))):
#         print(shifts.getlist[i].person.staffname, shifts.getlist[i].workdate, shifts.getlist[i].shift)


# calender.pyのDateObjectクラスのget_month_datesメソッドのテスト
# from src.DataObj.calender import DateObject
# def print_month_dates(year, month):
#     date_obj = DateObject(year, month, [], [])
#     month_dates = date_obj.get_month_dates()
#     assert len(month_dates) > 0, "'get_month_dates' は空のリストを返しました"
#     for date in month_dates:
#         print(date)

# if __name__ == "__main__":
#     # test_input_methods()
#     print_month_dates(2022, 12)
#     print_month_dates(2023, 1)
#     print_month_dates(2023, 2)

