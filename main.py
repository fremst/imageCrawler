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


## pyinstaller main.py -F --upx-dir C:\DevStudy\upx401w64\


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
    driver.execute_script('window.open("'+_url+'");')
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


def login():

    root = Tk()
    root.wm_attributes("-topmost", 1)
    root.title("로그인")
    root.geometry("290x92")

    label1 = Label(root, width=14, text="아이디")
    label1.grid(row=1, column=1)
    entry1 = Entry(root, width=20)
    entry1.insert(0, "thelight47")
    entry1.grid(row=1, column=2)
    label2 = Label(root, width=14, text="비밀번호")
    label2.grid(row=2, column=1)
    entry2 = Entry(root, show="*", width=20)
    entry2.insert(0, "11")
    entry2.grid(row=2, column=2)
    label3 = Label(root, width=14, text="자동입력방지")
    label3.grid(row=3, column=1)
    entry3 = Entry(root, width=20)
    entry3.grid(row=3, column=2)
    entry3.focus()
    # entry3.bind("<Return>", login(event=""))
    button1 = Button(root, width=40, text="로그인", command=lambda: main_job(root, entry1.get(), entry2.get(), entry3.get()))
    button1.grid(row=4, column=1, columnspan=2)
    root.mainloop()


def main_job(_root, _id, _pwd, _captcha):

    _root.destroy()

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

    page_num = int(1)
    job_count = int(0)
    success = int(0)
    fail = int(0)
    while True:
        driver.get(
            'https://tmg191.cafe24.com/mall/admin/admin_goods.php?amode=detail_search&search_d=&ps_gmarket_option'
            '=&date_type=&start_yy=2022&start_mm=12&start_dd=12&end_yy=2022&end_mm=12&end_dd=12&ps_site_id=&ps_category'
            '=&ps_market_id=&ps_status=sale&search_type=goods_name&ps_subject=&ps_fn=&ps_sort=dateup&ps_num=100&ps_simple'
            '=&ps_modify=&ps_page=' + str(page_num)
        )

        # TODO: 일시 정지 후 대기 버튼 클릭하면 진행
        
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
