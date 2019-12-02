from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from functools import reduce
import os, time, csv, random


# chrome选项
chromeoptions = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {'notifications': 2},
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
    # 'profile.managed_default_content_settings.images': 2,
}
chromeoptions.add_experimental_option('prefs', prefs)
# chromeoptions.add_argument('--headless')
# chromeoptions.add_argument('--disable-gpu')
# chromeoptions.add_argument('blink-settings=imagesEnabled=false') 
chromeoptions.add_argument('--user-agent=Mozilla/5.0 HAHA')
chromeoptions.add_argument('log-level=3')
chromeoptions.add_argument('lang=zh_CN.UTF-8')
# 启动chrome
chromedriver = r"chromedriver.exe"
driver = webdriver.Chrome(chromedriver, options=chromeoptions)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get('https://study.163.com/my')
# driver.refresh()
# time.sleep(5)

try:
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'ux-btn.th-bk-main.ux-btn-.ux-btn-.ux-modal-btn.um-modal-btn_ok.th-bk-main')))
    driver.find_element_by_class_name('ux-btn.th-bk-main.ux-btn-.ux-btn-.ux-modal-btn.um-modal-btn_ok.th-bk-main').click()
except:
    pass

# # driver.find_element_by_xpath("//a[@class='third-link f-fl' and text()='QQ']").click()
# qqlogin = driver.find_element_by_link_text('QQ')
# # qqlogin.click()
# driver.execute_script("$(arguments[0]).click()", qqlogin)

while driver.current_url != 'https://study.163.com/my?from=study':
    time.sleep(5)
    # driver.refresh()

mypages = driver.find_elements_by_xpath("//li[@class='ux-pager_itm']")[-1].text
print("参与学习的课程共{}页".format(mypages))
mypages = int(mypages)
mycurls = list()
for itx in range(1, mypages + 1):
    if itx == 1:
        mycurls.append('https://study.163.com/my?from=study')
    else:
        mycurls.append(r'https://study.163.com/my#/courses?p=' + str(itx))

mylist = list() # 参加的课程列表
for url in mycurls:
    plist = list()
    # print("查看参与课程分页{}".format(url))
    if driver.current_url != url:
        driver.get(url)
        time.sleep(5)
    css = driver.find_elements_by_xpath("//div[@class='uc-course-card']")

    for csx in css:
        urlx = csx.find_elements_by_tag_name('a')
        curl = csx.find_elements_by_tag_name('a')[0].get_attribute('href')
        cname = csx.find_element_by_xpath(".//div[@class='uc-ykt-course-card_title']").text
        # print("课程 {}".format(cname))
        cprogress = ''
        cprogresst = ''
        if len(urlx) == 1:
            if csx.find_elements_by_xpath(".//div")[2].get_attribute('class') == 'uc-ykt-course-card_progress':
                cprogress = csx.find_element_by_xpath(".//div[@class='uc-ykt-course-card_progress_current']").get_attribute('style')
                cprogresst = csx.find_element_by_xpath(".//div[@class='uc-ykt-course-card_progress_txt']").text
            elif csx.find_elements_by_xpath(".//div")[2].get_attribute('class') == 'uc-ykt-course-card_done':
                cprogress = '100%'
                cprogresst = '100%'
        else:
            cprogress = '0'
            cprogresst = '0'

        dictx = dict()
        dictx['itemName'] = cname
        dictx['itemUrl'] = curl
        dictx['itemProgress'] = cprogress
        dictx['itemProgresst'] = cprogresst    
        plist.append(dictx)
        mylist.append(dictx)
    

print("参与学习课程总数： {}".format(len(mylist)))
with open('mylessons.csv', 'w', newline='', encoding='UTF-8') as f:
    header = ['itemName', 'itemUrl', 'itemProgress', 'itemProgresst']
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    for row in mylist:
        writer.writerow(row)
print("参与学习课程列表保存在 mylessons.csv 文件中")

driver.quit()



        