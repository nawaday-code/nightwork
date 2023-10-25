class Shift:
    def __init__(self, person, workdate, shift):
        assert person is None or isinstance(person, Person), "personはNoneまたはPerson型でなければなりません"
        assert isinstance(workdate, date), "workdateはdate型でなければなりません"
        assert shift is None or isinstance(shift, str), "shiftはNoneまたはstr型でなければなりません"
        self.__person = person
        self.__workdate = workdate
        self.__shift = shift

    @property
    def person(self):
        return self.__person

    @property
    def workdate(self):
        return self.__workdate

    @property
    def shift(self):
        return self.__shift

class Shifts:
    def __init__(self, shift_list):
        assert all(isinstance(shift, Shift) for shift in shift_list), "shift_listはShiftオブジェクトのリストでなければなりません"
        self.__shift_list = shift_list
