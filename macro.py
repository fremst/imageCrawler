import requests
import ftplib
import warnings
import time
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, NoAlertPresentException, UnexpectedAlertPresentException
from tkinter import *
import pyautogui
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import os


# pyinstaller macro.py -F --upx-dir C:\DevStudy\upx401w64\

def get_config_data():
    _config_data = {
        'login_id': None,
        'login_pwd': None,
        'ftp_ip': None,
        'ftp_port': None,
        'ftp_id': None,
        'ftp_pwd': None,
        'ftp_folder': None,
        'ftp_url': None,
        'wait_scroll': 1,
        'wait_alert': 0.1,
    }
    try:
        with open(os.getcwd() + '/config.dat') as file:
            input_data = file.read().splitlines()
    except FileNotFoundError:
        print('config.dat 파일을 찾을 수 없습니다.')
        pyautogui.alert("config.dat 파일을 찾을 수 없습니다.")
        exit(0)

    for key in _config_data:
        for elem in input_data:
            if elem.startswith(key):
                _config_data[key] = elem.split(key + ":")[1].strip()
    if ~_config_data['ftp_folder'].endswith('/'):
        _config_data['ftp_folder'] = _config_data['ftp_folder'] + '/'
    if ~_config_data['ftp_url'].endswith('/'):
        _config_data['ftp_url'] = _config_data['ftp_url'] + '/'
    _config_data['ftp_url'] = _config_data['ftp_url'] + _config_data['ftp_folder']
    return _config_data


def login():
    login_window = Tk()
    login_window.wm_attributes("-topmost", 1)
    login_window.title("자동입력방지")
    login_window.geometry("290x52")

    label1 = Label(login_window, width=14, text="자동입력방지")
    label1.grid(row=1, column=1)
    entry1 = Entry(login_window, width=20)
    entry1.grid(row=1, column=2)
    entry1.focus()
    # entry3.bind("<Return>", confirm_login(login_window, entry1.get(), entry2.get(), entry3.get()))
    button1 = Button(login_window, width=40, text="확인",
                     command=lambda: confirm_login(login_window, entry1.get()))
    button1.grid(row=4, column=1, columnspan=2)
    login_window.mainloop()


def confirm_login(_login_window, _captcha):
    _login_window.destroy()

    id_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_id"]')
    id_input.click()
    id_input.clear()
    id_input.send_keys(config_data['login_id'])

    pwd_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_pass"]')
    pwd_input.click()
    pwd_input.clear()
    pwd_input.send_keys(config_data['login_pwd'])

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
    # raw_img_srcs = soup.find_all('img', {'src': re.compile('^https://'), 'origin': ""})
    raw_img_srcs = soup.find_all('img', {'style': "", 'class': "", 'origin': ""})
    _img_srcs = []
    for elem in raw_img_srcs:
        _img_src = str(elem.get('src'))
        _img_srcs.append(elem.get('src'))
    return _img_srcs


def upload_imgs(popup_url, date_time, popup_url_ind, _uid):
    _img_srcs = get_imgs(popup_url)
    session = ftplib.FTP()
    session.connect(config_data['ftp_ip'], int(config_data['ftp_port']))
    session.login(config_data['ftp_id'], config_data['ftp_pwd'])
    session.encoding = 'utf-8'
    try:
        session.mkd(config_data['ftp_folder'])
    except Exception:
        pass

    for _img_src_ind, _img_src in enumerate(_img_srcs):
        print("상품 번호: [" + _uid + "] 옵션: (" + str(popup_url_ind) + ", " + str(_img_src_ind) + ") 업로드 진행중")
        if _img_src.startswith('//'):
            _img_src = 'https:' + _img_src
        req = Request(_img_src, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as f:
            session.storbinary(
                'STOR /' + config_data['ftp_folder'] + _uid + '_'
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
        action.move_to_element(_url_input).perform()
        print("상품 번호: [" + _uid + "] 옵션: (" + str(popup_url_ind) + ", " + str(_url_inputs_ind) + ") 이미지 변경 진행중")
        _file_name = config_data['ftp_url'] + _base_file_name + str(_url_inputs_ind) + ".jpg"
        _url_input.click()
        _url_input.clear()
        _url_input.send_keys(_file_name)
        _url_input.send_keys(Keys.ENTER)
        while True:
            try:
                time.sleep(float(config_data['wait_alert']))
                alert = driver.switch_to.alert
                alert.accept()
                break
            except NoAlertPresentException:
                pass


def close_job(_driver, _wait_window):
    _driver.close()
    _wait_window.destroy()


def main_job():
    driver.get('https://tmg191.cafe24.com/mall/admin/admin_goods.php?ps_num=100&ps_page=1')

    wait_window = Tk()
    wait_window.wm_attributes("-topmost", 1)
    wait_window.title("대기")
    wait_window.geometry("150x52")
    button1 = Button(wait_window, width=20, text="진행",
                     command=lambda: [driver.execute_script('send_search()'), wait_window.destroy()])
    button1.grid(row=1, column=1, columnspan=1)
    button2 = Button(wait_window, width=20, text="종료", command=lambda: close_job(driver, wait_window))
    button2.grid(row=2, column=1, columnspan=1)
    wait_window.mainloop()

    page_num = int(1)
    job_count = int(0)
    success = int(0)
    fail = int(0)

    base_url = None
    try:
        base_url = driver.current_url.split('ps_page')[0] + '&ps_page='
    except InvalidSessionIdException:
        sys.exit()

    while True:
        url = base_url + str(page_num)
        driver.get(url)

        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(float(config_data['wait_scroll']))
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
                        with open(os.getcwd() + '/error.txt', 'w') as file:
                            file.write('[' + uid + '] ' + str(e))
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

    config_data = get_config_data()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action = ActionChains(driver)

    driver.get('https://tmg191.cafe24.com/mall/admin/admin_login.php')
    login()
    while True:
        main_job()

