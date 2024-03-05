import os
import csv
import pulp
import datetime
import readdata as rd
import tokaifunc as tfunc
import config
import time
import datdata 

def calc_schedule():

    dat = datdata.DatData()

    # 変数
    # N = Nr + Ndummy 
    # Nr：スケジュールの対象となる技師の集合
    # Ndaily：休日勤が可能な技師集合　Nnight：夜勤が可能な技師集合　Nboth：どちらかできる技師の集合
    # Ns：各休日勤・夜勤が可能な技師集合
    # staff = {}
    # N = []; Nr = []; Ndum = []; Ndaily = []; Nnight = []; Nboth = []; Ns = []
    staff = dat.staff_list
    pulpvar_list = dat.pulpvar_list
    modality_list = dat.modality_list

    N = dat.N; 
    Nr = dat.Nr 
    Ndaily = dat.Ndaily
    Nnight = dat.Nnight
    Nboth = dat.Nboth
    Ns = dat.Ns
    Ndum = dat._Ndum

    # G：モダリティグループに属する技師集合
    # Core：モダリティリーダーを任せることのできる技師集合
    # G = 0:MR, 1:TV, 2:HT, 3:MN, 4:XA, 5:RT, 6:XP, 7:CT, 8:XO, 9:etc
    # G = []; Core = []
    Gm = dat.Gm
    Core = dat.Core


    # T：日にちの集合（前月13日分と次月1日分を含む）
    # Tr：スケジュールの対象となる日にちの集合
    # Topened：診療日となる日にちの集合
    # Tclosed：休診日となる日にちの集合
    # T_dict = {}
    # T = []; Tr = []; Tclosed = []; Topened = []
    T_dict = dat.T_dict
    T = dat.T
    Tr_dict = dat.Tr_dict
    Tr = dat.Tr
    Tclose = dat.Tclose
    tokai_calendar = dat.tokai_calendar
    
    # 勤務の種類
    # W1 = ['A日', 'M日', 'C日', 'F日', 'A夜', 'M夜', 'C夜', '明', '日勤', '他勤', '休日', '休暇']
    # 0:A日->dA, 1:M日->dM, 2:C日->dC, 3:F日->dF, 
    # 4:A夜->nA, 5:M夜->nM, 6:C夜->nC, 7:明 ->n,
    # 8:日勤->'', 9:他勤->e, 10:休日->/, 12:休暇->#
    # 初回作成時の明けなし宿直に関しては明けをつけなくても大丈夫。夜勤・明けの制約は作成月のみ
    # Wdict = {'A日':'dA', 'M日':'dM', 'C日':'dC', 'F日':'dF', 'A夜':'nA', 'M夜':'nM', 'C夜':'nC', '明':'nn',
    #         'A宿':'nA', 'M宿':'nM', 'C宿':'nC',
    #         '日':'dW', '勤':'dW', '援':'eW', '張':'eW', 
    #         'RT':'dW','MR':'dW','TV':'dW','KS':'dW','NM':'dW', 'AG':'dW','XP':'dW',
    #         'MG':'dW','MT':'dW','CT':'dW','XO':'dW','FR':'dW','NF':'dW','AS':'dW','ET':'dW','半':'dW',
    #         '休':'do', '振':'do', '年':'ho','夏':'ho', '特':'ho',
    #         '例外':'Ex'}
    # W1 = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho']
    # W2 = ['Ex']
    # W3 = ['emp']
    W1 = dat.W1_list
    W2 = dat.W2_list
    W3 = dat.W3_list
    W = W1 + W2 + W3

    # 禁止シフトの集合
    Q = ['n','n','n']

    MAXCONSECUTIVEWORKS = 12        #法律上可能な連続勤務日数
    REQUIRED_NUM_OF_COLOSED_DAY = 11 #休診日に必要な人数（日勤、夜勤、明け）



    
    # 日付ごとの制約条件変数
    # alpha[work][date]
    # alpha 0:A日,1:M日,2:C日,3:F日,4:A夜,5:M夜,6:C夜,7:明,8:日勤,9:他勤,10:休日,11:休暇
    # beta[modality][date]
    # beta 0:MR, 1:TV, 2:HT, 3:MN, 4:XA, 5:RT, 6:XP, 7:CT, 8:XO, 9:MG, 10:MT, 11:FR/NF
    # gamma[modality][date]
    # gamma 0:MR, 1:TV, 2:HT, 3:MN, 4:XA, 5:RT, 6:XP, 7:CT, 8:XO, 9:MG, 10:MT, 11:FR/NF
    alpha = dat.alpha
    beta = dat.beta
    gamma = dat.gamma
    next_month_alpha = dat.calc_next_month_alpha()

    # alpha = []; beta = []; gamma = []

    # # 前月分の勤務
    # Fprev = []; Fp = []
    # # 今月分の勤務希望
    # Frequ = []; Fr = []
    # # 休日希望
    # Frequ_dayoff = []; Frd = []
    F_previous = dat.F_previous
    F_request = dat.F_request
    F_request_dayoff = dat.F_request_dayoff
    F_request_next_month = dat.F_request_next_month
    #
    

    # staff = rd.read_staff_info()

    # Ndum = tfunc.make_Ndum(10)

    # Nr, G, Core = rd.read_Nr_Gm_Core(Ndum)
    # Nnight, Ndaily, Ns = rd.read_skill(Ndum)        #Nnight,Ndailyにはdummyはいない。
    # Nboth = list(set(Nnight) | set(Ndaily))
    
    # N = Nr + Ndum

    # alpha = rd.read_alpha()
    # beta = rd.read_beta()
    # gamma = rd.read_gamma()

    # createDate:作成日時 epsilon:夜勤日勤回数の上限 iota:連続勤務日数 kappa:所定労働時間
    # myu:休日数 nyu1,2,3:連休数 rho:休日数の下限 lam:勤務間隔の荷重係数
    # createDate, epsilon, iota, kappa, myu, nyu, rho, lam, calctime = rd.read_config_var()
    configvar = dat.configvar
    create_date = configvar['date']
    night_and_dailiy_work_limit = configvar['epsilon']
    consecutive_work_limit = configvar['iota']
    holidays = configvar['myu']
    config_holidays = configvar['nyu']
    lam = [1,1,1,1,1,1,1,1,1,1,1]
    default_two_consecutive_holidays = config_holidays[0] + config_holidays[1]*2 + config_holidays[2]*3
    # default_two_consecutive_holidays = nyu[0] + nyu[1]*2 + nyu[2]*3
    default_three_consecutive_holidays = config_holidays[1] + config_holidays[2]*1
    default_four_consecutive_holidays = config_holidays[2]

    # 夜勤・休日日勤平均回数
    mean_works =dat.calc_mean_works()
    # mean_works = tfunc.calc_mean_of_night_and_daily(alpha, len(Ndaily), len(Nnight))
    # 休診日かかる夜勤・日勤平均回数=休診日 * 休診日に必要な人数 / 夜勤・日勤対応スタッフ数
    mean_works_on_close = dat.calc_mean_works_on_close()
    # mean_works_on_close = len(Tclosed) * REQUIRED_NUM_OF_COLOSED_DAY / len(Nboth)
    # Tdict, T, Tr, Tclosed, Topened, Toutput = tfunc.make_T(createDate, iota)

    # Fprev = rd.read_previous(createDate)
    # Frequ = rd.read_request(createDate)

    # Fp = tfunc.reformat_F(Fprev, Wdict, Tdict)
    # Fr = tfunc.reformat_F(Frequ, Wdict, Tdict)


# ***********************************************************************
# 最小化問題を記述
# ***********************************************************************
    model = pulp.LpProblem(sense=pulp.LpMinimize)

# ***********************************************************************
# 変数
# ***********************************************************************
    # x[i, j, k] 技師iがj日の勤務kであるかどうか・・・(1)
    x = pulp.LpVariable.dicts('x', [(n, t, w) for n in N for t in T for w in W], cat='Binary')

    #ダミー技師の総数
    dummy = pulp.LpVariable('dummy', cat='Continuous')

    # 勤務間隔変数
    work_interval1 = pulp.LpVariable.dicts('work_interval1', [(n, t) for n in Nboth for t in Tr], cat='Binary')
    work_interval2 = pulp.LpVariable.dicts('work_interval2', [(n, t) for n in Nboth for t in Tr], cat='Binary')
    work_interval3 = pulp.LpVariable.dicts('work_interval3', [(n, t) for n in Nboth for t in Tr], cat='Binary')
    work_interval4 = pulp.LpVariable.dicts('work_interval4', [(n, t) for n in Nboth for t in Tr], cat='Binary')
    total_work_interval = pulp.LpVariable('total_work_interval', cat='Continuous')

    # 各技師の合計夜勤・休日日勤回数
    work_all = pulp.LpVariable.dicts('work_all', [(n) for n in Nboth], cat='Integer')
    # 各技師の合計夜勤・休日日勤回数の平均偏差
    work_all_dev = pulp.LpVariable.dicts('work_all_dev', [(n) for n in Nboth], lowBound=0, cat='Continuous')
    # 各技師の合計夜勤・休日日勤回数の平均偏差の合計
    total_work_all_dev = pulp.LpVariable('total_work_all_dev', cat='Continuous')  

    # 連休変数''
    two_consecutive_holidays = pulp.LpVariable.dicts('two_consecutive_holidays', [(n, t) for n in Nboth for t in Tr[:-1]], cat='Binary')
    three_consecutive_holidays = pulp.LpVariable.dicts('three_consecutive_holidays', [(n, t) for n in Nboth for t in Tr[:-2]], cat='Binary')
    total_two_consecutive_holidays = pulp.LpVariable.dicts('total_two_consecutive_holidays', [(n) for n in Nboth], cat='Integer')
    total_three_consecutive_holidays = pulp.LpVariable.dicts('total_three_consecutive_holidays', [(n) for n in Nboth], cat='Integer')
    consecutive_holidays = pulp.LpVariable('consecutive_holidays', cat='Continuous')

    # 休診日に勤務する回数
    work_on_close = pulp.LpVariable.dicts('work_on_close', [n for n in Nboth], cat='Integer')
    # 休診日に勤務する回数の平均偏差
    work_on_close_dev = pulp.LpVariable.dicts('work_on_close_dev', [n for n in Nboth], lowBound=0, cat='Continuous')
    # 休診日に勤務する回数の平均偏差の合計
    total_work_on_close_dev = pulp.LpVariable('total_work_on_close_dev', cat='Continuous')
      
    # 休日希望が叶わなかった総数
    total_request_dayoff = pulp.LpVariable('total_request_dayoff', lowBound=0, cat='Continuous')


   
    


# ***********************************************************************  
# 目的関数
#   ダミーを少ないく、夜勤間隔を適度に、連休取得をできるだけ、
#   勤務回数を平均化、休診日出勤を平均化、休日希望をできるだけ　叶うように
# ***********************************************************************

    model += dummy \
            + total_work_interval \
                + consecutive_holidays \
                    + total_work_all_dev \
                        + total_work_on_close_dev \
                            + total_request_dayoff
    

# ***********************************************************************
# 制約条件
# ***********************************************************************

# 日にちtにおいて技師nに勤務wを必ず割り当てる・・・(5)
    model += pulp.lpSum([x[n, t, w] for n in N for t in Tr for w in W]) == 1

# ダミー技師の総数をカウント
    model += lam[0] * pulp.lpSum([x[n, t, w] for n in Ndum for t in Tr for w in W1]) == dummy

# 勤務間隔をまとめた変数設定            
    model += lam[1] * pulp.lpSum([work_interval1[n, t] for n in Nboth for t in Tr]) \
            + lam[2] * pulp.lpSum([work_interval2[n, t] for n in Nboth for t in Tr]) \
            + lam[3] * pulp.lpSum([work_interval3[n, t] for n in Nboth for t in Tr]) \
            + lam[4] * pulp.lpSum([work_interval4[n, t] for n in Nboth for t in Tr]) == total_work_interval
    
# 希望振休がどの程度実現できたか？
    # model += lam[9] * (len(F_request_dayoff) - pulp.lpSum([x[n, t, w] for n, t, w in F_request_dayoff])) == total_request_dayoff   # wはすべて'do'となっている

# 連休の取得割合
    # model += lam[6] * pulp.lpSum([default_two_consecutive_holidays - total_two_consecutive_holidays[n] for n in Nboth]) \
    #         + lam[7] * pulp.lpSum([default_three_consecutive_holidays - total_three_consecutive_holidays[n] for n in Nboth]) == consecutive_holidays
    model += -lam[6] * pulp.lpSum([total_two_consecutive_holidays[n] for n in Nboth]) \
            - lam[7] * pulp.lpSum([total_three_consecutive_holidays[n] for n in Nboth]) == consecutive_holidays
    
# 夜勤・休診日日勤の回数の平均偏差の合計
    model += lam[4] * pulp.lpSum([work_all_dev[n] for n in Nboth]) == total_work_all_dev

# 休診日における夜勤・休診日日勤の回数の平均偏差の合計
    model += lam[5] * pulp.lpSum([work_on_close_dev[n] for n in Nboth]) == total_work_on_close_dev



        
    # 日にちtにおける勤務wの必要人数を合わせる
    # W1 0:A日, 1:M日, 2:C日, 3:F日, 4:A夜, 5:M夜, 6:C夜, 7:明, 8:日, 9:他勤, 10:休日, 11:休暇
    # W1 = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho']
    # alpha 0:A日,1:M日,2:C日,3:F日,4:A夜,5:M夜,6:C夜,7:明,8:日勤,9:他勤,10:休日,11:休暇
    # beta
    # gamma
    i = 0
    for t in Tr:
        
        if not t in tokai_calendar.keys():

        # if t in Topened:
        
            # 診療日の日勤を設定人数以上で確保する・・・(6)
            # model += pulp.lpSum([x[n, t, 'dW'] for n in N]) >= alpha[8][i]   #indexをdat.pulpval_list.index('dA')に変更する
            model += pulp.lpSum([x[n, t, 'dW'] for n in N]) >= alpha[W.index('dW')][Tr_dict[t]]   #可読性が高い気がする
            
            # 診療日の休日人数を設定人数以下で確保する・・・(9)
            model += pulp.lpSum([x[n, t, 'do'] for n in N]) <= alpha[W.index('do')][Tr_dict[t]]
            
            # for m in range(len(Gm)-1):
            #     # 正規スタッフ数を設定人数以上で確保・・・(11)
            #     model += pulp.lpSum([x[n, t, 'dW'] for n in Gm[m]]) >= beta[m][i]
            #     # 責任者クラスを設定人数以上で確保・・・(12)
            #     model += pulp.lpSum([x[n, t, 'dW'] for n in Core[m]]) >= gamma[m][i]
            for m in modality_list:

                model += pulp.lpSum([x[n, t, 'dW'] for n in Gm[modality_list.index(m)]]) >= beta[modality_list.index(m)][Tr_dict[t]]
                model += pulp.lpSum([x[n, t, 'dW'] for n in Core[modality_list.index(m)]]) >= gamma[modality_list.index(m)][Tr_dict[t]]
        else:
            # 休診日の日勤は設定人数分を確保する・・・(7)
            # model += pulp.lpSum([x[n, t, 'dW'] for n in N]) == alpha[8][i]
            model += pulp.lpSum([x[n, t, 'dW'] for n in N]) == alpha[W.index('dW')][Tr_dict[t]]
            # 休診日の休日人数を設定人数以上で確保する・・・(10)
            # model += pulp.lpSum([x[n, t, 'do'] for n in N]) >= alpha[10][i]
            model += pulp.lpSum([x[n, t, 'do'] for n in N]) >= alpha[W.index('do')][Tr_dict[t]]


        # 各夜勤・休日勤の人数を確保する
        for w in W[:7]:
            # スタッフ全員に対して人数を確保する・・・(8)
            # model += pulp.lpSum([x[n, t, w] for n in N]) == alpha[W.index(w)][i]
            model += pulp.lpSum([x[n, t, w] for n in N]) == alpha[W.index(w)][Tr_dict[t]]
            # 対応可能なスタッフに各勤務を割り当てる・・・(13)(15)
            model += pulp.lpSum([x[n, t, w] for n in Ns[W.index(w)]]) == alpha[W.index(w)][Tr_dict[t]]
        # 明けの人数を確保する・・・(8)
        # model += pulp.lpSum([x[n, t, 'nn'] for n in N]) == alpha[7][i]
        model += pulp.lpSum([x[n, t, 'nn'] for n in N]) == alpha[W.index('nn')][Tr_dict[t]]
        # 休暇の人数を確保する
        # model += pulp.lpSum([x[n, t, 'ho'] for n in N]) == alpha[11][i]
        model += pulp.lpSum([x[n, t, 'ho'] for n in N]) == alpha[W.index('ho')][Tr_dict[t]]
        # 他勤の人数を確保する
        # model += pulp.lpSum([x[n, t, 'eW'] for n in N]) == alpha[9][i]
        model += pulp.lpSum([x[n, t, 'eW'] for n in N]) == alpha[W.index('eW')][Tr_dict[t]]
        #'emp'は入らない
        model += pulp.lpSum([x[n, t, 'emp'] for n in N]) == 0
        i += 1

    # 夜勤の翌日は明けにする・・・(14)
    for n in N:
        for t in Tr:
            next_day = t + datetime.timedelta(days=1)
            model += pulp.lpSum([x[n, t, w] for w in W[4:7]]) == x[n, next_day, 'nn']

    # 次月1日の勤務
    # 勤務希望をとりあえず叶えるために各勤務の希望人数と必要人数をそろえる
    for w in W1:
        model += pulp.lpSum([x[n, T[-1], w] for n in Nr ]) == next_month_alpha[W1.index(w)]
    # 次月に勤務希望がない場合は空(empty)とする
    model += pulp.lpSum([x[n, T[-1], 'emp']] for n in Nr) >= 0


    # 前月分の勤務を入力
    for n, t, w in F_previous:
        model += x[n, t, w] == 1
    # 勤務希望を叶える・・・(16)
    for n, t, w in F_request:    
        model += x[n, t, w] == 1
    # 次月1日の勤務希望を叶える　-> 実際は次月の勤務作成時に考えるが、当月で夜勤明けにならないようにするため
    for n, t, w in F_request_next_month:
        model += x[n, t, w] == 1
    

    # 禁止事項
    for n in Nr: 
        for t in Tr:
            # 連続勤務日数を13日以内にする・・・(18)
            model += pulp.lpSum([x[n, t-i, w] for i in range(MAXCONSECUTIVEWORKS) for w in W[:10]]) <= MAXCONSECUTIVEWORKS
        
        # 1か月間に休日をμ回取得する・・・(19)
        model += pulp.lpSum([x[n, t, 'do'] for t in Tr]) == myu

        for t in Tr:
            # 3連続夜勤を禁止する
            model += x[n, t-4, 'nn'] + x[n, t-2, 'nn'] + x[n, t, 'nn'] <= 2

            # 対象スタッフの勤務にダミーが入ることを禁止する
            model += x[n, t, 'Ex'] == 0

    # 連休の取得を考慮するのは日勤夜勤対象者のみ→日勤夜勤に入らない人は休診日が休みになるため考慮する必要がない
    for n in Nboth:

        # 1カ月における夜勤・日勤合計回数をε以内にする・・・(17)
        model += pulp.lpSum([x[n, t, w] for t in Tr for w in W[:7]]) == work_all[n]   #各技師の合計夜勤・休日日勤回数
        model += work_all[n] <= epsilon
        # 各技師の合計夜勤・休日日勤回数の平均偏差・・・(32)
        model += mean_works - work_all[n] >= -work_all_dev[n]
        model += mean_works - work_all[n] <= work_all_dev[n]

        # 休診日における勤務の取得回数を平均化する
        model += pulp.lpSum([x[n, t, 'do'] for t in Tclose]) == work_on_close[n]
        # 休診日における勤務回数をできるだけ平均化する
        model += mean_works_on_close - work_on_close[n] >= -work_on_close_dev[n]
        model += mean_works_on_close - work_on_close[n] <= work_on_close_dev[n]


        # 連休の取得は休日と休暇を組み合わせて判定する
        for t in Tr[:-1]:
            # 2連休を数える 下の2式を同時に満たすことができれば対象t日と翌日は休日となり２連休の判定ができる
            model += pulp.lpSum([x[n, t + i, w] for i in range(2) for w in W[10:12]]) -1 <= two_consecutive_holidays[n, t]     #どちらも休日であればtwo_consecutive_holidays=1となる                                      #(22)
            model += pulp.lpSum([x[n, t + i, w] for i in range(2) for w in W[10:12]])  >= 2 * two_consecutive_holidays[n, t]    #どちらも休日であればtwo_consecutive_holidays=1となる　この2式で2連休を判定する                                      #(23)
        # 各スタッフにおける２連休の総和
        model += pulp.lpSum([two_consecutive_holidays[n, t] for t in Tr[:-1]]) == total_two_consecutive_holidays[n]
        
        for t in Tr[:-2]:
            model += pulp.lpSum([x[n, t + i, w] for i in range(3) for w in W[10:12]]) -2 <= three_consecutive_holidays[n, t]                        #(25)
            model += pulp.lpSum([x[n, t + i, w] for i in range(3) for w in W[10:12]]) >= 3 * three_consecutive_holidays[n, t]                       #(26)
        model += pulp.lpSum([three_consecutive_holidays[n, t] for t in Tr[:-2]]) == total_three_consecutive_holidays[n]


        # 夜勤日勤勤務間隔         
        # 休日日勤の翌日に休日日勤や夜勤をできる限り入れない
        for t in Tr:
            # 以下の2式を満たす場合、勤務間隔が1日となる -> 対象日前日に日勤、対象日に日勤および夜勤が入る場合を想定　対象日前日に夜勤は考慮しない。ほかの制約で夜勤のあとに必ず明けが入るため
            model += pulp.lpSum([x[n, t-1, w] for w in W[:4]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) -1 <= work_interval1[n, t]  
            model += pulp.lpSum([x[n, t-1, w] for w in W[:4]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) >= 2 * work_interval1[n, t]
        # 休日日勤・夜勤の2日後に休日日勤や夜勤をできる限り入れない
            model += pulp.lpSum([x[n, t-2, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) -1 <= work_interval2[n, t]
            model += pulp.lpSum([x[n, t-2, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) >= 2 * work_interval2[n, t]
        # 3日後
            model += pulp.lpSum([x[n, t-3, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) -1 <= work_interval3[n, t]
            model += pulp.lpSum([x[n, t-3, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) >= 2 * work_interval3[n, t]
        # 4日後
            model += pulp.lpSum([x[n, t-4, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) -1 <= work_interval4[n, t]
            model += pulp.lpSum([x[n, t-4, w] for w in W[:7]]) + pulp.lpSum([x[n, t, w] for w in W[:7]]) >= 2 * work_interval4[n, t]



# # ***********************************************************************
# # 実行
# # ***********************************************************************

#     print(f'create at {createDate}')
#     print(f'calculatin time : {calctime} s  start....')    

#     cbcpath = config.readSettingJson("CBC_PATH")
#     pulp.LpStatus[model.solve(pulp.COIN_CMD(timeLimit=calctime, path=cbcpath))]
    
#     print(pulp.LpStatus[model.status])
    

# # ***********************************************************************
# # 出力
# # ***********************************************************************
#     # data = convert_scheduling_data(N, staff, G, Tr, Tclosed, T_dict, W, x)
#     data = rd.read_outcome(N, Toutput, T_dict, W, x, createDate)
#     # data = output_scheduling_data(N, Tr, T_dict, W, x)
#     # xl.output_data(N, staff, G, Tr, Tclosed, T_dict, W, x)
#     try:
#         dataDir = config.readSettingJson("DATA_DIR")
#         outputPath = os.path.join(dataDir,'shift.dat')
#         with open(outputPath, 'w', encoding='utf-8') as f:
#             writer = csv.writer(f, lineterminator='\n')
#             writer.writerow(['#' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ',' + pulp.LpStatus[model.status]])
#             writer.writerows(data)
#     except FileNotFoundError as e:
#         print(e)
#     except csv.Error as e:
#         print(e)
#     return pulp.LpStatus[model.status], data

def convertConfig(data):

    createDate = datetime.datetime.strptime(data[0][0], '%Y/%m/%d')
    epsilon = data[1][0]
    iota = data[2][0]
    kappa = data[3][0]
    myu = data[4][0]
    nyu = []
    nyu.append(data[5][0]); nyu.append(data[6][0]); nyu.append(data[7][0])
    rho = data[8][0]
    lam = []
    lam.append(data[9][0]); lam.append(data[10][0]); lam.append(data[11][0]); lam.append(data[12][0]); lam.append(data[13][0]) 
    
    return createDate, epsilon, iota, kappa, myu, nyu, rho, lam


def output_scheduling_data(N, Tr, T_dict, W, x):
    # W1 = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho']
    # W2 = ['Ex']
    invW = {'dA':'A日','dM':'M日','dC':'C日','dF':'F日','nA':'A夜','nM':'M夜','nC':'C夜','nn':'明','dW':'','eW':'他','do':'休','ho':'特','Ex':'ダ'}
    invDept = ['MR', 'TV', 'HT', 'NM', 'XA', 'RT', 'XP', 'CT', 'XO', 'FR/NF']
    buf = []

    for n in N:
        for t in Tr:
            shift = []
            for w in W:
                if x[n, t, w].value():
                    shift.append(n)
                    shift.append(T_dict[t])
                    shift.append(invW[w])
                    buf.append(shift)
    return buf                

def convert_scheduling_data(N, staff, G, Tr, Tclosed, T_dict, W, x):
    # W1 = ['dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC', 'nn', 'dW', 'eW', 'do', 'ho']
    # W2 = ['Ex']
    invW = {'dA':'A日','dM':'M日','dC':'C日','dF':'F日','nA':'A夜','nM':'M夜','nC':'C夜','nn':'明','dW':'','eW':'他','do':'休','ho':'特','Ex':'ダ'}
    invDept = ['MR', 'TV', 'HT', 'NM', 'XA', 'RT', 'XP', 'CT', 'XO', 'FR/NF']

    buf = []
    for n in N:
        staff_info = []
        if staff.get(n):
            staff_info.append(n)
            staff_info.append(staff[n]['id'])
            staff_info.append(staff[n]['name'])
            for m in G:
                if n in m:
                    staff_info.append(invDept[G.index(m)])
                    break
        else:
            staff_info.append(n)
            staff_info.append('')
            staff_info.append('')
            staff_info.append('')

        for t in Tr:
            shift = []
            for w in W:
                if x[n, t, w].value():
                    for i in staff_info:
                        shift.append(i)
                    shift.append(T_dict[t])
                    shift.append(invW[w])
                    buf.append(shift)
    return buf
        

