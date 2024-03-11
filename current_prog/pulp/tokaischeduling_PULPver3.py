import os
import csv
import pulp
import datetime
import readdata as rd
import tokaifunc as tfunc
import config
import time
import datdata 

class PulpScheduling:

    def __init__(self) -> None:
        
        pass

def calc_schedule():
    MAXCONSECUTIVEWORKS = 12        #法律上可能な連続勤務日数
    dat = datdata.DatData()

    # 変数
    modality_list = dat.modality_list
    invW = dat.pulp2work_dict

    N = dat.N; 
    Nr = dat.Nr 

    Nboth = dat.Nboth
    Ns = dat.Ns
    Ndum = dat._Ndum

    Gm = dat.Gm
    Core = dat.Core

    T = dat.T
    Tr_dict = dat.Tr_dict
    Tr = dat.Tr
    Tclose = dat.Tclose


    W1 = dat.W1_list
    W2 = dat.W2_list
    W3 = dat.W3_list
    W = W1 + W2 + W3

    alpha = dat.alpha
    beta = dat.beta
    gamma = dat.gamma
    next_month_alpha = dat.calc_next_month_alpha()

    F_previous = dat.F_previous
    F_request = dat.F_request
    F_request_dayoff = dat.F_request_dayoff
    F_request_next_month = dat.F_request_next_month
    
    configvar = dat.configvar
    # createDate = 作成日
    create_date = configvar['date']
    # epsilon = 夜勤日勤回数の上限
    night_and_dailiy_work_limit = configvar['epsilon']

    # iota = 連続勤務日数上限
    consecutive_work_limit = configvar['iota']
    # myu = 休日数
    number_of_dayoff = configvar['myu']
    # nyu = 達成した連休数
    desired_holidays = configvar['nyu']
    
    calc_time = configvar['calctime']
    desired_two_consecutive_holidays = desired_holidays[0] + desired_holidays[1]*2 + desired_holidays[2]*3
    # default_two_consecutive_holidays = nyu[0] + nyu[1]*2 + nyu[2]*3
    desired_three_consecutive_holidays = desired_holidays[1] + desired_holidays[2]*1
    desired_four_consecutive_holidays = desired_holidays[2]

    
    # 夜勤・休日日勤平均回数
    mean_works =dat.calc_mean_works()
    # mean_works = tfunc.calc_mean_of_night_and_daily(alpha, len(Ndaily), len(Nnight))
    # 休診日かかる夜勤・日勤平均回数=休診日 * 休診日に必要な人数 / 夜勤・日勤対応スタッフ数
    mean_works_on_close = dat.calc_mean_works_on_close()
    # mean_works_on_close = len(Tclosed) * REQUIRED_NUM_OF_COLOSED_DAY / len(Nboth)
    # Tdict, T, Tr, Tclosed, Topened, Toutput = tfunc.make_T(createDate, iota)
 
    coef = {'dummy': 1.0, \
            'work_interval1': 0.4, \
            'work_interval2': 0.3, \
            'work_interval3': 0.2, \
            'work_interval4': 0.1, \
            'work_all': 0.1, \
            'work_on_close': 0.1, \
            'two_consecutive_holidays': 0.1, \
            'three_consecutive_holidays': 0.05, \
            'request_dayoff': 0.2}


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
      
    # 休日希望が叶わなった総数
    total_request_dayoff = pulp.LpVariable('total_request_dayoff', cat='Continuous')


   
    


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
    for n in N:
        for t in Tr:
            model += pulp.lpSum([x[n, t, w] for w in W]) == 1

# ダミー技師の総数をカウント
    model += coef['dummy'] * pulp.lpSum([x[n, t, w] for n in Ndum for t in Tr for w in W1]) == dummy

# 勤務間隔をまとめた変数設定            
    model += coef['work_interval1'] * pulp.lpSum([work_interval1[n, t] for n in Nboth for t in Tr[:-1]]) \
            + coef['work_interval2']  * pulp.lpSum([work_interval2[n, t] for n in Nboth for t in Tr[:-1]]) \
            + coef['work_interval3']  * pulp.lpSum([work_interval3[n, t] for n in Nboth for t in Tr[:-1]]) \
            + coef['work_interval4']  * pulp.lpSum([work_interval4[n, t] for n in Nboth for t in Tr[:-1]]) == total_work_interval
    
# 連休の取得割合
    # model += lam[6] * pulp.lpSum([default_two_consecutive_holidays - total_two_consecutive_holidays[n] for n in Nboth]) \
    #         + lam[7] * pulp.lpSum([default_three_consecutive_holidays - total_three_consecutive_holidays[n] for n in Nboth]) == consecutive_holidays
    model += -coef['two_consecutive_holidays']  * pulp.lpSum([desired_two_consecutive_holidays - total_two_consecutive_holidays[n] for n in Nboth]) \
            - coef['three_consecutive_holidays']  * pulp.lpSum([desired_three_consecutive_holidays - total_three_consecutive_holidays[n] for n in Nboth]) == consecutive_holidays
    
# 夜勤・休診日日勤の回数の平均偏差の合計
    model += coef['work_all'] * pulp.lpSum([work_all_dev[n] for n in Nboth]) == total_work_all_dev

# 休診日における夜勤・休診日日勤の回数の平均偏差の合計
    model += coef['work_on_close'] * pulp.lpSum([work_on_close_dev[n] for n in Nboth]) == total_work_on_close_dev
# 希望振休がどの程度実現できたか？
    model += -coef['request_dayoff'] * pulp.lpSum([x[n, t, w] for n, t, w in F_request_dayoff]) == total_request_dayoff   # wはすべて'do'となっている

    
        
    # 日にちtにおける勤務wの必要人数を合わせる
    for t in Tr[:-1]:
        # alpha
        # 各勤務に必要な人数を確保する
        for w in W[:7]:
            # スタッフ全員に対して各勤務の人数を確保し、かつ　対応可能なスタッフを割り当てる
            # スタッフ全員に対して人数を確保する・・・(8)
            model += pulp.lpSum([x[n, t, w] for n in N]) == alpha[W.index(w)][Tr_dict[t]]
            # 対応可能なスタッフに各勤務「'dA', 'dM', 'dC', 'dF', 'nA', 'nM', 'nC'」を割り当てる・・・(13)(15)
            model += pulp.lpSum([x[n, t, w] for n in Ns[W.index(w)]]) == alpha[W.index(w)][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'dA'] for n in Ns[W.index('dA')]]) == alpha[W.index('dA')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'dM'] for n in Ns[W.index('dM')]]) == alpha[W.index('dM')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'dC'] for n in Ns[W.index('dC')]]) == alpha[W.index('dC')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'dF'] for n in Ns[W.index('dF')]]) == alpha[W.index('dF')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'nA'] for n in Ns[W.index('nA')]]) == alpha[W.index('nA')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'nM'] for n in Ns[W.index('nM')]]) == alpha[W.index('nM')][Tr_dict[t]]
        # model += pulp.lpSum([x[n, t, 'nC'] for n in Ns[W.index('nC')]]) == alpha[W.index('nC')][Tr_dict[t]]
        model += pulp.lpSum([x[n, t, 'nn'] for n in N]) == alpha[W.index('nn')][Tr_dict[t]]
        model += pulp.lpSum([x[n, t, 'ho'] for n in N]) == alpha[W.index('ho')][Tr_dict[t]]
        model += pulp.lpSum([x[n, t, 'eW'] for n in N]) == alpha[W.index('eW')][Tr_dict[t]]
        #'emp'は入らない
        model += pulp.lpSum([x[n, t, 'emp'] for n in N]) == 0
        # 'Ex'ダミー勤務は選択されない
        model += pulp.lpSum([x[n, t, 'Ex'] for n in Nr]) == 0


        if t in Tclose:
            # 休診日の日勤は設定人数分を確保する・・・(7)
            model += pulp.lpSum([x[n, t, 'dW'] for n in N]) == alpha[W.index('dW')][Tr_dict[t]]
            # model += pulp.lpSum([x[n, t, 'do'] for n in N]) >= alpha[W.index('do')][Tr_dict[t]]
            model += pulp.lpSum([x[n, t, 'do'] for n in N]) >= 0
        else:

            # 診療日の日勤を設定人数以上で確保する・・・(6)
            # model += pulp.lpSum([x[n, t, 'dW'] for n in N]) >= alpha[W.index('dW')][Tr_dict[t]]   #可読性が高い気がする
            model += pulp.lpSum([x[n, t, 'dW'] for n in N]) >= 0
            model += pulp.lpSum([x[n, t, 'do'] for n in N]) <= alpha[W.index('do')][Tr_dict[t]]
            
        # beta gamma    
        # モダリティスタッフ、およびコアメンバーの人数を確保する
        for m in modality_list:
            model += pulp.lpSum([x[n, t, 'dW'] for n in Gm[modality_list.index(m)]]) >= beta[modality_list.index(m)][Tr_dict[t]]
            model += pulp.lpSum([x[n, t, 'dW'] for n in Core[modality_list.index(m)]]) >= gamma[modality_list.index(m)][Tr_dict[t]]

    # 夜勤の翌日は明けにする・・・(14)
    for n in N:
        for t in Tr[:-1]:
            next_day = t + datetime.timedelta(days=1)
            model += pulp.lpSum([x[n, t, w] for w in W[4:7]]) == x[n, next_day, 'nn']


    # 次月1日の勤務 -> 夜勤や日勤は次月のため、習熟度の満たしていないスタッフでも入力可能なので、NsでなくNとして計算
    for w in W1:
        model += pulp.lpSum([x[n, T[-1], w] for n in N ]) == next_month_alpha[W1.index(w)]
    # model += pulp.lpSum([x[n, Tr[-1], 'dA'] for n in N]) == next_month_alpha[W1.index('dA')]
    # model += pulp.lpSum([x[n, Tr[-1], 'dM'] for n in N]) == next_month_alpha[W1.index('dM')]
    # model += pulp.lpSum([x[n, Tr[-1], 'dC'] for n in N]) == next_month_alpha[W1.index('dC')]
    # model += pulp.lpSum([x[n, Tr[-1], 'dF'] for n in N]) == next_month_alpha[W1.index('dF')]
    # model += pulp.lpSum([x[n, Tr[-1], 'nA'] for n in N]) == next_month_alpha[W1.index('nA')]
    # model += pulp.lpSum([x[n, Tr[-1], 'nM'] for n in N]) == next_month_alpha[W1.index('nM')]
    # model += pulp.lpSum([x[n, Tr[-1], 'nC'] for n in N]) == next_month_alpha[W1.index('nC')]
    # model += pulp.lpSum([x[n, Tr[-1], 'nn'] for n in N]) == next_month_alpha[W1.index('nn')]
    # model += pulp.lpSum([x[n, Tr[-1], 'dW'] for n in N]) == next_month_alpha[W1.index('dW')]
    # model += pulp.lpSum([x[n, Tr[-1], 'eW'] for n in N]) == next_month_alpha[W1.index('eW')]
    # model += pulp.lpSum([x[n, Tr[-1], 'do'] for n in N]) == next_month_alpha[W1.index('do')]
    # model += pulp.lpSum([x[n, Tr[-1], 'ho'] for n in N]) == next_month_alpha[W1.index('ho')]
    # 次月に勤務希望がない場合は空(empty)とする
    model += pulp.lpSum([x[n, Tr[-1], 'emp']] for n in Nr) >= 0
    model += pulp.lpSum([x[n, Tr[-1], 'Ex'] for n in Nr]) == 0


    # # 前月分の勤務を入力
    for n, t, w in F_previous:
        model += x[n, t, w] == 1
    # # 勤務希望を叶える・・・(16)
    for n, t, w in F_request:    
        model += x[n, t, w] == 1
    # # 次月1日の勤務希望を叶える　-> 実際は次月の勤務作成時に考えるが、当月で夜勤明けにならないようにするため
    for n, t, w in F_request_next_month:
        model += x[n, t, w] == 1
    # 振休を希望がかなわなかった場合は、勤務とする
    for n, t, w in F_request_dayoff:
        model += x[n, t, w] + x[n, t, 'dW'] + x[n, t, 'nn'] == 1

    # 禁止事項
    for n in Nr: 
        # 連続勤務日数を13日以内にする・・・(18)
        for t in Tr[:-1]:
            j = Tr_dict[t]
            model += pulp.lpSum([x[n, Tr[j-l], w] for l in range(MAXCONSECUTIVEWORKS) for w in W[:10]]) <= MAXCONSECUTIVEWORKS
       
        # 1か月間に休日をμ回取得する・・・(19)
        model += pulp.lpSum([x[n, t, 'do'] for t in Tr[:-1]]) == number_of_dayoff
        # 3連続夜勤を禁止する
        for t in Tr:
            j = Tr_dict[t]
            model += x[n, Tr[j-4], 'nn'] + x[n, Tr[j-2], 'nn'] + x[n, Tr[j], 'nn'] <= 2



    # 連休の取得を考慮するのは日勤夜勤対象者のみ→日勤夜勤に入らない人は休診日が休みになるため考慮する必要がない
    for n in Nboth:
        # 1カ月における夜勤・日勤合計回数の上限以下として平均化する・・・(17)
        # model += pulp.lpSum([x[n, t, w] for t in Tr for w in W[:7]]) <= night_and_dailiy_work_limit
        model += pulp.lpSum([x[n, t, w] for t in Tr[:-1] for w in W[:7]]) == work_all[n]   #各技師の合計夜勤・休日日勤回数
        model += work_all[n] <= night_and_dailiy_work_limit
        # 各技師の合計夜勤・休日日勤回数の平均偏差・・・(32)
        model += mean_works - work_all[n] >= -work_all_dev[n]
        model += mean_works - work_all[n] <= work_all_dev[n]

        # 休診日における勤務の取得回数を平均化する
        model += pulp.lpSum([x[n, t, 'do'] for t in Tclose]) == work_on_close[n]
        # 休診日における勤務回数をできるだけ平均化する
        model += mean_works_on_close - work_on_close[n] >= -work_on_close_dev[n]
        model += mean_works_on_close - work_on_close[n] <= work_on_close_dev[n]


        # 各連休の取得割合を求める　連休->休日あるいは休暇のどちらでも構わない
        for t in Tr[:-2]:
            j = Tr_dict[t]
            # 2連休を数える 下の2式を同時に満たすことができれば対象t日と翌日は休日となり２連休の判定ができる
            model += pulp.lpSum([x[n, Tr[j+l], w] for l in range(2) for w in W[10:12]]) -1 <= two_consecutive_holidays[n, t]     #どちらも休日であればtwo_consecutive_holidays=1となる                                      #(22)
            model += pulp.lpSum([x[n, Tr[j+l], w] for l in range(2) for w in W[10:12]])  >= 2 * two_consecutive_holidays[n, t]    #どちらも休日であればtwo_consecutive_holidays=1となる　この2式で2連休を判定する                                      #(23)
        # 各スタッフにおける２連休の総和
        model += pulp.lpSum([two_consecutive_holidays[n, t] for t in Tr[:-2]]) == total_two_consecutive_holidays[n]
        
        for t in Tr[:-3]:
            j = Tr_dict[t]
            model += pulp.lpSum([x[n, Tr[j+l], w] for l in range(3) for w in W[10:12]]) -2 <= three_consecutive_holidays[n, t]                        #(25)
            model += pulp.lpSum([x[n, Tr[j+l], w] for l in range(3) for w in W[10:12]]) >= 3 * three_consecutive_holidays[n, t]                       #(26)
        model += pulp.lpSum([three_consecutive_holidays[n, t] for t in Tr[:-3]]) == total_three_consecutive_holidays[n]


        # 夜勤日勤勤務間隔         
        # 休日日勤の翌日に休日日勤や夜勤をできる限り入れない
        for t in Tr[:-1]:
            j = Tr_dict[t]
            # 以下の2式を満たす場合、勤務間隔が1日となる -> 対象日前日に日勤、対象日に日勤および夜勤が入る場合を想定　対象日前日に夜勤は考慮しない。ほかの制約で夜勤のあとに必ず明けが入るため
            model += pulp.lpSum([x[n, Tr[j-1], w] for w in W[:4]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) -1 <= work_interval1[n, t]  
            model += pulp.lpSum([x[n, Tr[j-1], w] for w in W[:4]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) >= 2 * work_interval1[n, t]
        # 休日日勤・夜勤の2日後に休日日勤や夜勤をできる限り入れない
            model += pulp.lpSum([x[n, Tr[j-2], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) -1 <= work_interval2[n, t]
            model += pulp.lpSum([x[n, Tr[j-2], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) >= 2 * work_interval2[n, t]
        # 3日後
            model += pulp.lpSum([x[n, Tr[j-3], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) -1 <= work_interval3[n, t]
            model += pulp.lpSum([x[n, Tr[j-3], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) >= 2 * work_interval3[n, t]
        # 4日後
            model += pulp.lpSum([x[n, Tr[j-4], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) -1 <= work_interval4[n, t]
            model += pulp.lpSum([x[n, Tr[j-4], w] for w in W[:7]]) + pulp.lpSum([x[n, Tr[j], w] for w in W[:7]]) >= 2 * work_interval4[n, t]



# ***********************************************************************
# 実行
# ***********************************************************************
    print(f'create at {create_date}')
    print(f'calculatin time : {calc_time} s  start....')    

    cbcpath = config.readSettingJson("CBC_PATH")
    pulp.LpStatus[model.solve(pulp.COIN_CMD(timeLimit=calc_time, path=cbcpath))]
    
    print(pulp.LpStatus[model.status])

# ***********************************************************************
# 出力
# ***********************************************************************
    # 変数をxを出力
    x_list = dat.convert_outcome2list(x, N, Tr, W, invW)

    x_list = dat.rewrite_request(x_list, dat.request)

    x_list = dat.rewrite_request(x_list, dat.request_next_month)

    dat.output_xlist2shiftdat(x_list, pulp.LpStatus[model.status])

    score = 0
    for n, t, w in F_request_dayoff:
        score += x[n, t, w].varValue
    print(score)
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

# 得られた結果に対して、次月1日の編集とその結果をリストに変更する
def convert_outcome2list(x, N, Tr, W, invW):

    x_list = []
    for n in N:
        for t in Tr:
            for w in W:
                if x[n, t, w] == 1:
                    shift = []
                    shift.append(n)
                    shift.append(t)
                    shift.append(invW[x])
                    x_list.append(shift)

    return x_list

def next_month_handle(src, request_nextmonth):

    for n, t, w in request_nextmonth:
        for i in range(len(src)):
            if src[i][0] == n and src[i][1] == t:
                src[i][2] = w




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
        

