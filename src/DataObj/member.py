from .person import Person

class Member:
    def __init__(self, person_list):
        assert all(isinstance(person, Person) for person in person_list), "person_listはPersonオブジェクトのリストでなければなりません"
        self.__person_list = person_list

    def get_all(self):
        return self.__person_list

    def get_persons_by_modality(self, assigned_modality):
        return [person.uid for person in self.__person_list if person.assigned_modality == assigned_modality]
