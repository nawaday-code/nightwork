import json

class Settings:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.__work = config['勤務の集合']
        self.__day_off_day = config['休診日日勤の集合']
        self.__night = config['夜勤の集合']
        self.__day_off_night = config['休診日日勤・夜勤の集合']
        self.__after_night = config['夜勤明けの集合']
        self.__day_work = config['診療日日勤の集合']
        self.__other_work = config['その他の勤務の集合']
        self.__holiday = config['休日の集合']
        self.__vacation = config['休暇の集合']
        self.__modality = config['モダリティの集合']

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

