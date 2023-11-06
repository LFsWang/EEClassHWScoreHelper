from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
import os, time


options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)
#driver.implicitly_wait(30) 

## Setting
# 看網址後面的數字是什麼
# https://eeclass.nthu.edu.tw/course/?????
course_id = '15245'
# https://eeclass.nthu.edu.tw/course/homework/?????
homework_id = '29741'

# Wait for login
def manual_login():
    driver.get("https://eeclass.nthu.edu.tw/")
    print("請登入帳號... waiting...")
    wait = WebDriverWait(driver, 120)
    wait.until(lambda d : d.current_url == "https://eeclass.nthu.edu.tw/dashboard")
    print("login ok")

def manual_role():
    driver.get("https://eeclass.nthu.edu.tw/course/" + course_id)
    print("請改為助教權限 waiting...")
    wait = WebDriverWait(driver, 120, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException])
    wait.until(lambda d : d.find_element(By.CSS_SELECTOR, "#mbox-inline > div > div:nth-child(5)").text[:6] != "身份: 學生")
    print("TA ok")

def loadCSV(filepath):
    res = []
    with open(filepath) as f:
        while True:
            buf = f.readline()
            if not buf:
                break
            v = buf.strip().split(',')
            res.append(v)
    return res

def upload_score_pdf(student_id, score):
    driver.get("https://eeclass.nthu.edu.tw/homework/noSubmitList/" + homework_id + "?search=" + student_id)
    try:     
        button = driver.find_element(By.CSS_SELECTOR, "#submitList_table > tbody > tr > td.text-center.col-char7 > div > a")
    except:
        print("找不到同學 " + student_id + "，可能已上傳成績。")
        return
    button.click()
    time.sleep(5)
    

    # upload page is iframe
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "#iframelgModalId > div > div > div.modal-body > iframe"))

    input_score = driver.find_element(By.CSS_SELECTOR, "#auditScore > div > div > div > input")
    input_score.send_keys(score)

    driver.find_element(By.CSS_SELECTOR, "#auditAttachment > div > div > button").click()
    time.sleep(3)

    drop_area = driver.find_element(By.CSS_SELECTOR, "#auditReport_form_auditNote_uploadModal-area > input[type=file]")
    filepath =  os.path.abspath("uploads/" +  student_id + ".pdf")
    print(filepath)
    drop_area.send_keys(filepath)

    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "#auditReport_form_auditNote_uploadModal > div > div > div.modal-footer > div.buttons.text-center > button").click()
    driver.implicitly_wait(15)
    driver.find_element(By.CSS_SELECTOR, "#auditReport_form > div.form-group.fs-form-buttons > div > button.btn.btn-primary").click()
    driver.implicitly_wait(15)

    driver.switch_to.default_content()
    time.sleep(2)


data = loadCSV("score.csv")
manual_login()
manual_role()
print(data)
for student_id, score in data:
    upload_score_pdf(student_id, score)
