from selenium import webdriver
from functools import reduce
import time, csv

chromeoptions = webdriver.ChromeOptions()
# 关闭chrome通知
prefs = {
    'profile.default_content_setting_values': {'notifications': 2},
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
}
chromeoptions.add_experimental_option('prefs', prefs)
chromeoptions.add_argument('--headless')
chromeoptions.add_argument('--disable-gpu')
chromeoptions.add_argument('--user-agent=Mozilla/5.0 HAHA')
chromeoptions.add_argument('log-level=3')
chromeoptions.add_argument('lang=zh_CN.UTF-8')

# 指定chromedriver路径
chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

driver = webdriver.Chrome(chromedriver, options=chromeoptions)
driver.maximize_window()
driver.implicitly_wait(5)

driver.get(r'https://study.163.com/')
# 关闭用户协议页面
agbtn = driver.find_element_by_class_name('um-modal-btn_ok')
if agbtn:
    agbtn.click()
# 关闭首页弹出登录提示
time.sleep(3)
uxclose = driver.find_element_by_xpath("//i[@class='ux-icon ux-icon-close']")
if uxclose:
    uxclose.click()

# clst = c1lst + c2lst + c3lst
# clst = reduce(lambda x, y: x if y in x else x + [y], [[], ] + clst)
c1lst = list()
c2lst = list()
c3lst = list()
clst = list()

cs = driver.find_element_by_css_selector("[class='j-courseCat nitem courseCat f-f0  f-fl']")
csleftdiv = cs.find_element_by_css_selector("[class='ux-component-category-menu_left j-categoryLeft']")
csrightdiv = cs.find_element_by_css_selector("[class='ux-component-category-menu_right fadeInOut j-categoryRight']")

# 获取1级类别
cslefta = csleftdiv.find_elements_by_class_name('ux-component-category-menu_left_item_name')
c1lst.clear()
for it in cslefta:
    ita = it.get_attribute('data-log-data')
    itx = eval(ita)
    item1 = dict()
    item1['itemId'] = itx['itemId']
    item1['itemName'] = itx['itemName']
    item1['itemUrl'] = itx['itemUrl']
    item1['itemLevel'] = 1
    item1['itemParent'] = ''
    c1lst.append(item1)

# 获取2、3级类别
c2rightdiv = csrightdiv.find_elements_by_class_name('f-cb')
c2lst.clear()
c3lst.clear()
for it2 in c2rightdiv:
    it2a = it2.find_element_by_class_name('ux-component-category-menu_right_item_cat2.f-fl')
    ita = it2a.get_attribute('data-log-data')
    itemx = eval(ita)
    item2 = dict()
    item2['itemId'] = itemx['itemId']
    item2['itemName'] = itemx['itemName']
    item2['itemUrl'] = itemx['itemUrl']
    item2['itemLevel'] = 2
    item2['itemParent'] = ''
    c2lst.append(item2)
    c3righta = it2.find_elements_by_class_name('ux-component-category-menu_right_item_cat3_name')
    c3x = list()
    for it in c3righta:
        ita = it.get_attribute('data-log-data')
        c3x.append(eval(ita))
    for it3 in c3x:
        c3lst.append({
        'itemId': it3['itemId'],
        'itemName': it3['itemName'],
        'itemUrl': it3['itemUrl'],
        'itemLevel': 3,
        'itemParent': item2['itemId']
        })

clst = c1lst + c2lst + c3lst
driver.quit()

# 类别列表写入文件
header = ['itemId', 'itemName', 'itemUrl', 'itemLevel', 'itemParent']
with open('clst.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    for item in clst:
        writer.writerow(item)

