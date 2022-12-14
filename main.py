import requests
import ftplib
import warnings
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
from tkinter import *
import pyautogui
from webdriver_manager.chrome import ChromeDriverManager
import re
import datetime


# pyinstaller main.py -F --upx-dir C:\DevStudy\upx401w64\


def login():
    login_window = Tk()
    login_window.wm_attributes("-topmost", 1)
    login_window.title("로그인")
    login_window.geometry("290x92")

    label1 = Label(login_window, width=14, text="아이디")
    label1.grid(row=1, column=1)
    entry1 = Entry(login_window, width=20)
    entry1.insert(0, "thelight47")
    entry1.grid(row=1, column=2)
    label2 = Label(login_window, width=14, text="비밀번호")
    label2.grid(row=2, column=1)
    entry2 = Entry(login_window, show="*", width=20)
    entry2.insert(0, "11")
    entry2.grid(row=2, column=2)
    label3 = Label(login_window, width=14, text="자동입력방지")
    label3.grid(row=3, column=1)
    entry3 = Entry(login_window, width=20)
    entry3.grid(row=3, column=2)
    entry3.focus()
    # entry3.bind("<Return>", confirm_login(login_window, entry1.get(), entry2.get(), entry3.get()))
    button1 = Button(login_window, width=40, text="로그인",
                     command=lambda: confirm_login(login_window, entry1.get(), entry2.get(), entry3.get()))
    button1.grid(row=4, column=1, columnspan=2)
    login_window.mainloop()


def confirm_login(_login_window, _id, _pwd, _captcha):
    _login_window.destroy()

    id_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_id"]')
    id_input.click()
    id_input.clear()
    id_input.send_keys(_id)

    pwd_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_pass"]')
    pwd_input.click()
    pwd_input.clear()
    pwd_input.send_keys(_pwd)

    captcha_input = driver.find_element(By.CSS_SELECTOR, 'input[name="cap_text"]')
    captcha_input.click()
    captcha_input.clear()
    captcha_input.send_keys(_captcha)
    captcha_input.send_keys(Keys.ENTER)

    try:
        driver.maximize_window()
    except UnexpectedAlertPresentException:
        pyautogui.alert("다시 입력해 주세요.")
        login()


def get_popup_url(_uid):
    _url = "https://tmg191.cafe24.com/mall/admin/admin_goods_change_image_all.php?goods_uid=" + _uid
    return _url


def get_imgs(_popup_url):
    response = requests.get(_popup_url)
    soup = BeautifulSoup(response.text, "html.parser")
    raw_img_srcs = soup.find_all('img', {'src': re.compile('^https://'), 'origin': ""})
    _img_srcs = []
    for elem in raw_img_srcs:
        _img_srcs.append(elem.get('src'))
    return _img_srcs


def upload_imgs(popup_url, date_time, popup_url_ind, _uid):
    _img_srcs = get_imgs(popup_url)
    session = ftplib.FTP()
    session.connect('222.239.231.240', 2012)
    session.login("administrator", "J@dpftk4)")
    session.encoding = 'utf-8'

    for _img_src_ind, _img_src in enumerate(_img_srcs):
        print("상품 번호: [" + _uid + "] 옵션: (" + str(popup_url_ind) + ", " + str(_img_src_ind) + ") 업로드 진행중")
        with urlopen(_img_src) as f:
            session.storbinary(
                'STOR /NEW/' + _uid + '_'
                + date_time + '_'
                + str(popup_url_ind) + '_'
                + str(_img_src_ind) + '.jpg', f)
    session.quit()


def change_imgs(_url, _base_file_name):

    _url_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[id$="input"]')
    for _url_inputs_ind in range(len(_url_inputs)):
        _url_input = driver.find_elements(By.CSS_SELECTOR, 'input[id$="input"]')[_url_inputs_ind]
        _uid = _base_file_name.split("_")[0]
        popup_url_ind = _base_file_name.split("_")[2]
        # _action = ActionChains(driver)
        action.move_to_element(_url_input).perform()
        # driver.execute_script("window.scrollTo(0, 731)")
        # print(_url)
        # print(_url_input)
        print("상품 번호: [" + _uid + "] 옵션: (" + str(popup_url_ind) + ", " + str(_url_inputs_ind) + ") 이미지 변경 진행중")
        _file_name = "https://thelight47777.add4s.co.kr/TreeImgjl4/NEW/" + _base_file_name + str(_url_inputs_ind) + ".jpg"
        _url_input.click()
        _url_input.clear()
        _url_input.send_keys(_file_name)
        _url_input.send_keys(Keys.ENTER)
        while True:
            try:
                alert = driver.switch_to.alert
                alert.accept()
                break
            except NoAlertPresentException:
                time.sleep(0.1)


def main_job():
    driver.get('https://tmg191.cafe24.com/mall/admin/admin_goods.php?ps_num=100&ps_page=1')

    wait_window = Tk()
    wait_window.wm_attributes("-topmost", 1)
    wait_window.title("대기")
    wait_window.geometry("150x32")
    button1 = Button(wait_window, width=20, text="진행",
                     command=lambda: [driver.execute_script('send_search()'), wait_window.destroy()])
    button1.grid(row=1, column=1, columnspan=1)
    wait_window.mainloop()

    page_num = int(1)
    job_count = int(0)
    success = int(0)
    fail = int(0)

    base_url = driver.current_url.split('ps_page')[0] + '&ps_page='

    while True:
        url = base_url + str(page_num)
        driver.get(url)

        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            curr_height = driver.execute_script("return document.body.scrollHeight")

            if curr_height == prev_height:
                break
            else:
                prev_height = driver.execute_script("return document.body.scrollHeight")

        item_ids = driver.find_elements(By.CSS_SELECTOR, 'input[name="uid_hidden[]"]')
        if not item_ids:
            break

        for item_id in item_ids:
            job_count += 1
            print(f'{job_count}번째 상품')
            uid = item_id.get_attribute('value')
            popup_base_url = get_popup_url(uid)
            popup_urls = [popup_base_url, popup_base_url + '&mode=option', popup_base_url + '&mode=detail']
            driver.execute_script('window.open()')
            driver.switch_to.window(driver.window_handles[-1])

            try:
                for popup_url_ind, popup_url in enumerate(popup_urls):
                    driver.get(popup_url)
                    try:
                        date_time = datetime.datetime.now().strftime("%y%m%d")
                        upload_imgs(popup_url, date_time, popup_url_ind, uid)
                        _base_file_name = uid + '_' + date_time + '_' + str(popup_url_ind) + '_'
                        change_imgs(popup_url, _base_file_name)
                    except Exception as e:
                        print("작업 중 오류 발생")
                        print(e)
                        fail += 1
                        raise e
                success += 1
            except Exception as e:
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        page_num += 1
    pyautogui.alert(f'{job_count}개의 상품 작업 완료! 성공: {success}, 실패: {fail}')
    print(f'{job_count}개의 상품 작업 완료! 성공: {success}, 실패: {fail}')


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action = ActionChains(driver)

    driver.get('https://tmg191.cafe24.com/mall/admin/admin_login.php')
    login()
    main_job()
