#Access dbからデータを読み込むユーティリティクラス
import pyodbc
from datetime import timedelta
from src.DataObj.person import *
from src.DataObj.member import *
from src.Entity.shift import Shift, Shifts


DB_PATH = 'C:\\Users\\unawa\\デスクトップ\\yakinManager\\nightwork\\test勤務表\\shifttable.accdb'
DB_PASSWORD = '0000'


class AccessDBReader:
    @staticmethod
    #staff全員の情報を取得する
    def get_all_staff_and_skills():
        conn = pyodbc.connect(f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH};PWD={DB_PASSWORD};')
        cursor = conn.cursor()
        cursor.execute('SELECT uid, id, staffname, status, authority FROM tblStaff')
        rows = cursor.fetchall()
        imutable_info_list = []
        for row in rows:
            imutable_info = ImutableInfo(row[0], row[1], row[2], row[3], row[4])
            imutable_info_list.append(imutable_info)
        imutable_info_list_obj = ImutableInfoList(imutable_info_list)
        
        persons = []
        for imutable_info in imutable_info_list_obj.imutable_info_list:
            cursor.execute(f'SELECT modalities, status, skill_score FROM tblSkill WHERE uid = {imutable_info.uid}')
            rows = cursor.fetchall()
            staff_skills = []
            for row in rows:
                skill = Skill(row[0], row[1], row[2])
                staff_skills.append(skill)
            skills = Skills(staff_skills)
            person = Person(imutable_info, skills)
            persons.append(person)
        member = Member(persons)
        return member

    @staticmethod
    #staffの勤務情報を取得する
    def get_shifts(member, date):
        
        conn = pyodbc.connect(f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH};PWD={DB_PASSWORD};')
        cursor = conn.cursor()
        
        start_date = date.replace(day=1)
        if date.month == 12:
            end_date = date.replace(year=date.year+1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = date.replace(month=date.month+1, day=1) - timedelta(days=1)
        
        shifts = []
        for person in member.person_list:
            cursor.execute(f'SELECT workdate, shift FROM tblShift WHERE uid = {person.uid} AND workdate BETWEEN {start_date} AND {end_date}')
            rows = cursor.fetchall()
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            for shift_date in date_range:
                shift_row = next((row for row in rows if row[0] == shift_date), None)
                if shift_row:
                    shift = Shift(person, shift_row[0], shift_row[1])
                else:
                    shift = Shift(person, shift_date, None)
                shifts.append(shift)
        # この関数を実行すると、指定された日付の前後1ヶ月間のシフト情報を含むShiftsオブジェクトが返されます。
        # Shiftsオブジェクトは、指定された期間内のすべての日付に対してShiftオブジェクトのリストを持っています。
        # 各Shiftオブジェクトは、特定の日付の特定のPersonのシフト情報を表します。
        # もしPersonがその日にシフトを持っていない場合、Shiftオブジェクトのshift属性はNoneになります。
        return Shifts(shifts)
