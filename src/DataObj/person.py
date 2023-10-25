

class Skill:
    def __init__(self, modalities, status, skill_score):
        assert isinstance(modalities, str), "modalitiesはstr型でなければなりません"
        assert isinstance(status, str), "statusはstr型でなければなりません"
        assert isinstance(skill_score, int), "skill_scoreはint型でなければなりません"
        self.__modalities = modalities
        self.__status = status
        self.__skill_score = skill_score

    @property
    def modalities(self):
        return self.__modalities

    @property
    def status(self):
        return self.__status

    @property
    def skill_score(self):
        return self.__skill_score

class Skills:
    def __init__(self, skill_list):
        assert all(isinstance(skill, Skill) for skill in skill_list), "skill_listはSkillオブジェクトのリストでなければなりません"
        self.__skill_list = skill_list

    @property
    def skill_list(self):
        return self.__skill_list
    
    #skillの表示の仕方をここで追加・編集
    

class ImutableInfo:
    def __init__(self, uid, id, staffname, status, authority):
        assert isinstance(uid, int), "uidはint型でなければなりません"
        assert isinstance(id, str), "idはstr型でなければなりません"
        assert isinstance(staffname, str), "staffnameはstr型でなければなりません"
        assert isinstance(status, int), "statusはint型でなければなりません"
        assert isinstance(authority, int), "authorityはint型でなければなりません"
        self.__uid = uid
        self.__id = id
        self.__staffname = staffname
        self.__status = status
        self.__authority = authority

    @property
    def uid(self):
        return self.__uid

    @property
    def id(self):
        return self.__id

    @property
    def staffname(self):
        return self.__staffname

    @property
    def status(self):
        return self.__status

    @property
    def authority(self):
        return self.__authority

class ImutableInfoList:
    def __init__(self, imutable_info_list):
        assert all(isinstance(info, ImutableInfo) for info in imutable_info_list), "imutable_info_listはImutableInfoオブジェクトのリストでなければなりません"
        self.__imutable_info_list = imutable_info_list

    @property
    def imutable_info_list(self):
        return self.__imutable_info_list


class Person:
    def __init__(self, imutableInfo, skills):
        self.__uid = imutableInfo.uid
        self.__id = imutableInfo.id
        self.__staffname = imutableInfo.staffname
        self.__status = imutableInfo.status
        self.__authority = imutableInfo.authority
        self.__skills = skills.skill_list
