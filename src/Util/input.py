#Access dbからデータを読み込むユーティリティクラス
import pyodbc
import DataObj.person
import DataObj.member

class AccessDBReader:
#staff全員の情報を取得する
    def get_all_staff_and_skills():
        conn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=shifttable.accdb;')
        cursor = conn.cursor()
        cursor.execute('SELECT uid, id, staffname, status, authority FROM staff')
        rows = cursor.fetchall()
        imutable_info_list = []
        for row in rows:
            imutable_info = ImutableInfo(row[0], row[1], row[2], row[3], row[4])
            imutable_info_list.append(imutable_info)
        imutable_info_list_obj = ImutableInfoList(imutable_info_list)
        
        persons = []
        for imutable_info in imutable_info_list_obj.imutable_info_list:
            cursor.execute('SELECT modalities, status, skill_score FROM tblSkill WHERE uid = ?', imutable_info.uid)
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
#staffの勤務情報を取得する
    
    
    def get_shifts(self, member, date):
        from datetime import timedelta
        from Entity.shift import Shift, Shifts
        
        conn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=shifttable.accdb;')
        cursor = conn.cursor()
        
        start_date = date - timedelta(days=30)
        end_date = date + timedelta(days=30)
        
        shifts = []
        for person in member.person_list:
            cursor.execute('SELECT workdate, shift FROM tblShift WHERE uid = ? AND workdate BETWEEN ? AND ?', (person.uid, start_date, end_date))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    shift = Shift(person, row[0], row[1])
                    shifts.append(shift)
            else:
                for i in range((end_date - start_date).days + 1):
                    shift_date = start_date + timedelta(days=i)
                    shift = Shift(person, shift_date, None)
                    shifts.append(shift)
        # この関数を実行すると、指定された日付の前後1ヶ月間のシフト情報を含むShiftsオブジェクトが返されます。
        # Shiftsオブジェクトは、指定された期間内のすべての日付に対してShiftオブジェクトのリストを持っています。
        # 各Shiftオブジェクトは、特定の日付の特定のPersonのシフト情報を表します。
        # もしPersonがその日にシフトを持っていない場合、Shiftオブジェクトのshift属性はNoneになります。
        return Shifts(shifts)


