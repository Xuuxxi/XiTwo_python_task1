import requests
import re
import pymysql


# encoding=utf-8
# 抢救乱码里的数据
def getCh(a):
    # 将指定字符通过正则表达式提取出来
    pattern = "[B|C|D|K|\-|1-9|\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    results = regex.findall(a)
    return results


# 数据导入数据库
def imp(a, tmType):
    host = 'localhost'
    username = 'root'
    password = '123456'
    db_name = 'xuuxxi_for_task1'
    insert_table_sql = """\
    INSERT INTO pta(tm_id,tm_name,tm_type)
     VALUES('{tm_id}','{tm_name}','{tm_type}')
    """
    delete_table_sql = """\
DELETE FROM pta 
"""
    connection = pymysql.connect(host=host,
                                 user=username,
                                 password=password,
                                 charset='utf8mb4',
                                 db=db_name)
    try:
        with connection.cursor() as cursor:
            for i in range(0, len(a[0])):
                cursor.execute(
                    insert_table_sql.format(tm_id=a[0][i], tm_name=a[1][i], tm_type=tmType))
            connection.commit()
    finally:
        # 删除所有数据
        '''
        with connection.cursor() as cursor:
            cursor.execute(delete_table_sql)
            connection.commit()
        '''
        connection.close()


# problem 会出现乱码，但中文输出正确。
def start(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    temp = r.text
    temp1 = getCh(temp)
    # 去除多余字符
    try:
        num = int(len(temp1))
        for i in range(0, num):
            a = temp1[i]
            if len(a) == 1:
                temp1.pop(i)
    except:
        pass
    return temp1


# 分离题目和编号
def Split(a):
    cnt = 0
    result1 = []
    result2 = []
    result = []
    for i in a:
        if (cnt % 2) == 0:
            result1.append(i)
        else:
            result2.append(i)
        cnt += 1
    # 抢救消失的零
    for i in range(0, len(result1)):
        if (i + 1) % 10 == 0:
            result1[i] += '0'
    result.append(result1)
    result.append(result2)
    return result


if __name__ == "__main__":
    url = ['https://pintia.cn/api/problem-sets/14/problem-list?problem_type=CODE_COMPLETION&page=0&limit=100',
           'https://pintia.cn/api/problem-sets/14/problem-list?problem_type=PROGRAMMING&page=0&limit=100']
    temp = start(url[0])
    tm_fn = Split(temp)
    imp(tm_fn, 'CODE_COMPLETION')
    temp = start(url[1])
    tm_pro = Split(temp)
    imp(tm_pro, 'PROGRAMMING')
