import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import config


WORK2PULP_DICT = {'A日':'dA', 'M日':'dM', 'C日':'dC', 'F日':'dF', 'A夜':'nA', 'M夜':'nM', 'C夜':'nC', '明':'nn',
        'A宿':'nA', 'M宿':'nM', 'C宿':'nC',
        '日':'dW', '勤':'dW', '援':'eW', '張':'eW', 
        'RT':'dW','MR':'dW','TV':'dW','KS':'dW','NM':'dW', 'AG':'dW','XP':'dW',
        'MG':'dW','MT':'dW','CT':'dW','XO':'dW','FR':'dW','NF':'dW','AS':'dW','ET':'dW','半':'dW',
        '休':'do', '振':'do', '年':'ho','夏':'ho', '特':'ho', '希':'dW',
        '例外':'Ex'}
PULP2WORK_DICT = {'dA':'A日','dM':'M日','dC':'C日','dF':'F日','nA':'A夜','nM':'M夜','nC':'C夜','nn':'明','dW':'勤','eW':'他','do':'休','ho':'特','Ex':'ダ', 'emp':'空'}

class Staff:
    def __init__(self, uid, id, staffname):
        self.uid = int(uid)
        self.id = str(id)
        self.staffname = staffname
        self.dept = ""
        self.modality_skill ={}
        self.work_skill = {}

class StaffList():
    
    StaffList: dict[int, Staff]

    def __init__(self) -> None:
        
        self.StaffList = {}


class DatData:
    staffs: dict[int, Staff]
    def __init__(self):
        self.staffs = {}

        self.dat_dir = config.readSettingJson('DATA_DIR')
        # self.dat_dir = 'C:\\Users\\hhond\\source\\repos\\nightwork\\current_prog\\data'
        self.work2pulp_dict = WORK2PULP_DICT
        self.pulp2work_dict = PULP2WORK_DICT
        # self.pulpvar2num = { 'da':0, 'dm':1, 'dc':2, 'df':3, 'na':4, 'nm':5, 'nc':6, 'nn':7, 'dw':8, 'ew':9, 'do':10, 'ho':11, 'Ex':12, 'em':13 }
        # self.modality2num = {'mr':0, 'tv':1, 'ks':2, 'nm':3, 'ag':4, 'rt':5, 'xp':6, 'ct':7, 'xo':8, 'mg':9, 'mt':10, 'fr':11}
        self._W1_list = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho']
        self._W2_list = ['Ex']
        self._W3_list = ['emp']
        self._modality_list = ['mr', 'tv', 'ks', 'nm', 'ag', 'rt', 'xp', 'ct', 'xo', 'fr', 'mg', 'mt']
        self._group_list =  ['MR', 'TV', 'KS', 'NM', 'AG', 'RT', 'XP', 'CT', 'XO', 'FR']
        self._Ndum = [900, 901, 902, 903, 904, 905, 906, 907, 908, 909]
       
       #staffinfo, Nrdeptcore, skillを読み込み、個人情報を取得する
        self._get_staff_data()
        self._get_dept_and_modality_skills_data()
        self._get_work_skills_data()
       
        self._Nr, self._Gm, self._Core, self._dept_dict = self._read_Nr_Gm_Core()
        self._Nnight, self._Ndaily, self._Ns = self._read_skill()
        self._T_dict, self._T, self._Tr_dict, self._Tr = self._schedule_T()
        # self._F_previous = self.read_previous_request('previous.dat')
        # self._F_request = self.read_previous_request('request.dat')
        # self._F_request_dayoff = self.read_previous_request('request_dayoff.dat')
        # self._F_request_next_month = self.read_previous_request('request_nextmonth.dat')
        self._previous = self.read_previous_request_('previous.dat')
        self._request = self.read_previous_request_('request.dat')
        self._request_dayoff = self.read_previous_request_('request_dayoff.dat')
        self._request_next_month = self.read_previous_request_('request_nextmonth.dat')
        
    # 辞書の値からキーを抽出
    def get_key_from_value(self, dicts, val):
        keys = [k for k, v in dicts.items() if v == val]
        if keys:
            return keys[0]
        return None


    def _get_staff_data(self):
        staff_info_path = 'staffinfo.dat'
        path = os.path.join(self.dat_dir, staff_info_path)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                uid, id, name = line.split(',')
                self.staffs[int(uid)] = Staff(int(uid), id, name)


    def _get_dept_and_modality_skills_data(self):
        Nr_dept_core_path = 'Nrdeptcore.dat'
        modality_skills = ['rt', 'mr', 'tv', 'ks', 'nm', 'xp', 'ct', 'xo', 'ag', 'mg', 'mt']
        path = os.path.join(self.dat_dir, Nr_dept_core_path)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                line = line.strip()
                arr = []
                arr = line.split(',')
                uid = int(arr[0])
                if uid in self.staffs.keys():
                    self.staffs[uid].dept = str(arr[1])
                    i = 2
                    for key in modality_skills:
                        self.staffs[uid].modality_skill[key] = int(arr[i])
                        i += 1

    def _get_work_skills_data(self):
        skill_path = 'skill.dat'
        work_skills = ['ag', 'mr', 'ct', 'fr', 'night', 'daily']
        path = os.path.join(self.dat_dir, skill_path)

        with open(path, encoding='utf-8_sig') as f:
            for line in f:
                line = line.strip()
                arr = []
                arr = line.split(',')
                uid = int(arr[0])
                if uid in self.staffs.keys():
                    i = 1
                    for skill in work_skills:
                        self.staffs[uid].work_skill[skill] = int(arr[i])
                        i += 1
            
                

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
    def W_list(self):
        return self._W1_list + self._W2_list + self._W3_list
    
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
                if len(line[1:]) == 1:
                    value = line[1]
                    if value.isdigit():
                        value = int(value)
                else:
                    value = line[1:]
                    for i in range(len(value)):
                        if value[i].isdigit():
                            value[i] = int(value[i])
                d[key] = value
        return d
    
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
        first_day_of_month = datetime.strptime(self.configvar['date'], '%Y/%m/%d')
        consecutivework = self.configvar['iota']
        current_date = first_day_of_month - timedelta(days = consecutivework)
        end_date = first_day_of_month + relativedelta(months = 1)
        
        i = 0
        j = 0
        while current_date <= end_date:
            T_dict[current_date] = i
            T.append(current_date)
            if first_day_of_month <= current_date <= end_date:
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
        dept_dict = {}
        path = os.path.join(self.dat_dir, filepath)

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                arr = line.strip().split(',')
                uid = int(arr[0])
                dept = arr[1].lower()
                dept_dict[uid] = dept
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

        return sorted(_Nr), [sorted(m) for m in _Gm], [sorted(m) for m in _Core], dept_dict
    
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

    # def read_previous_request(self, filepath):
    #     data = []
    #     _F_list = []
    #     configvar = self.configvar
    #     dict = self.convert_table
    #     date = datetime.strptime(configvar['date'], '%Y/%m/%d')
    #     path = os.path.join(self.dat_dir, filepath)
    #     with open(path, encoding='utf-8_sig') as f:
    #         lines = f.readlines()

    #         if not lines or all(line.strip() == '' for line in lines):  # ファイルが空または全てが空文字列の場合
    #             return _F_list
            
    #         for line in lines:
    #             line = line.strip()
    #             data.append(list(line.split(',')))

    #         for d in data:
    #             uid = int(d[0])
    #             if uid in self._dept_dict.keys():
    #                 if not self._dept_dict[uid].upper()  in ['AS','ET']:
    #                     _list = []
    #                     _list.append(int(d[0]))
    #                     day = date + timedelta(days=int(d[1]))
    #                     _list.append(day)
    #                     work = self.get_key_from_value(dict, int(d[2]))
    #                     _list.append(self.work2pulp_dict[work])
    #                     _F_list.append(_list)
        
    #     return _F_list                

    def read_previous_request_(self, filepath):
        data = []
        _F_list = []
        configvar = self.configvar
        dict = self.convert_table
        date = datetime.strptime(configvar['date'], '%Y/%m/%d')
        path = os.path.join(self.dat_dir, filepath)
        with open(path, encoding='utf-8_sig') as f:
            lines = f.readlines()

            if not lines or all(line.strip() == '' for line in lines):  # ファイルが空または全てが空文字列の場合
                return _F_list
            
            for line in lines:
                line = line.strip()
                data.append(list(line.split(',')))

            for d in data:
                uid = int(d[0])
                if uid in self._dept_dict.keys():
                    if not self._dept_dict[uid].upper()  in ['AS','ET']:
                        _list = []
                        _list.append(int(d[0]))
                        day = date + timedelta(days=int(d[1]))
                        _list.append(day)
                        work = self.get_key_from_value(dict, int(d[2]))
                        _list.append(work)
                        _F_list.append(_list)
        
        return _F_list  
        
    def calc_next_month_alpha(self):
        
        W = self._W1_list
        work2pulp = self.work2pulp_dict
        next_month_alpha = [[0] for _ in range(len(W))]

        for n, t, w in self._request_next_month:
            req_work = work2pulp[w]
            next_month_alpha[W.index(req_work)] += 1
        
        #ただし、明けに関しては3名確定
        next_month_alpha[W.index('nn')] = 3

        return next_month_alpha

    def calc_mean_works(self):
        alpha = self.alpha

        daily_work_count = sum([sum(row) for row in alpha[:4]])
        night_work_count = sum([sum(row) for row in alpha[4:7]])

        return daily_work_count / len(self._Ndaily) + night_work_count / len(self._Nnight)
    

    def calc_mean_works_on_close(self):
        required_staffs_on_close = 11
        Tclose = 0
        for t in self._Tr:
            if t in self.tokai_calendar:
                Tclose += 1

        return Tclose * required_staffs_on_close / len(list(set(self._Nnight) | set(self._Ndaily)))

    def output_x(self, x, N, T, W):
        with open(os.path.join(self.dat_dir, 'x.dat'), 'w')  as f:
            for n in N:
                for t in T:
                    for w in W:
                        f.write(f"{n},{t},{w},{x[n, t, w].varValue}\n")

    def read_x(self):     
        x = {}
        with open(os.path.join(self.dat_dir, 'x.dat'), 'r') as f:
            for line in f:
                line = line.strip()
                arr = line.split(',')
                n = int(arr[0])
                t = datetime.strptime(arr[1], '%Y-%m-%d %H:%M:%S')
                w = arr[2]
                value = float(arr[3]) if arr[3] != 'None' else 0.0
                x[(n, t, w)] = value
        return x
        
    def convert_outcome2list(self, x, N, Tr, W, invW):

        x_list = []
        for n in N:
            for t in Tr:
                for w in W:
                    if x[n, t, w] == 1:
                        if w != 'emp': 
                            shift = []
                            shift.append(n)
                            shift.append(t)
                            shift.append(invW[w])
                            x_list.append(shift)

        return x_list  
    
    def rewrite_request(self, x_list, request):

        for n , t, w in request:
            for  i in range(len(x_list)):
                if x_list[i][0] == n and x_list[i][1] == t:

                    x_list[i][2] = w
                    break
        return x_list

    def output_xlist2shiftdat(self, x_list):
        basic_date = datetime.strptime(self.configvar['date'], '%Y/%m/%d')
        with open(os.path.join(self.dat_dir, 'new_shift.dat'), 'w', encoding='utf-8') as f:        
            for i in range(len(x_list)):
                uid = x_list[i][0]
                date = (x_list[i][1] - basic_date).days
                shift = self.convert_table[x_list[i][2]]
                f.write(f"{uid},{date},{shift}\n")


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

    @property
    def Tclose(self):
        Tclose = []
        for t in self._Tr:
            if t in self.tokai_calendar:
                Tclose.append(t)
        return Tclose
    @property
    def prebious(self):
        return self._previous
    
    @property
    def request(self):
        return self._request
    
    @property
    def request_dayoff(self):
        return self._request_dayoff
    
    @property
    def request_next_month(self):
        return self._request_next_month

    @property
    def F_previous(self):
        _f = self._previous
        for i in range(len(_f)):
            _f[i][2] = self.work2pulp_dict[_f[i][2]]
        return _f

    @property
    def F_request(self):
        _f = self._request
        for i in range(len(_f)):
            _f[i][2] = self.work2pulp_dict[_f[i][2]]
        return _f

    @property
    def F_request_dayoff(self):
        _f = self._request_dayoff
        for i in range(len(_f)):
            _f[i][2] = self.work2pulp_dict[_f[i][2]]
        return _f

    @property
    def F_request_next_month(self):
        _f = self._request_next_month
        for i in range(len(_f)):
            _f[i][2] = self.work2pulp_dict[_f[i][2]]
        return _f
    

# datData = DatData()

# x = datData.read_x()

# print(x)
# list_x = datData.convert_outcome2list(x, datData.N, datData.Tr, datData.W_list, datData.pulp2work_dict)
# new_list_x = datData.rewrite_request(list_x, datData._request)
# output_list_x = datData.reformat_xlist2shiftdat(new_list_x)

# for n, t, w in output_list_x:
#     print(f"{n},{t},{w}")
# req= datData.F_request
# gl = datData.modality_list
# # for uid, t, shift in req:
# #     print(str(uid) + '__' + str(t) + '__' + shift)
# alpha = datData.alpha
# print(len(alpha[0]))
# al = datData.pulpvar_list
# gm = datData.Gm
# for g, l in zip(alpha, al):
#     print(str(l) + str(g))

# print(datData.calc_mean_works_on_close())
# print(datData.calc_mean_works())
# for date in d.keys():
#     print(str(date) + '___' + str(d[date]))
#     if date in t_cal.keys():
#         print(str(date) + '_closed')
