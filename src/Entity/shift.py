from datetime import date
from src.DataObj.person import Person 

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
    #名前付きコンストラクタで、あらゆる形状のshiftオブジェクトを入力可能にする予定（必要があれば）
    #名前付きコンストラクタを実装する場合、最後にShiftオブジェクトのリストに形成して、このクラスのコンストラクタに通すこと（検証の共有）
    def __init__(self, shift_list):
        assert all(isinstance(shift, Shift) for shift in shift_list), "shift_listはShiftオブジェクトのリストでなければなりません"
        self.__shift_list = shift_list

    @property
    def getlist(self):
        return self.__shift_list

    #Shiftをあらゆる形状で取得するメソッドを追加予定（主に清水さん宛）


