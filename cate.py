from selenium import webdriver
from functools import reduce
import time

chromeoptions = webdriver.ChromeOptions()
# 关闭chrome通知
prefs = {
    'profile.default_content_setting_values': {'notifications': 2},
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
}
chromeoptions.add_experimental_option('prefs', prefs)
# chromeoptions.add_argument('--headless')
# chromeoptions.add_argument('--disable-gpu')
chromeoptions.add_argument('--user-agent=Mozilla/5.0 HAHA')
chromeoptions.add_argument('log-level=3')
chromeoptions.add_argument('lang=zh_CN.UTF-8')

# 指定chromedriver路径
chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

driver = webdriver.Chrome(chromedriver, options=chromeoptions)
driver.maximize_window()
driver.implicitly_wait(15)

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


# 汇总类别列表
clst = list()

c1s = driver.find_elements_by_xpath("//a[@class='ux-component-category-menu_left_item_name']")
c1lst = list()

cx = list()
for it in c1s:
    ita = it.get_attribute('data-log-data')
    cx.append(eval(ita))
if c1s:
    for it in cx:
        c1lst.append({
            'itemId': it['itemId'],
            'itemName': it['itemName'],
            'itemUrl': it['itemUrl'],
            'itemLevel': 1,
            'itemParent': ''
        })
c1lst = reduce(lambda x, y: x if y in x else x + [y], [[], ] + c1lst)

c2lst = list()
for it1 in c1lst:
    driver.get(it1['itemUrl'])
    time.sleep(2)
    c2s = driver.find_elements_by_xpath("//span[@class='ux-category-breadcrumb-cat2-item cat_item']")
    # c2ss = driver.find_element_by_xpath("//div[@class='ux-category-breadcrumb-cat3']")
    if c2s:
        for it2 in c2s:
            ita = it2.find_element_by_tag_name('a')
            c2lst.append({
                'itemId': ita.get_attribute('data-id'),
                'itemName': ita.text,
                'itemUrl': ita.get_attribute('href'),
                'itemLevel': 2,
                'itemParent': it1['itemId']
            })
# c2lst = reduce(lambda x, y: x if y in x else x + [y], [[], ] + c2lst)

c3lst = list()
for it2 in c2lst:
    driver.get(it2['itemUrl'])
    time.sleep(2)
    c3s = driver.find_elements_by_xpath("//span[@class='ux-category-breadcrumb-cat3-item cat_item']")
    if c3s:
        for it3 in c3s:
            ita = it3.find_element_by_tag_name('a')
            c3lst.append({
                'itemId': ita.get_attribute('data-id'),
                'itemName': ita.text,
                'itemUrl': ita.get_attribute('href'),
                'itemLevel': 3,
                'itemParent': it2['itemId']
            })

clst = c1lst + c2lst + c3lst
clst = reduce(lambda x, y: x if y in x else x + [y], [[], ] + clst)