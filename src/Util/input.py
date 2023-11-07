#Access dbからデータを読み込むユーティリティクラス
import pyodbc
import datetime
from src.DataObj.person import *
from src.DataObj.member import *
from src.Entity.shift import Shift, Shifts


DB_PATH = 'C:\\Users\\unawa\\デスクトップ\\yakinManager\\nightwork\\test勤務表\\shifttable.accdb'
DB_PASSWORD = '0000'


class AccessDBReader:
    @staticmethod
    #指定月のdeptフィールドの値を取得し、Personオブジェクトを作成する
    def get_member(month):
        conn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DB_PATH + ';PWD=' + DB_PASSWORD + ';')
        cursor = conn.cursor()
        cursor.execute('SELECT uid, id, staffname, status, authority FROM tblStaff WHERE status <= 3')
        rows = cursor.fetchall()
        imutable_info_list = []
        for row in rows:
            imutable_info = ImutableInfo(*row)
            imutable_info_list.append(imutable_info)
        imutable_info_list_obj = ImutableInfoList(imutable_info_list)
        
        persons = []
        for imutable_info in imutable_info_list_obj.imutable_info_list:
            cursor.execute('SELECT modalityName, status, skill FROM tblSkill WHERE uid = ?', (imutable_info.uid,))
            rows = cursor.fetchall()
            staff_skills = [Skill(*row) for row in rows]
            skills = Skills(staff_skills)
            year = datetime.now().year
            date = datetime(year, month, 1).strftime('%Y/%m/%d')
            cursor.execute('SELECT dept FROM tblDept WHERE date = ?', (date,))
            dept = cursor.fetchone()[0]
            modality = Modality(dept)
            person = Person(imutable_info, skills, modality)
            persons.append(person)
        member = Member(persons)
        return member

    @staticmethod
    #staffの勤務情報を取得する
    def get_shifts(member, date):
        
        conn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DB_PATH + ';PWD=' + DB_PASSWORD + ';')
        cursor = conn.cursor()
        
        start_date = date.replace(day=1) - datetime.timedelta(days=30)
        end_date = (date.replace(day=1) + datetime.timedelta(days=60)) - datetime.timedelta(days=1)
        
        shifts = []
        for person in member.person_list:
            cursor.execute('SELECT workdate, shift FROM tblShift WHERE uid = ? AND workdate BETWEEN ? AND ?', (person.uid, start_date, end_date))
            rows = cursor.fetchall()
            date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            for shift_date in date_range:
                shift_row = next((row for row in rows if row[0] == shift_date), None)
                if shift_row:
                    shift = Shift(person, *shift_row)
                else:
                    shift = Shift(person, shift_date, None)
                shifts.append(shift)
        # この関数を実行すると、指定された日付の前後1ヶ月間のシフト情報を含むShiftsオブジェクトが返されます。
        # Shiftsオブジェクトは、指定された期間内のすべての日付に対してShiftオブジェクトのリストを持っています。
        # 各Shiftオブジェクトは、特定の日付の特定のPersonのシフト情報を表します。
        # もしPersonがその日にシフトを持っていない場合、Shiftオブジェクトのshift属性はNoneになります。
        return Shifts(shifts)


    