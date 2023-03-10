
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

file_path = './pitcher.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# data = {}

driver = webdriver.Chrome()

# 연도범위 동안 팀리스트 스크래핑 후 json으로 저장
yearScope = range(1983, 2023)
team_List = ['SK', 'SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', 'kt', '히어로즈', '두산', '해태', '현대', '청보',
             '삼미', 'MBC', 'OB', '태평양', '빙그레', '쌍방울']

for year in yearScope:
    data[year] = []
    for team in team_List:
        url = 'http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys=%d&ye=%d&se=0&te=%s' \
              '&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=2&o1=FIP&o2=WAR' \
              '&de=0&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=' % (year, year, team)
        driver.get(url)
        trs = driver.find_elements(By.CSS_SELECTOR, '#mytable > tbody > tr')
        for index, item in enumerate(trs):
            if len(item.text) <= 5:
                continue
            if (item.find_elements(By.CSS_SELECTOR, 'th')):
                continue
            name = item.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text  # 선수명
            position = 'P'  # 포지션
            G = item.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text  # 경기수
            #Sp = item.find_elements(By.CSS_SELECTOR, 'td:nth-child(25)').text  # 선발
            Inning = item.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text  # 이닝
            #hit = item.find_element(By.CSS_SELECTOR, 'td:nth-child(19)').text  # 피안타
            #BB = item.find_element(By.CSS_SELECTOR, 'td:nth-child(10)').text  # 피볼넷
            #Dead_Ball = item.find_element(By.CSS_SELECTOR, 'td:nth-child(11)').text  # 사구
            #SO = item.find_element(By.CSS_SELECTOR, 'td:nth-child(12)').text  # 삼진
            #Wild_pitch = item.find_element(By.CSS_SELECTOR, 'td:nth-child(17)').text  # 폭투
            #BLK = item.find_element(By.CSS_SELECTOR, 'td:nth-child(15)').text  # 보크
            avg = item.find_element(By.CSS_SELECTOR, 'td:nth-child(19)').text  # 피안타율
            obp = item.find_element(By.CSS_SELECTOR, 'td:nth-child(20)').text  # 피출루율

            # doc = {
            #     'name': name, 'position': position, 'G': G, 'Inning': Inning,
            #     'avg': avg, 'obp': obp, 'year': year, 'team': team
            # }
            data[year].append({
                'name': name, 'team': team, 'position': position, 'G': G, 'Inning': Inning,
                'avg': avg, 'obp': obp, 'year': year, 'team': team
            })

            print(year, team, name, '저장 완료')

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

driver.quit()