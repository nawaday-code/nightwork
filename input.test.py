import sys
sys.path.append('/Users/nawayuuki/ProgramSpace/nightwork/nightwork/src')
from src.Util.input import *

def test_input_methods():
    
    assert hasattr(input, 'get_all_staff_and_skills'), "input has no method 'get_all_staff_and_skills'"
    assert hasattr(input, 'get_shifts'), "input has no method 'get_shifts'"
    
    # Test the return values of the methods
    reader = input.AccessDBReader()
    staff_and_skills = reader.get_all_staff_and_skills()
    assert len(staff_and_skills.person_list) > 0, "get_all_staff_and_skills returned an empty list"
    print(staff_and_skills.person_list[0].imutable_info.staffname)
    
    from datetime import date
    shifts = reader.get_shifts(staff_and_skills, date.today())
    assert len(shifts.shift_list) > 0, "get_shifts returned an empty list"
    print(shifts.shift_list[0].person.imutable_info.staffname, shifts.shift_list[0].workdate, shifts.shift_list[0].shift)

if __name__ == "__main__":
    test_input_methods()


