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
    # entry3.bind("<Return>", login(event=""))
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


def get_url(_uid):
    _url = "https://tmg191.cafe24.com/mall/admin/admin_goods_change_image_all.php?goods_uid=" + _uid
    return _url


def get_image(_popup_url):
    response = requests.get(_popup_url)
    soup = BeautifulSoup(response.text, "html.parser")
    _img_src = soup.img['src']
    return _img_src


def upload_image(_img_src, _uid):
    session = ftplib.FTP()
    session.connect('222.239.231.240', 2012)
    session.login("administrator", "J@dpftk4)")
    session.encoding = 'utf-8'
    with urlopen(_img_src) as f:
        # TODO: 파일명 변경 ex. 101522_221213_1
        session.storbinary('STOR /NEW/' + _uid + '.jpg', f)
    session.quit()


def change_image(_url, _uid):
    driver.execute_script('window.open("' + _url + '");')
    # time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    url_input = driver.find_element(By.CSS_SELECTOR, '#main_0_input')
    url_input.click()
    url_input.clear()
    url_input.send_keys("https://thelight47777.add4s.co.kr/TreeImgjl4/NEW/" + _uid + ".jpg")
    url_input.send_keys(Keys.ENTER)
    while True:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            break
        except NoAlertPresentException:
            time.sleep(0.1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


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

    base_url = driver.current_url.split('ps_page')[0]+'&ps_page='

    while True:
        url = base_url+str(page_num)
        driver.get(url)

        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # TODO: 안정적인/빠른 버전 (1)
            time.sleep(1)
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
            popup_url = get_url(uid)

            img_src = get_image(popup_url)
            try:
                # TODO: 3개의 탭 이미지 모두 업로드
                upload_image(img_src, uid)
                print("상품 번호 [" + uid + "] 업로드 완료!")
                try:
                    # TODO: 3개의 탭 이미지 모두 변경
                    change_image(popup_url, uid)
                    print("상품 번호 [" + uid + "] 이미지 변경 완료!")
                    success += 1
                except Exception:
                    print("상품 번호 [" + uid + "] 이미지 변경 중 오류 발생")
                    fail += 1
                    continue
            except Exception:
                print("상품 번호 [" + uid + "] 업로드 중 오류 발생")
                fail += 1

        page_num += 1
    pyautogui.alert(f'{job_count}개의 상품 작업 완료! 성공: {success}, 실패: {fail}')


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
