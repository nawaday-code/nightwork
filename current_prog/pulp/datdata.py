import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import config


Wdict = {'A日':'dA', 'M日':'dM', 'C日':'dC', 'F日':'dF', 'A夜':'nA', 'M夜':'nM', 'C夜':'nC', '明':'nn',
        'A宿':'nA', 'M宿':'nM', 'C宿':'nC',
        '日':'dW', '勤':'dW', '援':'eW', '張':'eW', 
        'RT':'dW','MR':'dW','TV':'dW','KS':'dW','NM':'dW', 'AG':'dW','XP':'dW',
        'MG':'dW','MT':'dW','CT':'dW','XO':'dW','FR':'dW','NF':'dW','AS':'dW','ET':'dW','半':'dW',
        '休':'do', '振':'do', '年':'ho','夏':'ho', '特':'ho',
        '例外':'Ex'}
class DatData:

    def __init__(self):
        
        self.dat_dir = config.readSettingJson('DATA_DIR')
        self.work2pulp_dict = Wdict
        # self.pulpvar2num = { 'da':0, 'dm':1, 'dc':2, 'df':3, 'na':4, 'nm':5, 'nc':6, 'nn':7, 'dw':8, 'ew':9, 'do':10, 'ho':11, 'Ex':12, 'em':13 }
        # self.modality2num = {'mr':0, 'tv':1, 'ks':2, 'nm':3, 'ag':4, 'rt':5, 'xp':6, 'ct':7, 'xo':8, 'mg':9, 'mt':10, 'fr':11}
        self._W1_list = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho', 'Ex', 'em']
        self._W2_list = ['Ex']
        self._W3_list = ['em']
        self._modality_list = ['mr', 'tv', 'ks', 'nm', 'ag', 'rt', 'xp', 'ct', 'xo', 'fr', 'mg', 'mt']
        self._group_list =  ['MR', 'TV', 'KS', 'NM', 'AG', 'RT', 'XP', 'CT', 'XO', 'FR']
        self._Ndum = [900, 901, 902, 903, 904, 905, 906, 907, 908, 909]
        self._Nr, self._Gm, self._Core = self._read_Nr_Gm_Core()
        self._Nnight, self._Ndaily, self._Ns = self._read_skill()
        self._T_dict, self._T, self._Tr_dict, self._Tr = self._schedule_T()

    # 辞書の値からキーを抽出
    def get_key_from_value(self, dicts, val):
        keys = [k for k, v in dicts.items() if v == val]
        if keys:
            return keys[0]
        return None

    @property
    def modality_list(self):
        return self._modality_list
    
    @property
    def pulpvar_list(self):
        return self._W1_list
    
    @property
    def W1_list(self):
        return self._W1_list
    
    @property
    def W2_list(self):
        return self._W2_list
    
    @property
    def W3_list(self):
        return self._W3_list
    
    @property
    def convert_table(self, filepath='converttable.dat'):
        dict = {}
        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                key, value = line.strip().split(',')
                dict.setdefault(key, int(value))
        return dict

    @property
    def shift2num_dict(self, filepath='converttable.dat'):
        dict = {}
        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                key, value = line.strip().split(',')
                dict.setdefault(key, int(value))
        return dict

    @property
    def alpha(self, filepath = 'alpha.dat'):
        d = []
        alpha = []
        path = os.path.join(self.dat_dir, filepath)
        
        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                d.append(list(line.split(',')))
        
        for arr in d:
            required_numbers = []
            for i in arr[1:]:
                required_numbers.append(int(i))
            alpha.insert(self._W1_list.index(arr[0]), required_numbers)
        
        return alpha
    @property
    def beta(self, filepath = 'beta.dat'):
        d = []    
        beta = []

        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding="utf-8_sig") as f:    
        # with open(settings.BASE_DIR + '\\data\\beta.dat', encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                d.append(list(line.split(',')))
            
        for arr in d:
            lowLimit = []
            for i in arr[1:]:
                lowLimit.append(int(i))
            beta.insert(self._modality_list.index(arr[0].lower()), lowLimit)

        return beta
        
    @property
    def gamma(self, filepath='gamma.dat'):
        d = []
        gamma = []
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding="utf-8_sig") as f:    
        # with open(settings.BASE_DIR + '\\data\\gamma.dat', encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                d.append(list(line.split(',')))
                
        for arr in d:
            core = []
            for i in arr[1:]:
                core.append(int(i))
            gamma.insert(self._modality_list.index(arr[0].lower()), core)    

        return gamma            

    @property
    def configvar(self, filepath='configvar.dat'):
        d = {}
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip().split(',')
                key = line[0]
                value = line[1:]
                d[key] = value
        return d
    
    @property
    def previous(self, filepath='previous.dat'):
        d = []
        Fprev = []
        configvar = self.configvar
        dict = self.convert_table
        date = datetime.strptime(configvar['date'][0], '%Y/%m/%d')
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding='utf-8_sig') as f:
            for line in f:
                line = line.strip()
                d.append(list(line.split(',')))
        
            for arr in d:
                prev = []
                prev.append(int(arr[0]))
                day = datetime.strftime(date + timedelta(days=int(arr[1])), '%Y/%m/%d')
                prev.append(day)
                prev.append(self.get_key_from_value(dict, int(arr[2])))
                Fprev.append(prev)
        
        return Fprev    


    @property
    def modalityconstants(self, filepath='modalityconstants.dat'):
        d = []    
        constants = []
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding="utf-8_sig") as f:    
            for line in f:
                line = line.strip()
                d.append(list(line.split(',')))
            
        for arr in d:
            lowLimit = []
            for i in arr[1:]:
                lowLimit.append(int(i))
            constants.insert(self._modality_list.index(arr[0].lower()), lowLimit)

        return constants

    @property
    def tokai_calendar(self, filepath='tokai-calendar.csv'):
        dict = {}
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding='cp932') as f:
            for line in f:
                if not line[0] == '#':
                    key, value = line.strip().split(',')
                    key = datetime.strptime(key, '%Y/%m/%d')
                    dict.setdefault(key, value)
        return dict

    def _schedule_T(self):
        T_dict = {}
        Tr_dict = {}
        T = [];
        Tr = [] 
        first_day_of_month = datetime.strptime(self.configvar['date'][0], '%Y/%m/%d')
        consecutivework = int(self.configvar['iota'][0])
        current_date = first_day_of_month - timedelta(days = consecutivework)
        end_date = first_day_of_month + relativedelta(months = 1)
        
        i = 0
        j = 0
        while current_date <= end_date:
            T_dict[current_date] = i
            T.append(current_date)
            if first_day_of_month <= current_date < end_date:
                Tr_dict[current_date] = j
                Tr.append(current_date)
                j += 1
            current_date += timedelta(days=1)
            i += 1

        return T_dict, T, Tr_dict, Tr
    
    @property
    def staff_list(self, filepath='staffinfo.dat'):
        dict = {}
        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                uid, id, name = line.split(',')
                dict[int(uid)] = {'uid': int(uid), 'id': id, 'name': name}
        return dict        

    def _read_Nr_Gm_Core(self, filepath='Nrdeptcore.dat'):

        _Nr = []
        _Gm = [[] for _ in range(len(self._modality_list))]
        _Core = [[] for _ in range(len(self._modality_list))]

        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                arr = line.strip().split(',')
                uid = int(arr[0])
                dept = arr[1].lower()

                if dept != 'as' and arr[3] != 'et':
                    _Nr.append(uid)

                    if dept in self._modality_list:
                        index = self._modality_list.index(dept)
                        _Gm[index].append(uid)
                        if arr[index + 3] == '6':
                            _Core[index].append(uid)


        for n in self._Ndum:
            for i in range(len(self._modality_list)):
                _Gm[i].append(n)
                _Core[i].append(n)

        return sorted(_Nr), [sorted(m) for m in _Gm], [sorted(m) for m in _Core]
    
    def _read_skill(self, filepath='skill.dat'):
        
        skill_list =['da', 'dm', 'dc', 'df', 'na', 'nm', 'nc']
        _Nnight = []
        _Ndaily = []
        _Ns = [[] for _ in range(len(skill_list))]

        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                arr = line.strip().split(',')
                uid = int(arr[0])

                if arr[5] == '2':
                    _Nnight.append(uid)
                if arr[6] == '2':
                    _Ndaily.append(uid)

                for i in range(1, 5):
                    if arr[i] == '2' and arr[6] == '2':     
                        _Ns[i-1].append(uid)

                for i in range(1, 4):
                    if arr[i] == '2' and arr[5] == '2':
                        _Ns[i+3].append(uid)

        for n in self._Ndum:
            for i in range(len(skill_list)):
                _Ns[i].append(n)

        return sorted(_Nnight), sorted(_Ndaily), [sorted(l) for l in _Ns]


    @property
    def Nr(self):
        return self._Nr
    
    @property
    def N(self):
        return self._Nr + self._Ndum
    
    @property
    def Gm(self):
        return self._Gm
    
    @property
    def Core(self):
        return self._Core
    
    @property
    def Nnight(self):
        return self._Nnight
    
    @property
    def Ndaily(self):
        return self._Ndaily
    
    @property
    def Nboth(self):
        return list(set(self._Nnight) | set(self._Ndaily))
    
    @property
    def Ns(self):
        return self._Ns
    
    @property
    def T_dict(self):
        return self._T_dict
    @property
    def T(self):
        return self._T
    
    @property
    def Tr_dict(self):
        return self._Tr_dict
    @property
    def Tr(self):
        return self._Tr



datData = DatData()

gm= datData.Gm
gl = datData.modality_list
for g, l in zip(gm, gl):
    print(str(l) + str(g))
# for date in d.keys():
#     print(str(date) + '___' + str(d[date]))
#     if date in t_cal.keys():
#         print(str(date) + '_closed')
