import json

class Settings:
    def __init__(self, trust_path):
        self.__settings_data = self.__load_settings(trust_path.value)
        self.__modalities = self.__settings_data.get('Modalities', [])
        self.__shifts = self.__settings_data.get('Shifts', [])
        self.__working_groups = self.__settings_data.get('WorkingGroups', [])
        self.__working_status = self.__settings_data.get('WorkingStatus', [])
        self.__pulp_var = self.__settings_data.get('PulpVar', [])
        self.__pulp_items = self.__settings_data.get('PulpItems', [])
        self.__modality_config_header = self.__settings_data.get('ModalityConfigHeader', [])
        self.__work_count_header = self.__settings_data.get('WorkCountHeader', [])

    def __load_settings(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @property
    def modalities(self):
        return self.__modalities

    @property
    def shifts(self):
        return self.__shifts

    @property
    def working_groups(self):
        return self.__working_groups

    @property
    def working_status(self):
        return self.__working_status

    @property
    def pulp_var(self):
        return self.__pulp_var

    @property
    def pulp_items(self):
        return self.__pulp_items
    
    # 勤務の集合 W を取得するメソッド
    def get_W(self):
        return {shift['workdict'] for shift in self.__shifts}

    # 休診日日勤の集合を取得するメソッド
    def get_day_works(self):
        return {item['searchStr'] for item in self.__work_count_header if '日' in item['acronym']}

    # 夜勤の集合を取得するメソッド
    def get_night_works(self):
        return {item['searchStr'] for item in self.__work_count_header if '夜' in item['acronym']}

    # 休診日日勤・夜勤の集合を取得するメソッド
    def get_day_and_night_works(self):
        day_works = self.get_day_works()
        night_works = self.get_night_works()
        return day_works.union(night_works)

    # 夜勤明けの集合を取得するメソッド
    #_modality_config_headerのacronym"NS"の"searchStr”からdayとnightを抜いて作成してもいいかも
    def get_ake(self):
        return {shift['acronym'] for shift in self.__shifts if '明' in shift['acronym']}

    # 診療日日勤の集合を取得するメソッド
    def get_target_modalities(self):
        return {modality['acronym'] for modality in self.__modalities if modality.get('target', False)}
    
    # その他の勤務の集合を取得するメソッド
    def get_other(self):
        return {item['searchStr'] for item in self.__modality_config_header if item['acronym'] == 'BT'}

    # 休日の集合を取得するメソッド
    def get_dayoff(self):
        return {item['searchStr'] for item in self.__modality_config_header if item['acronym'] == 'DayOff'}

    # 休暇の集合を取得するメソッド
    def get_holiday(self):
        return {item['searchStr'] for item in self.__modality_config_header if item['acronym'] == 'Holiday'}

    # モダリティの集合を取得するメソッド
    def get_modality_acronyms(self):
        return {modality['acronym'] for modality in self.__modalities}
