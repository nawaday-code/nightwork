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
        self.pulpvar2num = { 'da':0, 'dm':1, 'dc':2, 'df':3, 'na':4, 'nm':5, 'nc':6, 'nn':7, 'dw':8, 'ew':9, 'do':10, 'ho':11, 'Ex':12, 'em':13 }
        self.pulpvar2num = {'mr':0, 'tv':1, 'ks':2, 'nm':3, 'ag':4, 'rt':5, 'xp':6, 'ct':7, 'xo':8, 'mg':9, 'mt':10, 'fr':11}
        
    # 辞書の値からキーを抽出
    def get_key_from_value(self, dicts, val):
        keys = [k for k, v in dicts.items() if v == val]
        if keys:
            return keys[0]
        return None

    @property
    def convert_table(self, filepath='converttable.dat'):
        dict = {}
        path = os.path.join(self.dat_dir, 'converttable.dat')

        with open(path, encoding="utf-8_sig") as f:
            for line in f:
                key, value = line.strip().split(',')
                dict.setdefault(key, int(value))
        return dict

    @property
    def shift2num_dict(self, filepath='converttable.dat'):
        dict = {}
        path = os.path.join(self.dat_dir, 'converttable.dat')

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
            alpha.insert(int(self.pulpvar2num[arr[0].lower()]), required_numbers)
        
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
            beta.insert(self.pulpvar2num[arr[0].lower()], lowLimit)

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
            gamma.insert(self.pulpvar2num[arr[0].lower()], core)    

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
            constants.insert(self.pulpvar2num[arr[0].lower()], lowLimit)

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


    def make_T(self):
        mydate = datetime.strptime(self.configvar['date'][0], '%Y/%m/%d')
        consecutivework = int(self.configvar['iota'][0])
        Tdict = {}
        T = []; Tr = []; Tclosed = []; Topened = []; Toutput = []
        pre = mydate - timedelta(days = consecutivework)
        post = mydate + relativedelta(months = 1)

        for d in range((post - pre).days + 1):
            strd = datetime.strftime(pre + timedelta(d), '%Y-%m-%d')
            Tdict[d] = strd
            T.append(d)

        # pre = mydate
        # post = post           
        # for d in range((post - pre).days + 1):
        #     strd = datetime.strftime(pre + timedelta(d), '%Y-%m-%d')
        #     day = self.get_key_from_value(Tdict, strd)
        #     Toutput.append(day)
        
        # pre = mydate
        # post = post - timedelta(days=1)
        # for d in range((post - pre).days + 1):
        #     strd = datetime.strftime(pre + timedelta(d), '%Y-%m-%d')
        #     day = self.get_key_from_value(Tdict, strd)
        #     Tr.append(day)
        #     holiday = JapanHoliday()
        #     if holiday.is_holiday(strd):
        #         Tclosed.append(day)
        #     else:
        #         Topened.append(day)


        return Tdict, T, Tr#, Tclosed, Topened, Toutput
datData = DatData()

d= datData.tokai_calendar
print(d)