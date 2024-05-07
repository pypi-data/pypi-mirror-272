# -*- coding: utf-8 -*-
# @File  : 通用代码.py
# @Time  : 2023/6/9 13:12
# @Author: 唐旭东

import sys,re,numpy,json,pymysql
from loguru import logger
from typing import Union
from .read_data import ReadData
from .pytmysql import PyMySQL
from .str_category import is_num
from .list_processing import list_dupl

#老高考批次
batch_dict1 = {'本科一批A': '本科一批', '专科': '专科', '本科一批A1': '本科一批', '本科一批B': '本科一批',
                 '本科二批A': '本科二批', '本科二批B': '本科二批', '本科二批C': '本科二批', '高本贯通批': '专科',
                 '本科提前A': '本科一批', '本科提前批A': '本科一批', '本科提前批B': '本科一批', '本科提前B': '本科一批',
                 '本科一批': '本科一批', '蒙授本科一批': '本科一批', '本科二批': '本科二批', '蒙授本科二批': '本科二批',
                 '专科提前': '专科', '专科提前批': '专科', '蒙授本科提前A': '本科一批', '蒙授本科提前批A': '本科一批',
                 '蒙授专科': '专科', '蒙授本科提前B': '本科一批', '蒙授本科提前批B': '本科一批', '蒙授专科提前': '专科',
                 '蒙授专科提前批': '专科', '国家专项': '本科一批', '本科提前批': '本科一批', '提前批': '本科一批',
                 '地方专项': '本科一批', '提前批公安专科': '专科', '公安专科院校': '专科', '提前本科二批': '本科二批',
                 '提前本科一批': '本科一批', '专项计划批': '本科一批', '本科提前批其他类': '本科一批',
                 '本科一批预科': '本科一批', '本科二批预科B类': '本科二批', '本科二批预科A类': '本科二批',
                 '专科提前批定向类': '专科', '专科提前批其他类': '专科', '本科提前批空军招飞批': '本科一批',
                 '本科二批预科B': '本科二批', '专项计划': '本科一批', '本科二批预科A': '本科二批',
                 '本科一批高校专项': '本科一批', '本科二批预科': '本科二批', '本科提前批预科': '本科一批',
                 '本科提前批高校专项': '本科一批', '一类模式本科二批预科': '本科二批', '一类模式专科预科': '专科',
                 '专科预科': '专科', '一类模式本科一批预科': '本科一批', '帮扶专项': '本科一批',
                 '提前本科批': '本科一批', '一本预科': '本科一批', '二本及预科': '本科二批', '提前专项批': '本科二批',
                 '提前专科批': '专科', '专项提前批': '本科二批', '高职专项': '专科',
                 '本科提前批B段(国家专项)': '本科一批', '本科提前批少数民族紧缺人才专项（G段）': '本科一批',
                 '本科提前批地方专项（D段）': '本科一批', '本科提前批省属院校贫困地区国家专项（C段）': '本科一批',
                 '本科提前批精准扶贫专项（E段）': '本科一批', '本科提前批革命老区专项（F段）': '本科一批',
                 '提前批一本': '本科二批', '提前批二本': '本科二批', '提前二批专科': '本科二批',
                 '本科一批(普通类)': '本科一批', '本科二批(普通类)': '本科二批', '专科批(普通类)': '专科批(普通类)',
                 '本科一批(单列类-选考外语)': '本科一批', '本科二批(单列类-选考外语)': '本科二批',
                 '本科一批(单列类-选考民族语文)': '本科一批', '本科二批(单列类-选考民族语文)': '本科二批',
                 '专科批(单列类-选考外语)': '专科', '专科批(单列类-选考民族语文)': '专科',
                 '【内高】18级单列本科二批（四年）': '本科二批', '【内高】19级单列本科二批': '本科二批',
                 '本科二批单列': '本科二批', '【内高】18级单列本科一批': '本科一批',
                 '【内高】18级单列本科一批（四年）': '本科一批', '【内高】18级普通本科一批': '本科一批',
                 '【内高】19级单列本科一批': '本科一批', '【内高】19级普通本科一批': '本科一批', '本科一批单列': '本科一批',
                 '【内高】18级单列专科': '专科', '【内高】18级单列专科（四年）': '专科', '【内高】18级普通专科': '专科',
                 '【内高】19级单列专科': '专科', '【内高】19级普通专科': '专科', '专科单列': '专科',
                 '【内高】18级单列本科二批': '本科二批', '【内高】18级普通本科二批': '本科二批',
                 '【内高】19级普通本科二批': '本科二批', '【内高】18级单列本科提前批': '本科一批',
                 '【内高】18级普通本科提前批': '本科一批', '【内高】19级单列本科提前批': '本科一批',
                 '【内高】19级普通本科提前批': '本科一批', '【内高】18级单列本科提前批（四年）': '本科一批'}

#新高考批次
batch_dict2 = {'bk': '本科', 'zk': '专科', '本科': '本科', '专科': '专科', '本科提前批A': '特殊类型招生控制线', '本科提前批B': '特殊类型招生控制线', '本科提前B': '特殊类型招生控制线',
                 '专科提前': '专科', '专科提前批': '专科', '蒙授本科提前A': '特殊类型招生控制线', '蒙授本科提前批A': '特殊类型招生控制线',
                 '蒙授专科': '专科', '蒙授本科提前B': '特殊类型招生控制线', '蒙授本科提前批B': '特殊类型招生控制线', '蒙授专科提前': '专科',
                 '蒙授专科提前批': '专科', '国家专项': '特殊类型招生控制线', '本科提前批': '特殊类型招生控制线', '提前批': '特殊类型招生控制线',
                 '地方专项': '特殊类型招生控制线', '提前批公安专科': '专科', '公安专科院校': '专科','专项计划批': '特殊类型招生控制线', '本科提前批其他类': '特殊类型招生控制线',
                 '专科提前批定向类': '专科', '专科提前批其他类': '专科', '本科提前批空军招飞批': '特殊类型招生控制线', '专项计划': '特殊类型招生控制线','本科提前批预科': '特殊类型招生控制线',
                 '本科提前批高校专项': '特殊类型招生控制线', '一类模式专科预科': '专科','专科预科': '专科', '帮扶专项': '特殊类型招生控制线',
                 '提前本科批': '特殊类型招生控制线', '提前专科批': '专科', '高职专项': '专科','本科提前批B段(国家专项)': '特殊类型招生控制线', '本科提前批少数民族紧缺人才专项（G段）': '特殊类型招生控制线',
                 '本科提前批地方专项（D段）': '特殊类型招生控制线', '本科提前批省属院校贫困地区国家专项（C段）': '特殊类型招生控制线',
                 '本科提前批精准扶贫专项（E段）': '特殊类型招生控制线', '本科提前批革命老区专项（F段）': '特殊类型招生控制线'}

#返回省市区名称和地区编号
def prurar_code(gkle='all',ssq=None):
    gkle=gkle.strip('省份')
    prurar_code={"北京": 11, "天津": 12, "河北": 13, "山西": 14, "内蒙古": 15, "辽宁": 21, "吉林": 22, "黑龙江": 23,
           "上海": 31, "江苏": 32, "浙江": 33, "安徽": 34, "福建": 35, "江西": 36, "山东": 37, "河南": 41, "湖北": 42,
           "湖南": 43, "广东": 44, "广西": 45, "海南": 46, "重庆": 50, "四川": 51, "贵州": 52, "云南": 53,
           "陕西": 61, "甘肃": 62, "青海": 63, "宁夏": 64, "新疆": 65}
    prurar_dict={x[0]: x[1] for x in ReadData('各省份高考分类').data[1:]}
    if ssq:
        return prurar_code[ssq]
    if gkle in ('专业类','专业组','新高考','老高考','综合'):
        return json.loads(prurar_dict.get(gkle))
    return prurar_code

#转换批次名称
def convert_pc(pc,prurar=None):
    if prurar:
        new_pc = batch_dict1.get(pc) if prurar in prurar_code('老高考省份') else batch_dict2.get(pc)
        if new_pc:
            return new_pc
    if '本科' in pc and '提前' in pc:
        return '本科提前批'
    elif '专科' in pc and '提前' in pc:
        return '专科提前批'
    elif '本科' in pc or 'bk' in pc or '一段' in pc:
        return '本科'
    elif '专科' in pc or 'zk' in pc or '二段' in pc:
        return '专科'
    else:
        return '特殊类'

#转换科类名称
def convert_kl(kl):
    if '不限' in kl:
        return '综合'
    if 'li' in kl or '物理' in kl or '理' in kl:
        return '理工'
    if 'wen' in kl or '历史' in kl or '文' in kl:
        return '文史'
    if 'all' in kl or '综合' in kl:
        return '综合'
    return kl

#删除了数据中判断为Flase(判断0的返回值为Flase)的数据
def delete_flase_empty(ls):
    nls=[]
    for l in ls:
        type_l=type(l)
        if type_l!=int and type_l!=float and l:
            logger.error(f"数据集中存在非数字类型数据！\n{ls}")
            sys.exit()
        if l and not numpy.isnan(l):
            nls.append(l)
    return nls

#求平均数默认保留小数
def txdavg(ls,zero_in=False,dp=2,valid=True):
    """
    :param zero_in 0是否参与计算，默认不参与
    :param dp 默认保留2位小数
    :param valid 默认保留有效小数位
    """
    ls_0=[]
    if zero_in:
        ls_0 = [l for l in ls if l==0]
    ls = delete_flase_empty(ls)+ls_0
    if ls:
        if valid:
            return prvadepl(round(sum(ls)/len(ls), dp))
        return round(sum(ls) / len(ls), dp)
    else:
        return None

#求百分比平均数默认保留百分比中两位小数
def txdpercavg(ls,dp=2):
    nls=[]
    for l in ls:
        if l is None:
            continue
        if type(l)==str:
            if re.search('^([0-9.]+%)$',l):
                nls.append(float(l[:-1])/100)
            else:
                logger.error(f'计算平均百分比时，发现存在非百分比数据\n{ls}')
                sys.exit()
    ls = delete_flase_empty(nls)
    if ls:
        return txdperc(sum(ls)/len(ls), dp)
    else:
        return None

#求最小数
def txdmin(ls):
    ls = delete_flase_empty(ls)
    if ls:
        return min(ls)
    else:
        return None

#将数字转换为百分比，默认百分比中数字保留两位小数
def txdperc(num,dp=2):
    return f'{round(num * 100, dp)}%' if is_num(num) else None

class QueryScoreRank:
    """
    查询分数位次，省份批次线
    """
    def __init__(self,year,simplify_pcname=True):
        """
        :param year:年份
        :param mysql:mysql连接对象
        :param simplify_pcname:将批次转换为只有本专科
        """
        self.year=year
        self.simplify_pcname=simplify_pcname
        self.batch_xian_dict={}
        self.frac_rank_dict={'北京':{},'天津':{},'上海':{},'江苏':{},'山西':{},'广东':{},'江西':{},'other':{}}
        self.get_batch_xian()#获取当前年份所有省份所有科类批次线生成字典数据
        self.get_frac_rank()#获取当前年份所有省份所有科类所有批次分数排名生成字典数据

    def get_batch_xian(self):
        """
        获取当前年份所有省份所有科类批次线生成字典数据
        """
        batch_dict = {'本科批': '本科', '本科一批(普通类)': '本科一批', '本科二批(普通类)': '本科二批','专科批(普通类)': '专科', }
        batch_xians = ReadData('批次线表', ['region_name', 'kelei_name', 'batch', 'batch_fen'],select_sql=f"`year` = '{self.year}'", replace_th=False).data[1:]
        if self.simplify_pcname:
            # 将批次转换为只有本专科
            for batch_xian in batch_xians:
                pc = batch_dict.get(batch_xian[2], batch_xian[2])
                pc = '专科' if '专科' in convert_pc(pc) else '本科'
                pc = "专科" if ("专科" in pc or "二段" in pc) else "本科"
                key = f'{batch_xian[0]}_{pc}_{convert_kl(batch_xian[1])}'
                if key in self.batch_xian_dict:
                    if self.batch_xian_dict[key] - batch_xian[-1] > 0:
                        self.batch_xian_dict[key] = batch_xian[-1]
                else:
                    self.batch_xian_dict[key] = batch_xian[-1]
        else:
            for batchds in batch_xians:
                pc = batch_dict.get(batchds[2], batchds[2])
                self.batch_xian_dict[f"{batchds[0]}_{batchds[2]}_{batchds[1]}"] = int(batchds[-1])
                self.batch_xian_dict[f"{batchds[0]}_{batchds[2]}_{batchds[1]}"] = int(batchds[-1])

    def get_frac_rank(self):
        """
        获取当前年份所有省份所有科类所有批次分数排名生成字典数据
        """
        frac_ranks = ReadData('一分一段表', ['region_name','kelei_name','tag','gaokaofen','paim'],select_sql=f"`year` = '{self.year}'",replace_th=False).data[1:]
        for frac_rank in frac_ranks:
            region_name=frac_rank[0]
            if region_name in ['北京','天津','山西','上海','江苏','江西','广东']:
                # print(region_name)
                if region_name in ['江苏','山西']:
                    key = f'{region_name}_{convert_kl(frac_rank[1])}_{"本科" if "一" in frac_rank[2] else "专科"}'
                else:
                    key = f'{region_name}_{convert_kl(frac_rank[1])}_{"专科" if "专科" in frac_rank[2] else "本科"}'
                if key in self.frac_rank_dict[region_name]:
                    self.frac_rank_dict[region_name][key][0].append(frac_rank[-2])
                    self.frac_rank_dict[region_name][key][1].append(frac_rank[-1])
                else:
                    self.frac_rank_dict[region_name].update({key: [[frac_rank[-2]], [frac_rank[-1]]]})
            else:
                key=f'{frac_rank[0]}_{convert_kl(frac_rank[1])}'
                if key in self.frac_rank_dict['other']:
                    self.frac_rank_dict['other'][key][0].append(frac_rank[-2])
                    self.frac_rank_dict['other'][key][1].append(frac_rank[-1])
                else:
                    self.frac_rank_dict['other'].update({key:[[frac_rank[-2]],[frac_rank[-1]]]})

    #返回分数位次和位次百分比
    def rfrac_rank(self,prurar,pc,kl,frac,isrrp=False):
        """
        :param prurar:省市区名称
        :param pc:批次
        :param kl:科类
        :param frac:要查询位次的分数
        :param isrrp:是否返回位次百分比
        :return 分数位次，（批次线，批次线位次，分数位次百分比）
        """
        kl = convert_kl(kl)
        if not frac:
            if isrrp:
                return None,(None,None,None)
            return None

        frac_rank=self.rfrac_rank1(prurar, pc, kl, frac)
        if isrrp:
            batch_xian,batch_xian_rank=self.rbx_rank(prurar,pc,kl)
            return frac_rank, (batch_xian,batch_xian_rank,txdperc(frac_rank/batch_xian_rank) if batch_xian_rank and frac_rank else None)
        return frac_rank

    #返回批次线和批次线位次
    def rbx_rank(self,prurar,pc,kl,rbxr=True):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param rbxr:是否返回位次
        :return:返回批次线和批次线位次
        """
        kl = convert_kl(kl)
        if f'{prurar}_{pc}_{kl}' in self.batch_xian_dict:
            key = f'{prurar}_{pc}_{kl}'
        elif f'{prurar}_{"专科" if ("专科" in pc or "二段" in pc) else "本科"}_{kl}' in self.batch_xian_dict:
            key = f'{prurar}_{"专科" if ("专科" in pc or "二段" in pc) else "本科"}_{kl}'
        else:
            key = None

        if key:
            batch_xian = self.batch_xian_dict[key]
            if rbxr:
                batch_xian_rank = self.rfrac_rank1(prurar, pc, kl, batch_xian)
                return batch_xian, batch_xian_rank
            return batch_xian

    def x(self,prurar,pc,kl,score_ranking,typ):
        if not is_num(score_ranking):
            return
        try:
            kl = convert_kl(kl)
            if prurar in ['北京','天津','上海','江苏','江西','广东']:
                fens=self.frac_rank_dict[prurar][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][0]
                paims=self.frac_rank_dict[prurar][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][1]
            elif prurar == '山西':
                if "专科" in pc or ('二' in pc and ("C" in pc or "c" in pc)):
                    cengci = "专科"
                else:
                    cengci = "本科"
                fens = self.frac_rank_dict[prurar][f'{prurar}_{kl}_{cengci}'][0]
                paims = self.frac_rank_dict[prurar][f'{prurar}_{kl}_{cengci}'][1]
            else:
                if prurar == '内蒙古':
                    if '蒙授' in prurar and '蒙授' not in kl:
                        kl='蒙授'+kl
                fens=self.frac_rank_dict['other'][f'{prurar}_{kl}'][0]
                paims=self.frac_rank_dict['other'][f'{prurar}_{kl}'][1]
            if typ==1:
                return paims[fens.index(min(fens, key=lambda x: abs(float(x) - float(score_ranking))))]
            return fens[paims.index(min(paims, key=lambda x: abs(float(x) - float(score_ranking))))]
        except:
            return

    #返回分数位次
    def rfrac_rank1(self,prurar,pc,kl,score):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param score:分数
        :return:返回分数对应位次
        """
        return self.x(prurar,pc,kl,score,1)

    #返回位次对应分数
    def rfrac_rank2(self,prurar,pc,kl,rank):
        """
        :param prurar:省市区
        :param pc:批次
        :param kl:科类
        :param rank:分数
        :return:返回位次对应分数
        """
        return self.x(prurar, pc, kl, rank, 2)
        # kl = convert_kl(kl)
        # if prurar in '江苏':
        #     fens=self.frac_rank_dict['江苏'][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][0]
        #     paims=self.frac_rank_dict['江苏'][f'{prurar}_{kl}_{"专科" if "专科" in pc else "本科"}'][1]
        # else:
        #     fens=self.frac_rank_dict['other'][f'{prurar}_{kl}'][0]
        #     paims=self.frac_rank_dict['other'][f'{prurar}_{kl}'][1]
        # return fens[paims.index(min(paims, key=lambda x: abs(float(x) - float(ranking))))]

def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info("开始时间：{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info('共耗时：%f秒' % (time.time() - start_time))
        logger.info("结束时间：{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))))
        return result
    return wrapper

#提取专业名称中招生标签
def exenla(major,maispb=False,return_string=False):
    """
    :param major:专业名称
    :param maispb:是否查找匹配标签
    :param return_string:返回字符串
    :return: 专业名称中的标签
    """
    bqs={'招生标签':list(list_dupl([v for v in
              ['国家专项', '地方专项', '帮扶专项', '预科', '联合培养', '中外合作', '校企合作', '高职本科', '高校专项', '联合办学','精准扶贫','少数民族', '民族班', '少民', '闽台', '优师', '公费', '订单', '双语', '定向']
                if v in major and f'非{v}' not in major])),
    '匹配标签': list(list_dupl([v for v in
                       ['师范','苏区专项']
                    if v in major and f'非{v}' not in major]))
     }
    zhonhwaihezuo=re.search('中[^心]合作',major)
    if zhonhwaihezuo and '中外合作' not in bqs['招生标签']:
        bqs['招生标签'].append('中外合作')
    if return_string:
        return '、'.join(bqs['招生标签'])
    return bqs if maispb else bqs['招生标签']

#获取表头中字段名称索引，表头以列表形式传入
def getexcelth(rowdatas0,ht):
    """
    :param rowdatas0:表头以列表形式传入
    :param ht:表头中字段名称
    :return: 字段索引
    """
    for i,v in enumerate(rowdatas0):
        if ht == v:
            return i
    if '科类' == ht:
        ht='文\理科'
    for i,v in enumerate(rowdatas0):
        if ht == v:
            return i
    if '招生标签' == ht:
        ht='招生类型'
    for i,v in enumerate(rowdatas0):
        if ht in v:
            return i
    ht='专业名称' if ht=='业名称' else ht
    ht='招生标签' if ht=='招生类型' else ht
    ht='科类' if ht=='文\理科' else ht
    raise ValueError(f'表头中未找到“{ht}”相关字段名称，可以将“{ht}”字段添加至表中或将相应字段修改为“{ht}”')

#保留有效的小数位
def prvadepl(num):
    if type(num)==float or type(num)==numpy.float64:
        num = eval(str(num).rstrip('0').rstrip('.'))
    return num

#提取专业名称中专业名称和括号部分内容，根据需要返回一级大类和二级大类
class ExtractEnrollmentLabels:
    def __init__(self):
        self.data={f'{v[0]}_{v[1]}':v[1:] for v in ReadData('专业、大类以及逻辑代码').data[1:]}

    def exmana(self,major,batch,school_name):
        """
        :param major:专业名称
        :param batch:批次
        :param school_name:学校名称，学校名称中有“职业”关键字优先在职业本科查找专业名称信息
        :return:专业名称、专业名称逻辑代码、二级大类、二级大类逻辑代码、一级大类、一级大类逻辑代码
        """
        major_name = get_major_name(major)[0]
        if '专科' in batch:
            return self.data.get('专科' + '_' + major_name, [None] * 6)
        else:
            major_name = '本科预科班' if '预科' in major_name else major_name
            mana = self.data.get('本科' + '_' + major_name)
            if mana:
                return mana
            if '职业' in school_name:
                return self.data.get('职业本科' + '_' + major_name, [None] * 6)
        return [None] * 6

#对列表中的多个列表以第某个元素进行排序
def sortedlbys(lists,i,reverse=False):
    """
    :param lists:数据列表
    :param i:一维数据中基准索引
    :param reverse:排序方式，默认False，有小到大
    :return:排序后的数据列表
    """
    sorted_lists = sorted(lists, key=lambda x: x[i], reverse=reverse)
    return sorted_lists

class UpdateName():
    """
    更新院校名称和专业名称
    """
    def __init__(self):
        with open('c:/mysql_config.json', 'r', encoding='utf-8') as f:
            mysql_config = json.load(f)['1']
        db = pymysql.connect(host=mysql_config['host'], port=3306, user='root', password=mysql_config['password'],
                                  database=mysql_config['database'])
        cursor = db.cursor()
        cursor.execute('select * from 更新院校名称名单')
        schools=cursor.fetchall()
        self.schools = sorted(list(schools), key=lambda x: len(x[0]), reverse=True)
        zk_majors, bk_majors = [], []
        cursor.execute('select * from 更新专业名称名单')
        majors = cursor.fetchall()
        for v in majors:
            if v[0] == '本科':
                bk_majors.append(v[1:])
            elif v[0] == '专科' and v[1] != '汽车检测与维修技术':
                zk_majors.append(v[1:])
        self.zk_majors = sorted(zk_majors, key=lambda x: len(x[0]), reverse=True)
        self.bk_majors = sorted(bk_majors, key=lambda x: len(x[0]), reverse=True)
        cursor.close()
        db.close()

    def update_school_name(self, name):
        name=optstr(name)
        for school in self.schools:
            if name.startswith(school[0]):
                return name.replace(school[0], school[1], 1)
        return name

    def update_major_name(self,batch, name):
        name=optstr(name)
        re_name=re.search('(^[\u4e00-\u9fa5、]+)(.*)',name)
        if re_name:
            re_name=re_name.groups(1)
            if '专科' in batch or '二段' in batch:
                for major in self.zk_majors:
                    if re_name[0]==major[0]:
                        return major[0]+re_name[1]
            else:
                for major in self.bk_majors:
                    if re_name[0]==major[0]:
                        return major[0]+re_name[1]
        return name

#删除字符串首尾看不见的字符，将中文括号改为英文括号，以及其他符号的替换
def optstr(values:Union[str,list,dict]):
    def format_str(s):
        s=s.strip()
        return s.replace('（', '(').replace('）', ')').replace('\t', '').replace('\n', '').replace(r'\n', '').replace('\r','').replace(' ', '').replace('\xa0', ' ').replace('★', ' ').replace('☆',' ').replace('▲', ' ').replace('\u3000', '')
    if not values:
        return values
    elif type(values)==str:
        return format_str(values)
    elif type(values)==list:
        for i,value in enumerate(values):
            value=prvadepl(value)
            if type(value) == str:
                values[i]=format_str(value)
    elif type(values)==dict:
        for i,value in enumerate(values.values()):
            value=prvadepl(value)
            if type(value) == str:
                values.values()[i] = format_str(value)
    return values

def get_major_name(s):
    """
    获取专业名称
    """
    name=re.search('([\u4e00-\u9fa5、]+)(.*)',optstr(s))
    if name:
        return name.groups(1)

class GetSchoolName:
    """
    获取院校名称
    """
    def __init__(self):
        self.schools=sorted([x[0] for x in ReadData('院校名称').data[1:]], key=lambda x: len(x), reverse=True)
    def __call__(self,school):
        school=optstr(school)
        for school_name in self.schools:
            if school.startswith(school_name):
                return [school_name,school.replace(school_name,'',1)]

def get_code_name(s):
    """
    提取院校代码和名称或专业代码和名称
    """
    code = re.search('(^[0-9A-Za-z]+)', optstr(s)).group(1)
    name = optstr(s.lstrip(code))
    return [code,name]

def is_school(string):
    """
    判断是否为学校名称
    """
    re_string=re.search('([\u4e00-\u9fa5]+)',optstr(string))
    if re_string:
        re_string=re_string.group(1)
        if re_string.endswith('大学') or re_string.endswith('学院') or re_string.endswith('学校') or re_string.endswith('分校'):
            return True

def unify_keys(ks):
    """
    统一表头字段名称
    """
    key_dict={x[0]: x[1] for x in ReadData('读取数据时表头字段统一化参考表').data[1:]}
    for i,k1 in enumerate(ks):
        for k2,ys in key_dict.items():
            for y in ys.split(','):
                if y==k1:
                    ks[i]=k2
                    break
    return ks