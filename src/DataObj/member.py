from .person import Person

class Member:
    def __init__(self, person_list):
        assert all(isinstance(person, Person) for person in person_list), "person_listはPersonオブジェクトのリストでなければなりません"
        self.__person_list = person_list

    def get_all(self):
        return self.__person_list
    
    def _filter_persons_by_status(self, statuses):
        filtered_persons = []
        for person in self.__person_list:
            for skill in person.skills:
                if skill.status in statuses:
                    filtered_persons.append(person.id)
                    break
        return filtered_persons

    def get_Nr(self):
        return self._filter_persons_by_status([1, 2])

    def get_Ndaily(self):
        return self._filter_persons_by_status(["休日勤"])

    def get_Nnight(self):
        return self._filter_persons_by_status(["夜勤"])

    def get_Nboth(self):
        daily = set(self._filter_persons_by_status(["休日勤"]))
        night = set(self._filter_persons_by_status(["夜勤"]))
        return list(daily.union(night))

    def get_Ns(self):
        daily = set(self._filter_persons_by_status(["休日勤"]))
        night = set(self._filter_persons_by_status(["夜勤"]))
        return list(daily.intersection(night))

    def _map_modality_to_group(self, person):
        modality_to_group = {
            'MR': 0, 'TV': 1, 'HT': 2, 'MN': 3, 'XA': 4,
            'RT': 5, 'XP': 6, 'CT': 7, 'XO': 8
        }
        return modality_to_group.get(person.assigned_modality, 9)

    def get_G(self):
        g = [[] for _ in range(10)]
        for person in self.__person_list:
            group_index = self._map_modality_to_group(person)
            g[group_index].append(person.id)
        return g

    def get_Core(self):
        modality_leaders = []
        for person in self.__person_list:
            for skill in person.skills:
                if skill.skill_score % 10 == 3:
                    modality_leaders.append(person.id)
                    break
        return modality_leaders

    def get_Core_G(self):
        core_g = [[] for _ in range(10)]
        for person in self.__person_list:
            for skill in person.skills:
                if skill.skill_score % 10 == 3:
                    group_index = self._map_modality_to_group(person)
                    core_g[group_index].append(person.id)
                    break
        return core_g



    def get_by_modality(self, assigned_modality):
        return [person.uid for person in self.__person_list if person.assigned_modality == assigned_modality]
