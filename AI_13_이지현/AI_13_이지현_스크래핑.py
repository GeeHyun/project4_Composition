from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
from selenium.common.exceptions import UnexpectedAlertPresentException


COMPOSER = '쇼팽'

def get_midi(COMPOSER, PAGES):

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    # 로그인
    LOGIN_URL = f'https://midiex.net/bbs/login.php?url=/'
    driver.get(LOGIN_URL)

    driver.find_element(By.CSS_SELECTOR, '#login_id').send_keys('miso324@naver.com')
    driver.find_element(By.CSS_SELECTOR, '#login_pw').send_keys('pforplj4')   # 프로젝트용 비밀번호
    driver.find_element(By.CSS_SELECTOR, '#login_fs > div:nth-child(4) > input.btn.btn-primary.btn-block').click()
    
    # 원하는 키워드 검색 결과에서 음악 번호 알아내기
    for i in range(PAGES):
        LIST_URL = f'https://midiex.net/bbs/board.php?bo_table=midi&sfl=wr_subject%7C%7Cwr_content&stx={COMPOSER}&sop=and&page={i+1}'
        page = requests.get(LIST_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        subjects = soup.find_all(class_="td_subject")

        # 음악 번호를 이용해 다운로드 진행
        for subject in subjects:
            try:
                midi_num = subject.find('a')['href'].split('/')[-1]

                DOWN_URL = f'https://midiex.net/midi/{midi_num}'
                driver.get(DOWN_URL)

                driver.find_element(By.CSS_SELECTOR, '#bo_v_file > ul > li > a.view_file_download > strong').click()
                time.sleep(10)
            
            # 파일이 삭제되었을 경우 발생하는 오류 대처
            except UnexpectedAlertPresentException:
                pass

if __name__ == '__main__':
    get_midi(COMPOSER, 4)
