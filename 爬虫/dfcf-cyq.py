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

# 定义调试函数
def screenshot_debug(browser, name):
    OUT_DIR = 'output/screenshot'
    browser.save_screenshot("%s/%s.png" % (OUT_DIR, name))

# 初始化浏览器
def browser_init():
    # 无界面模式运行,参考:https://blog.csdn.net/Artificial_idiots/article/details/108490448
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-proxy-server')
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    ua = '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) ' + \
         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    chrome_options.add_argument(ua)
    chrome_options.add_argument('--start-maximized')
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
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

# 从新浪财经获取股票交易日期
def get_trade_date(stock_code):
    print('从新浪财经获取%s最新的交易日期' % stock_code)
    # 从新浪财经获取最近的交易日期
    url = 'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%%20_%s_60_1608109168173=/CN_MarketDataService.getKLineData?symbol=%s&scale=%d&ma=no&datalen=%d' % (stock_code, stock_code, 240, 70)
    contents = urlopen(url).read().decode()
    contents = re.findall('=\((.*)\);', contents)  # 寻找=(到);之间的内容
    contents = json.loads(contents[0])
    dates = [ content['day'] for content in contents]
    date = dates[-60:] if (len(dates) >= 60) else dates  # 取出最后60个
    return date

# 比较东财日期大小
def compare_date(t1, t2):
    '''
    def y(x):
        x_str = x[0:4] + x[5:7] + x[8:10]
        return int(x_str)
    '''
    y = lambda x: int(x[0:4] + x[5:7] + x[8:10])
    diff = y(t1) - y(t2)
    # print(y(t1), y(t2), diff)
    if diff > 0:
        return 1
    elif diff == 0:
        return 0
    else:
        return -1

# 检查数据是否有重复,根据日期判断即可
def check_data_error(contents, stock_code):
    # 设置需要用到的变量
    x = []
    status = -1
    # 对比数据日期以便判断数据是否存在问题
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
    MAX_REPEAT, STEP, RANDOM_STEP = 4, 5.4, 5.4

    ### 获取今日所有股票列表
    print('正在获取今日所有开盘股票')
    codes = get_list()
    print(codes)

    ### 打开网页并等待所有元素加载完成
    browser = browser_init()
    for code in codes:
        if 'N' in code['名称']:
            print('%s为当日上市新股,暂时不处理' % code['名称'])
            continue
        print('正在获取股票%s-%s的数据' % (code['名称'], code['代码']))
        browser.get('http://quote.eastmoney.com/concept/%s.html' % code['代码'])
        browser.find_element_by_xpath('//*[@id="type-selector"]/a[5]').click()  # 点击'日K'按钮
        browser.find_element_by_id('btn-cyq').click()  # 点击'筹码分布'按钮
        screenshot_debug(browser, code['代码'] + '-1')
        canvas = browser.find_element_by_xpath('//*[@id="chart-container"]/div[2]/canvas[2]')
        canvas_width = canvas.get_attribute('width')
        canvas_height = canvas.get_attribute('height')
        # print(canvas_width, canvas_height)
        # wait_data(browser)

        ### 移动鼠标然后抓取数据
        ### 移动到柱状图页面,以STEP为单位逐步向右移动以便抓取数据,避免定位不准导致的重复或者遗漏问题
        # 取得最后60个交易日期
        trade_date = get_trade_date(code['代码'])
        print('最后60个交易日为%s' % trade_date)
        # 取得最新交易时间
        zxsj = browser.find_element_by_xpath('//*[@id="quote-time"]').text[:10]
        print('最新交易日为%s' % zxsj)
        # 移动到柱状图最左边
        action = ActionChains(browser)
        element = browser.find_element_by_xpath('//*[@id="chart-container"]/div[2]/canvas[2]')
        action.move_to_element_with_offset(element, 0, (int(canvas_height)*2)/3).perform()
        screenshot_debug(browser, code['代码'] + '-2')
        # 逐步向右移动获取柱状图对应筹码分布
        contents = []
        # 1.非N开头新股移动到最左边元素/trade_date[0]
        while True:
            action.move_by_offset(STEP, 0).perform()
            content = wait_data(browser)
            if 0 == compare_date(content[0], trade_date[0]):
                print('已移动到最左边的元素')
                contents.append(content)
                break
        screenshot_debug(browser, code['代码'] + '-3')
        print(contents)
        # 2.逐步向右移动到最右边元素trade_date[-1],依次对比每个日期并取数据
        repeat_cnts = 0
        for date in trade_date[1:]:
            while True:
                content = wait_data(browser)
                ret = compare_date(content[0], date)
                print(content[0], date, ret)
                # 避免获取了最后一个交易日数据,移动微小距离
                if (content[0] != date) and (content[0] == trade_date[-1]):
                    action = ActionChains(browser)
                    action.move_by_offset(RANDOM_STEP, 0).perform()
                    continue
                # 判断是否移动到对应元素
                if 0 == ret:
                    print('已找到到日期%s的元素,将向右移动寻找元素' % date)
                    contents.append(content)
                    action = ActionChains(browser)
                    action.move_by_offset(STEP, 0).perform()
                    break
                elif -1 == ret:
                    print('鼠标依旧处于滞后元素位置,将向右移动寻找元素')
                    action = ActionChains(browser)
                    action.move_by_offset(STEP, 0).perform()
                elif 1 == ret:
                    print('鼠标依旧处于超前元素位置,将向左移动寻找元素')
                    action = ActionChains(browser)
                    action.move_by_offset((0 - STEP), 0).perform()
        screenshot_debug(browser, code['代码'] + '-4')
        print(contents)

        ### 判断取到的数据是否存在问题
        ret = check_data_error(contents, code['代码'])
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
