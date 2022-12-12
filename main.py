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
from selenium.common.exceptions import NoSuchElementException

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


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
        session.storbinary('STOR /NEW/' + _uid + '.jpg', f)
    session.quit()


def change_image(_url, _uid):
    driver.execute_script('window.open("'+_url+'");')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    url_input = driver.find_element(By.CSS_SELECTOR, '#main_0_input')
    url_input.click()
    url_input.clear()
    url_input.send_keys("http://thelight47777.add4s.co.kr/TreeImgjl4/NEW/" + _uid + ".jpg")
    # time.sleep(1)
    url_input.send_keys(Keys.ENTER)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    chrome_options = Options()

    # 브라우저 자동 종료 방지
    chrome_options.add_experimental_option("detach", True)

    # 불필요한 에러 메시지 미출력
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 셀레니움 로그 무시
    warnings.filterwarnings("ignore", category=DeprecationWarning)  # Deprecated warning 무시

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action = ActionChains(driver)

    # 웹페이지 이동

    driver.get('https://tmg191.cafe24.com/mall/admin/admin_login.php')
    driver.implicitly_wait(5)  # 로딩까지 5초간 대기
    driver.maximize_window()  # 화면 최대화

    id_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_id"]')

    id_input.click()
    id_input.clear()
    id_input.send_keys('thelight47')

    pwd_input = driver.find_element(By.CSS_SELECTOR, 'input[name="login_pass"]')
    pwd_input.click()
    pwd_input.clear()
    pwd_input.send_keys('11')

    captcha_input = driver.find_element(By.CSS_SELECTOR, 'input[name="cap_text"]')
    captcha_input.click()
    captcha_input.clear()
    captcha_input.send_keys(input('자동입력 방지 문자를 입력해주세요.\n:'))
    captcha_input.send_keys(Keys.ENTER)

    page_num = 1
    # TODO: page_num 순회 및 예외 처리
    driver.get(
        'https://tmg191.cafe24.com/mall/admin/admin_goods.php?amode=detail_search&search_d=&ps_gmarket_option'
        '=&date_type=&start_yy=2022&start_mm=12&start_dd=12&end_yy=2022&end_mm=12&end_dd=12&ps_site_id=&ps_category'
        '=&ps_market_id=&ps_status=sale&search_type=goods_name&ps_subject=&ps_fn=&ps_sort=dateup&ps_num=100&ps_simple'
        '=&ps_modify=&ps_page=' + str(page_num)
        )
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        curr_height = driver.execute_script("return document.body.scrollHeight")

        if curr_height == prev_height:
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")

    # TODO: 예외 처리
    item_ids = driver.find_elements(By.CSS_SELECTOR, 'input[name="uid_hidden[]"]')
    for item_id in item_ids:
        uid = item_id.get_attribute('value')
        popup_url = get_url(uid)

        img_src = get_image(popup_url)
        upload_image(img_src, uid)
        print("상품번호 [" + uid + "] 업로드 완료!")
        change_image(popup_url, uid)
        print("상품번호 [" + uid + "] 이미지 변경 완료!")
