from selenium import webdriver
import time, csv, random

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

# 指定chromedriver路径
chromedriver = r"chromedriver.exe"

driver = webdriver.Chrome(chromedriver, options=chromeoptions)
driver.maximize_window()
driver.implicitly_wait(30)

driver.get(r'https://study.163.com/')
time.sleep(5)
# 关闭用户协议页面
agbtn = driver.find_element_by_class_name('um-modal-btn_ok')
if agbtn:
    agbtn.click()
# 关闭首页弹出登录提示
# uxclose = driver.find_element_by_xpath("//i[@class='ux-icon ux-icon-close']")
# if uxclose:
#     uxclose.click()

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

# c3lst = list(filter(lambda x: x['itemLevel'] == '3', clst))
c3lst = list(x for x in clst if x['itemLevel'] == '3')
print("3级类别总数： {}".format(len(c3lst)))

lessons = list()
for item in c3lst:
    lessons.clear()
    # 打开3级分类链接
    print("开始搜索3级课程类别：<{}> 下的课程".format(item['itemName']))
    c3url = item['itemUrl']
    if not c3url:
        continue
    driver.get(c3url)
    time.sleep(random.randint(5, 10))
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

    print("\t 3级课程类别<{}>有{}页课程".format(item['itemName'], pcount))
    # 打开课程分页， 获取课程信息
    for urlx in urls:
        driver.get(urlx)
        # print('正在搜索分页: {}'.format(urlx))
        time.sleep(5)
        cs = driver.find_elements_by_xpath("//li[@class='uc-course-list_itm f-ib']")
        
        for itx in cs:
            csx = itx.find_element_by_tag_name('div') # 获取课程logType,itemId,itemName
            curl = csx.find_element_by_css_selector("[class='uc-coursecard uc-ykt-coursecard f-fl']")
            cscore = csx.find_element_by_css_selector("[class='uc-starrating_score']")
            cprice = csx.find_element_by_css_selector("[class='uc-ykt-coursecard-wrap_price f-pa']")

            # 课程ID、名称
            csd = eval(csx.get_attribute('data-log-data'))
            dictx = dict()
            for k, v in csd.items():
                dictx[k] = v
            # print(dictx['itemId'], dictx['itemName'])
            # 课程链接 itemUrl            
            csd = eval(curl.get_attribute('data-log-data'))
            for k, v in csd.items():
                dictx[k] = v
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
    header = ['logType', 'itemId', 'itemName', 'c3Id', 'c3Name', 'itemUrl', 'itemScore', 'itemPrice']
    with open('lessons.csv', 'a+', newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, header)
        # writer.writeheader()
        for item in lessons:
            writer.writerow(item)

driver.quit()
