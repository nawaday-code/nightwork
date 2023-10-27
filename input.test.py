import sys
# sys.path.append('/Users/nawayuuki/ProgramSpace/nightwork/nightwork/src')
from src.Util.input import *

def test_input_methods():
    
    assert hasattr(AccessDBReader, 'get_all_staff_and_skills'), "AccessDBReaderには 'get_all_staff_and_skills' メソッドがありません"
    assert hasattr(AccessDBReader, 'get_shifts'), "AccessDBReaderには 'get_shifts' メソッドがありません"
    
    # メソッドの戻り値をテストする
    reader = AccessDBReader()
    staff_and_skills = reader.get_all_staff_and_skills()
    assert len(staff_and_skills.person_list) > 0, "'get_all_staff_and_skills' は空のリストを返しました"
    print(staff_and_skills.person_list[0].staffname)
    
    from datetime import date
    shifts = reader.get_shifts(staff_and_skills, date.today())
    assert len(shifts.getlist) > 0, "'get_shifts' は空のリストを返しました"
    for i in range(min(120, len(shifts.getlist))):
        print(shifts.getlist[i].person.staffname, shifts.getlist[i].workdate, shifts.getlist[i].shift)

if __name__ == "__main__":
    test_input_methods()


