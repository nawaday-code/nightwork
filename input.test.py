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
    print(staff_and_skills.person_list[0].imutable_info.staffname)
    
    from datetime import date
    shifts = reader.get_shifts(staff_and_skills, date.today())
    assert len(shifts.shift_list) > 0, "'get_shifts' は空のリストを返しました"
    print(shifts.shift_list[0].person.imutable_info.staffname, shifts.shift_list[0].workdate, shifts.shift_list[0].shift)

if __name__ == "__main__":
    test_input_methods()


