from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, csv, random, os
from functools import reduce


# chrome选项
chromeoptions = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {'notifications': 2},
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
    'profile.managed_default_content_settings.images': 2,
}
chromeoptions.add_experimental_option('prefs', prefs)
chromeoptions.add_argument('--headless')
chromeoptions.add_argument('--disable-gpu')
chromeoptions.add_argument('blink-settings=imagesEnabled=false') 
chromeoptions.add_argument('--user-agent=Mozilla/5.0 HAHA')
chromeoptions.add_argument('log-level=3')
chromeoptions.add_argument('lang=zh_CN.UTF-8')
# 启动chrome
chromedriver = r"chromedriver.exe"
driver = webdriver.Chrome(chromedriver, options=chromeoptions)
driver.maximize_window()
driver.implicitly_wait(10)

# 读取类别列表
clst = list()
with open('clst.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    csv_reader = csv.DictReader(f, fieldnames=header)
    for row in csv_reader:
        dictx = dict()
        for k, v in row.items():
            dictx[k] = v
        clst.append(dictx)

if os.path.exists('lessons.csv'):
    os.remove('lessons.csv')

# c3lst = list(filter(lambda x: x['itemLevel'] == '3', clst))
c3lst = list(x for x in clst if x['itemLevel'] == '3')
print("3级类别总数： {}".format(len(c3lst)))

# 读取已完成3级类别列表文件clst3done.csv
c3lstdone = list()
if os.path.exists('clst3done.csv'):
    with open('clst3done.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        csv_reader = csv.DictReader(f, fieldnames=header)
        for row in csv_reader:
            dictx = dict()
            for k, v in row.items():
                dictx[k] = v
            c3lstdone.append(dictx)
# c3lstdone = reduce(lambda x, y:x if y in x else x + [y], [[],] + c3lst)
# 去除已经搜索过课程的3级类别
for lx in c3lstdone:
    c3lst.remove(lx)
print("本次搜索3级课程类别有{}条".format(len(c3lst)))

# 开始搜索
lessons = list()
titleset = set()
for item in c3lst:
    lessons.clear()
    # 打开3级分类链接
    print("查找3级课程类别：<{}> 下的课程".format(item['itemName']))
    c3url = item['itemUrl']
    if not c3url:
        continue
    driver.get(c3url)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    # 关闭用户协议页面
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'um-modal-btn_ok')))
        agbtn = driver.find_element_by_class_name('um-modal-btn_ok')
        agbtn.click()
    except:
        pass
    # 部分3级页面是同一2级页面，跳过
    c3title = driver.title
    if c3title in titleset:
        continue
    else:
        titleset.add(c3title)
    print("跳过3级课程类别<{}>链接{}重复内容".format(item['itemName'], item['itemUrl']))

    # time.sleep(5)
    # 获取3级分类课程分页url列表
    cps = driver.find_elements_by_xpath("//li[@class='ux-pager_itm']")
    # pnext = driver.find_element_by_xpath("//li[@class='ux-pager_btn ux-pager_btn__next']")
    urls = list() # 分页链接
    if len(cps) > 1:
        pcount = int(cps[-1].text)
        for i in range(pcount):
            if i == 0:
                url = c3url
            else:
                url = c3url + r"#/?p=" + str(i+1)
            urls.append(url)
    else:
        pcount = 1
        urls.append(c3url)

    # print("\t3级课程类别<{}>有{}页课程".format(item['itemName'], pcount))
    # 打开3级课程分类分页， 获取课程信息
    for urlx in urls:
        driver.get(urlx)
        # print('\t搜索分页: {}'.format(urlx))
        time.sleep(3)
        driver.refresh()
        time.sleep(5)
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'uc-course-list_item')]")))
        cs = driver.find_elements_by_xpath("//li[@class='uc-course-list_itm f-ib']")
        # cs = driver.find_elements_by_xpath("//li[contains(@class, 'uc-course-list_item')]")
        # print("\t该分页共有{}门课程".format(len(cs)))
        
        for itx in cs:
            csx = itx.find_element_by_tag_name('div') # 获取课程logType,itemId,itemName
            # 课程ID、名称
            csd = eval(csx.get_attribute('data-log-data'))
            dictx = dict()
            for k, v in csd.items():
                dictx[k] = v
            # print("{} \t {}".format(dictx['itemId'], dictx['itemName']))
            # curl = csx.find_element_by_css_selector("[class='uc-coursecard uc-ykt-coursecard f-fl']")
            # curl = csx.find_element_by_xpath(".//div[@class='uc-coursecard uc-ykt-coursecard f-fl']")
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'uc-coursecard')]")))
                curl = csx.find_element_by_xpath(".//div[contains(@class,'uc-coursecard')]")
            except:
                curl = ''

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='uc-starrating_score']")))
                # cscore = csx.find_element_by_css_selector("[class='uc-starrating_score']")
                # cscore = csx.find_element_by_xpath(".//span[@class='uc-starrating_score']")
                cscore = csx.find_element_by_xpath(".//span[contains(@class, 'uc-starrating_score')]")
            except:
                cscore = ''
            
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='uc-ykt-coursecard-wrap_price f-pa']")))
                # cprice = csx.find_element_by_css_selector("[class='uc-ykt-coursecard-wrap_price f-pa']")
                cprice = csx.find_element_by_xpath(".//div[contains(@class, 'uc-ykt-coursecard-wrap_price')]")
            except:
                cprice = ''

            
            # 课程链接 itemUrl 
            if curl:           
                csd = eval(curl.get_attribute('data-log-data'))
                for k, v in csd.items():
                    dictx[k] = v
                dictx['itemUrl'] = 'https:' + dictx['itemUrl']
            # 课程评分            
            if cscore:
                dictx['itemScore'] = cscore.text
            else:
                dictx['itemScore'] = ''
            # 课程价格            
            if cprice:
                dictx['itemPrice'] = cprice.text
            else:
                dictx['itemPrice'] = ''
            # 课程3级类别ID、名称
            dictx['c3Id'] = item['itemId']
            dictx['c3Name'] = item['itemName']
            # 保存课程信息到课程列表
            lessons.append(dictx)

    print('\t 3级课程类别<{}>有{}门课程'.format(item['itemName'], len(lessons)))
    # 课程列表写入文件
    with open('lessons.csv', 'a+', newline='', encoding='UTF-8') as f:
        header = ['logType', 'itemId', 'itemName', 'c3Id', 'c3Name', 'itemUrl', 'itemScore', 'itemPrice']
        writer = csv.DictWriter(f, header)
        # writer.writeheader()
        for lx in lessons:
            writer.writerow(lx)
    
    # 保存已完成3级类别记录到文件clst3done.csv
    if os.path.exists('clst3done.csv'):
        with open('clst3done.csv', 'a+', newline='', encoding='UTF-8') as f:
            header = ['itemId', 'itemName', 'itemUrl', 'itemLevel', 'itemParent']
            writer = csv.DictWriter(f, header)
            writer.writerow(item)
    else:
        with open('clst3done.csv', 'w', newline='', encoding='UTF-8') as f:
            header = ['itemId', 'itemName', 'itemUrl', 'itemLevel', 'itemParent']
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerow(item)
    # 删除cookies      
    # driver.delete_all_cookies()

driver.close()
driver.quit()
