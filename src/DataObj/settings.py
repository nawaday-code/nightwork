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
    def work(self):
        return self.__work

    @property
    def day_off_day(self):
        return self.__day_off_day

    @property
    def night(self):
        return self.__night

    @property
    def day_off_night(self):
        return self.__day_off_night

    @property
    def after_night(self):
        return self.__after_night

    @property
    def day_work(self):
        return self.__day_work

    @property
    def other_work(self):
        return self.__other_work

    @property
    def holiday(self):
        return self.__holiday

    @property
    def vacation(self):
        return self.__vacation

    @property
    def modality(self):
        return self.__modality

