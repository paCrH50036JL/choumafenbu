# coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
import pandas as pd
import time
from urllib.request import urlopen
import json
import re

# 获取当日所有股票信息:
# 地址: http://35.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408020983883791639_1617375883153&pn=1&pz=4000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1617375883158
# 说明: pn=1-从哪页开始,pz=4000-获取多少个数据
def get_list():
    # 抓取数据
    url = 'http://35.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408020983883791639_1617375883153&pn=%s&pz=%s&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1617375883158' % (1, 4000)
    content = urlopen(url=url).read().decode()
    # print(content)
    # 解析数据
    content = re.findall('\((.*)\);', content)  # 寻找(到);之间的内容
    content = json.loads(content[0])
    codes = []
    for info in content['data']['diff']:
        # f12-代码 f13-地区(0-sz,1-sh) f14-名称
        # print(info['f12'], info['f13'], info['f14'])
        code = {'名称':info['f14'], '代码': ('sz' if info['f13'] == 0 else 'sh') + info['f12']}
        codes.append(code)
    # print(codes, len(codes), content['data']['total'])
    return codes


# 初始化浏览器
def browser_init():
    # 无界面模式运行,参考:https://blog.csdn.net/Artificial_idiots/article/details/108490448
    option = webdriver.ChromeOptions()
    # option.add_argument('window-size=1920x3000')  # 指定浏览器分辨率,此数值设置关系到后面的移动距离10.8,变为太小会导致元素遗漏
    # option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # option.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=executable_path, options=option)
    return browser

# '''
# 1.整个图片大小:990*600，开始默认处于最中心位置，向左为负向右为正
# 2.使用My Ruler插件测量可知,总柱状个数为60个(右侧19、中间1、左侧40)、长度为1086-436=650,因此每个距离大约为10.83
# 3.轨迹来回重复的问题: https://blog.csdn.net/YungGuo/article/details/110557087
# '''
# # 取原点数据
# action.move_by_offset(0, 0).perform()
# print(browser.find_element_by_xpath(XPATH).text)
# # 取左边数据,然后回原点
# action.move_by_offset(-10, 0).perform()
# print(browser.find_element_by_xpath(XPATH).text)
# action.move_by_offset(10, 0).perform()
# # 取右边数据,然后回原点
# action.move_by_offset(10, 0).perform()
# print(browser.find_element_by_xpath(XPATH).text)
# action.move_by_offset(-10, 0).perform()
def wait_data(browser):
    TIMEOUT = 100

    xpath1 = '//*[@id="chart-container"]/div[1]/div[3]/div[1]/span'
    xpath2 = '//*[@id="chart-container"]/div[1]/div[3]/div[2]/span'
    xpath4 = '//*[@id="chart-container"]/div[1]/div[3]/div[4]/span'
    xpath5 = '//*[@id="chart-container"]/div[1]/div[3]/div[5]/span'
    xpath6 = '//*[@id="chart-container"]/div[1]/div[3]/div[6]/span'
    xpath7 = '//*[@id="chart-container"]/div[1]/div[3]/div[7]/span'
    xpath8 = '//*[@id="chart-container"]/div[1]/div[3]/div[8]/span'
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath1)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath2)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath4)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath5)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath6)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath7)))
    # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath8)))
    # 1.js页面会存在刷新问题导致某个瞬间读取不到对象,处理方式为多次尝试直到读取到为止
    # 2.详细参考: https://blog.csdn.net/zhangvalue/article/details/102921631
    while True:
        try:
            x1 = browser.find_element_by_xpath(xpath1).text
            x2 = browser.find_element_by_xpath(xpath2).text
            x4 = browser.find_element_by_xpath(xpath4).text
            x5 = browser.find_element_by_xpath(xpath5).text
            x6 = browser.find_element_by_xpath(xpath6).text
            x7 = browser.find_element_by_xpath(xpath7).text
            x8 = browser.find_element_by_xpath(xpath8).text
            break
        except:
            pass
    return [x1, x2, x4, x5, x6, x7, x8]

# 检查数据是否有重复,根据日期判断即可
def test_data(contents):
    x = []
    status = -1
    for tmp in contents:
        x.append(tmp[0])
    if len(set(x)) == len(x):
        status = 0
        print('###########无错误#######')
    else:
        status = -1
        print('###########有错误#######')
    return status, len(x), x

if __name__ == "__main__":
    ### 定义用到的变量
    LEFT, RIGHT, ERROR_CNTS = 40, 20, 10
    STEP = 10.8

    ### 获取今日所有股票列表
    print('正在获取今日所有开盘股票')
    codes = get_list()
    print(codes)

    ### 打开网页并等待所有元素加载完成
    browser = browser_init()
    for code in codes:
        if 'N' in code['名称']:
            print('%s为当日上市新股,暂时不处理')
            continue
        print('正在获取股票%s-%s的数据' % (code['名称'], code['代码']))
        browser.get('http://quote.eastmoney.com/concept/%s.html' % code['代码'])
        browser.find_element_by_xpath('//*[@id="type-selector"]/a[5]').click()  # 点击'日K'按钮
        browser.find_element_by_id('btn-cyq').click()  # 点击'筹码分布'按钮
        canvas = browser.find_element_by_xpath('//*[@id="chart-container"]/div[2]/canvas[2]')
        canvas_width = canvas.get_attribute('width')
        canvas_height = canvas.get_attribute('height')
        # print(canvas_width, canvas_height)
        # wait_data(browser)

        ### 移动鼠标然后抓取数据
        ### 移动到柱状图页面,以STEP为单位逐步向右移动以便抓取数据,避免定位不准导致的重复或者遗漏问题
        # 取得最新交易时间
        zxsj = browser.find_element_by_xpath('//*[@id="quote-time"]').text[:10]
        # 移动到柱状图最左边
        action = ActionChains(browser)
        element = browser.find_element_by_xpath('//*[@id="chart-container"]/div[2]/canvas[2]')
        action.move_to_element_with_offset(element, 0, int(canvas_height)/2).perform()
        # 逐步向右移动获取柱状图对应筹码分布
        contents = []
        # 1.非N开头新股需要移动到时间不为zxsj,代表最左边元素
        while True:
            action.move_by_offset(STEP, 0).perform()
            content = wait_data(browser)
            if content[0] != zxsj:
                print('已移动到最左边的元素')
                contents.append(content)
                break
        print(contents)
        # 2.逐步向右移动到时间为zxsj,代表最右边元素
        while True:
            action = ActionChains(browser)
            action.move_by_offset(STEP, 0).perform()
            content = wait_data(browser)
            # 判断是否移动到最右边元素
            if content[0] == zxsj:
                print('已移动到最右边的元素')
                contents.append(content)
                break
            else:
                # 判断是否移动到新元素
                if content not in contents:
                    contents.append(content)
        print(contents)

        ### 判断取到的数据是否存在问题
        ret = test_data(contents)
        if ret[0] != 0:
            exit()

        ### 使用pandas进行处理
        df = pd.DataFrame(contents)
        columns = {0: '日期', 1: '获利比例', 2: '平均成本', 3: '90%成本', 4: '集中度', 5: '70%成本', 6: '集中度'}
        df.rename(columns=columns, inplace=True)
        print(df)
        df.to_csv(path_or_buf='output/%s.csv' % code['代码'], index=False, encoding='gbk')

        ### 延迟一下获取下一个股票数据
        time.sleep(1)

    ### 退出
    browser.quit()
