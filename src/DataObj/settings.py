import json

class Settings:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        self.__modalities = config.get('Modalities', [])
        self.__shifts = config.get('Shifts', [])
        self.__modality_config_header = config.get('ModalityConfigHeader', [])
        self.__work_count_header = config.get('WorkCountHeader', [])
        self.__skills = config.get('Skills', [])
        self.__skill_types = config.get('SkillTypes', [])
        self.__registers = config.get('Registers', [])
        self.__working_groups = config.get('WorkingGroups', [])
        self.__working_status = config.get('WorkingStatus', [])

    @property
    def modalities(self):
        return self.__modalities

    @property
    def shifts(self):
        return self.__shifts

    @property
    def modality_config_header(self):
        return self.__modality_config_header

    @property
    def work_count_header(self):
        return self.__work_count_header

    @property
    def skills(self):
        return self.__skills

    @property
    def skill_types(self):
        return self.__skill_types

    @property
    def registers(self):
        return self.__registers

    @property
    def working_groups(self):
        return self.__working_groups

    @property
    def working_status(self):
        return self.__working_status
