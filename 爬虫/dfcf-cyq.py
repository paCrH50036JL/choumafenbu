# coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
import pandas as pd
import time

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
    # https://blog.csdn.net/zhangvalue/article/details/102921631
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
    LEN = 60

    x = []
    status = -1
    for tmp in contents:
        x.append(tmp[0])
    if len(set(x)) == len(x) == LEN:
        status = 0
        print('###########无错误#######')
    else:
        status = -1
        print('###########有错误#######')
    return status, len(x), x

if __name__ == "__main__":
    ### 定义用到的变量
    LEFT, RIGHT = 40, 20
    STEP = 10.8

    ### 初始化并打开网站页面
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    options = webdriver.ChromeOptions()
    # options.headless = True
    browser = webdriver.Chrome(executable_path=executable_path, options=options)
    # browser.maximize_window()
    browser.get('http://quote.eastmoney.com/concept/sh603322.html')
    browser.find_element_by_id('cmfb-btn').click()
    wait_data(browser)

    ### 移动鼠标然后抓取数据
    # 取得最新交易时间
    zxsj = browser.find_element_by_xpath('//*[@id="quote-time"]').text[:10]
    # 移动到柱状图页面,以2为单位逐步向右移动以便抓取数据,避免定位不准导致的重复或者遗漏问题
    action = ActionChains(browser)
    action.move_to_element(browser.find_element_by_xpath('//*[@id="chart-container"]/div[1]')).perform()
    contents_right = []
    contents_right.append(wait_data(browser))
    while True:
        action = ActionChains(browser)
        action.move_by_offset(STEP, 0).perform()
        content = wait_data(browser)
        if (len(contents_right) != (RIGHT - 1)) and (content[0] == zxsj):  # 元素未刷新,继续移动
            continue
        else:
            if content not in contents_right:  # 判断是否移动到了新元素
                contents_right.append(content)
        if len(contents_right) == RIGHT:  # 判断是否遍历完毕
            break
    print(contents_right)
    # 移动到柱状图页面,以1为单位逐步向左移动以便抓取数据,避免定位不准导致的重复或者遗漏问题
    action = ActionChains(browser)
    action.move_to_element(browser.find_element_by_xpath('//*[@id="chart-container"]/div[1]')).perform()
    contents_left = []
    while True:
        action = ActionChains(browser)
        action.move_by_offset((0 - STEP), 0).perform()
        content = wait_data(browser)
        if (content not in contents_left) and \
                (content[0] != contents_right[0]) and (content[0] != zxsj):  # 判断是否移动到了新元素
            contents_left.append(content)
        if len(contents_left) == LEFT:  # 判断是否遍历完毕
            break
    print(contents_left)

    ### 处理拿到的数据
    contents = contents_left[::-1] + contents_right
    print(contents)
    ret = test_data(contents)
    print(ret)
    if ret[0] != 0:
        exit()

    ### 使用pandas进行处理
    df = pd.DataFrame(contents)
    columns = {0: '日期', 1: '获利比例', 2: '平均成本', 3: '90%成本', 4: '集中度', 5: '70%成本', 6: '集中度'}
    df.rename(columns=columns, inplace=True)
    print(df)
    df.to_csv(path_or_buf='cyq.csv', index=False, encoding='gbk')

    ### 退出
    browser.quit()
