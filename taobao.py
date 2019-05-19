from selenium import webdriver as wb
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pyautogui
import threading

global browser


def switchWindows(browser, i):
    browser.switch_to_window(browser.window_handles[i])


def __login__(username, password, pathA, pathB):
    pyautogui.PAUSE = 0.5  # 设置每个动作0.2s太快来不及输入密码
    options = wb.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 切换到开发者模式
    browser = wb.Chrome(options=options)
    browser.maximize_window()  # 窗口最大化保证坐标正确
    browser.get('https://login.taobao.com/member/login.jhtml')
    # try:
    # left,top,width,height=pyautogui.locateOnScreen('G:/jupyter project/淘宝/login_switch_blue.PNG')
    # except:
    # left,top,width,height=pyautogui.locateOnScreen('G:/jupyter project/淘宝/login_switch.PNG')      获取login_switch位置
    time.sleep(3)
    moveToX = 1484
    moveToY = 297
    pyautogui.moveTo(1484, 297)  # 移动到切换登录的位置
    pyautogui.click()  # 点击切换按钮
    pyautogui.typewrite(username)
    pyautogui.press('tab')
    pyautogui.typewrite(password)
    errorType = 0
    try:
        left, top, width, height = pyautogui.locateOnScreen(pathA)
        print('识别蓝色')
        moveToX = left + 140
        moveToY = top + 15
        print(moveToX, moveToY)
        pyautogui.moveTo(moveToX, moveToY)
        pyautogui.mouseDown()
        moveToX = moveToX + 300
        pyautogui.moveTo(moveToX, moveToY)
        pyautogui.mouseUp()
        pyautogui.moveTo(moveToX - 250, moveToY + 60)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
    except:
        errorType = 1  # 识别不出蓝色

    if errorType == 1:
        try:
            left, top, width, height = pyautogui.locateOnScreen(pathB)
            moveToX = left + 200
            moveToY = top + 20
            print('识别红色')
            print(moveToX, moveToY)  # 1299 497
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseDown()
            moveToX = moveToX + 300
            pyautogui.moveTo(moveToX, moveToY)
            pyautogui.mouseUp()
            pyautogui.moveTo(moveToX - 250, moveToY + 60)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        except:
            errorTye = 2  # 识别不出绿色

    if errorType == 2:
        print('没有滑块')
        pyautogui.moveTo(1189, 497)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
    # 调整到淘宝首页

    wait = wdw(browser, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="//www.taobao.com/"]'))).click()

    return browser  # 返回浏览器当前的页面


def openPage(browser):  # 打开nike

    wait = wdw(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'q'))).send_keys('nike')
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'iframe[class="srp-iframe"]'))).click()  # 打开新窗口
    # browser.execute_script("(arguments[0]).click()",a)   淘宝启用了noscrpit反爬
    switchWindows(browser, 1)  # 切换窗口

    # 打开女子,打开女子就验证
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           'a[href="//nike.tmall.com/category-1394890745.htm?spm=a1z10.5-b-s.w4011-14234872789.54.4b40295bxWLzrN&search=y&scene=taobao_shop#TmshopSrchNav"]'))).click()
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[href="//nike.tmall.com/category-1394899096.htm?spm=a1z10.5-b-s.w4011-14234872789.90.5694295bEoa4Mm&search=y&scene=taobao_shop#TmshopSrchNav"]'))).click()
    # browser.refresh()
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[href="//nike.tmall.com/category-1394899099.htm?spm=a1z10.5-b-s.w4011-14234872789.70.2e8a295bMdIyvv&search=y&scene=taobao_shop#TmshopSrchNav"]'))).click()
    return browser


def nextClass(browser, page):
    wait = wdw(browser, 10)
    name = str(page)
    tryTime = 0
    while tryTime < 10:  # 如果点击失败了，就再试一次，四次都不成功就退出
        # time.sleep(5)
        try:
            a = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="J_TWidget nav180"]//dd[' + name + ']/a')))  # 分类
            print(a.text)
            browser.execute_script("(arguments[0]).click()", a)  # 用脚本点击不用刷新
            switchWindows(browser, 2)  # 现在一共有三个窗口切换过去
            print(browser)
            return browser  # 打开完以后就返回
        except:
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="J_sufei"]')))
            tryTime = tryTime + 1
            print('原来是检测了不要刷新，在循环一次试试')


def getGoods(browser):
    time.sleep(3)
    wait = wdw(browser, 10)
    for row in range(1, 11):  # 商品一个最多多少行 ，只有正常退出循环才有下一页
        for col in range(1, 5):  # 每一行多少个商品也就是多少列,因为最后一个是item-last所以这里不能选节点
            row = str(row)
            col = str(col)
            try:
                d = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           '//div[@class="J_TItems"]//div[@class="item4line1"][' + row + ']//dl[' + col + ']/dd[@class="thumb"]/preceding-sibling::*[1]//img')))
                # d.click()#打开物品
                print(d.text)
                browser.execute_script("(arguments[0]).click()", d)  # 用脚本点击不用刷新
                switchWindows(browser, 3)  # 切这个窗口才能打印
                # 点击了商品check一下
                shoe = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@data-spm="1000983"]'))).text
                print('型号:' + shoe)
                sales = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="tm-count"]'))).text
                print('月销量:' + sales)
                try:
                    promoteprice = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//dl[@class="tm-promo-panel tm-promo-cur"]//span[@class="tm-price"]'))).text
                    print('促销价格¥:' + promoteprice)
                except:
                    promoteprice = '不做促销'
                    print(promoteprice)

                sales = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//dl[@id="J_StrPriceModBox"]//span[@class="tm-price"]'))).text
                print('原价格:¥' + sales)
                browser.close()  # 打印完关闭
                switchWindows(browser, 2)  # 切回去
                # browser.refresh()            #刷新
            except:
                print("找不到商品")
                return browser  # 找完商品了测试有没有下一页
    return browser  # 找完商品了测试有没有下一页


def nextPage(browser):
    # time.sleep(3) #挺十秒在爬
    # browser.refresh()  #在nextpage这里出错
    wait = wdw(browser, 10)
    try:
        nextPage = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="J_SearchAsync next"]')))
        print(nextPage.text)
        browser.execute_script("(arguments[0]).click()", d)  # 用脚本点击不用刷新
        print(browser)
        return browser, True
    except:
        browser.close()
        switchWindows(browser, 1)
        print('nextPage没有下一页')
        print(browser)
        return browser, False  # 没有下一页了


def getImformation(browser):
    Class = 2
    while True:

        browser = nextClass(browser, Class)  # 打开第一个分类

        print('打开第几个分类了')
        print(Class)
        while True:
            browser = getGoods(browser)
            browser, isNextPage = nextPage(browser)
            print(isNextPage)
            if isNextPage == False:
                print('没有下一页')
                break
        Class += 1
        if Class == 13:
            break


def checkAction():
    pyautogui.moveTo(837 + 318, 479 + 10)
    pyautogui.mouseDown()
    pyautogui.moveTo(837 + 318, 479 + 10 + 50)
    pyautogui.mouseUp()
    pyautogui.moveTo(800, 479 + 10 + 100 + 30)
    pyautogui.mouseDown()
    pyautogui.moveTo(1200, 479 + 10 + 100 + 30)
    pyautogui.mouseUp()


def check(browser):  # 把这个函数弄成多线程函数然后挂起它，一旦遇到问题了在调用
    mutex = threading.Lock()
    wait = wdw(browser, 5)  # 验证模块少等一点，而寻找模块等久一点，防止出现验证模块的时候切换到了寻找模块
    while True:
        mutex.acquire()
        print('执行一次')
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="J_sufei"]')))
            print('验证成功')
            checkAction()
            browser.refresh()  # 验证成功要刷新一次才能获取
            handle = browser.current_window_handle
            browser.switch_to_window(handle)
            time.sleep(30)  # 每次验证了久等待
            # return browser  如果return回去的话线程就会死掉
            # except:
            # print('未找到验证模块')  #一旦没有找打验证模块说明，只是因为没有刷新才遇到了问题
            # handle=browser.current_window_handle
            # browser.refresh() #验证成功要刷新一次才能获取
            # browser.switch_to_window(handle)
            # return browser
        except:
            print('没有检测到模块')
        mutex.release()


if __name__ == '__main__':
    browser = __login__('18778386305', 'sjl56123', 'G:/jupyter project/淘宝/block_blue.PNG',
                        'G:/jupyter project/淘宝/block_red.PNG')
    browser = openPage(browser)
    threads = []
    t1 = threading.Thread(target=getImformation, args=(browser,))
    # getImformation(browser)
    threads.append(t1)
    t2 = threading.Thread(target=check, args=(browser,))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()

# ime.sleep(5)
# int('开始')
# utton=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search')))
# utton.click()18778386305sjl56123
# login_switch=browser.find_element_by_css_selector("#J_Quick2Static")  #通过id找到18778386305数据流6123
# username=browser.find_element_by_css_selector('input[name="T18778386305PL_username"]')  #找节点通过属性18778386305sjl5612318718778386305睡觉了61231877838630518778386305升级了612378386305sjl56123
# login_switch.click()18778386305数据流6123
# username.send_keys('18778386305')
# password=browser.find_element_by_css_selector('input[name="TPL_password"]')
# password.send_keys('sjl56123')
# block=browser.find_element_by_css_selector('span[id="nc_1_n1z"]')18778386305数据量6123s
# moveBlock=ActionChains(browser)
# moveBlock.click_and_hold(block).perform()
# moveBlock.move_by_offset(10,0).perform()

# moveBlock.drag_and_drop_by_offset(block,298,0).perform()