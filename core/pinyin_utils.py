from Pinyin2Hanzi import *
from functools import reduce
from utils.logger import Logger

dagparams = DefaultDagParams()
pinyin_group = list(all_pinyin())
logger = Logger()

## 接口方法，拼音转中文
def translate_pinyin_to_Chinese(pinyin: str) -> str:
    pinyin = initialize(pinyin)
    result = ''
    loc = 0
    for i, word in enumerate(pinyin):
        if not('a' <= word <= 'z' or 'A' <= word <= 'Z' or word == '\''):
            result += word
            loc = i + 1
    pinyin = pinyin[loc:]
    if("\'" in pinyin):
        return result + translate(pinyin.split("\'"))
    else:
        return result + translate(split_pinyin(pinyin))
    
## 划分连续的一段拼音串为多个拼音列表
def split_pinyin(pinyin: str) -> list:
    res_list = []
    i = 0
    while(True):
        if i == len(pinyin):
            break
        flag = True
        for j in range(len(pinyin), i, -1):
            if j == i:
                flag = False
                break
            if pinyin[i:j] in pinyin_group or simplify_pinyin(pinyin[i:j]) in pinyin_group:
                res_list.append(pinyin[i:j])
                i = j - 1
                break
        if not flag:
            res_list.append(pinyin[i:])
            break
        i += 1
    return res_list

## 初始化和规范化拼音字符串的前后部分
def initialize(pinyin: str) -> str:
    pinyin = pinyin.strip().strip("\'").lower()
    return pinyin

## 规范化单个拼音：lue -> lve
def standardize(pinyin_list: list) -> list:
    for i, py in enumerate(pinyin_list):
        pinyin_list[i] = simplify_pinyin(py)
    return pinyin_list

## 转化拼音为文字
def translate(pinyin_list: list) -> str:
    pinyin_list = standardize(pinyin_list)
    logger.info(f"拼音分割后: {pinyin_list}")
    res_list = []
    for i in range(len(pinyin_list), 0, -1):
        if len(dag(dagparams, pinyin_list[:i], path_num=1)) != 0:
            res_list = dag(dagparams, pinyin_list[:i], path_num=1)[0].path
            break
    logger.info(f"转化为中文后: {res_list}")
    return reduce(lambda x, y: x + y, res_list)