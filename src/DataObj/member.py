from person import Person

class Member:
    def __init__(self, person_list):
        assert all(isinstance(person, Person) for person in person_list), "person_listはPersonオブジェクトのリストでなければなりません"
        self.__person_list = person_list

    @property
    def person_list(self):
        return self.__person_list
