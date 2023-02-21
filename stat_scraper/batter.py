from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

file_path = './batter.json'

data = {}

driver = webdriver.Chrome()

# 연도범위 동안 팀리스트 스크래핑 후 DB에 저장
yearScope = range(1982, 2023)
team_List = ['SK', 'SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', 'kt', '히어로즈', '두산', '해태', '현대', '청보',
             '삼미', 'MBC', 'OB', '태평양', '빙그레', '쌍방울']

for year in yearScope:
    data[year] = []
    for team in team_List:
        url = 'http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys=%d&ye=%d&se=0&te=%s' \
              '&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1' \
              '&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=' % (year, year, team)
        driver.get(url)
        trs = driver.find_elements(By.CSS_SELECTOR, '#mytable > tbody > tr')
        for index, item in enumerate(trs):
            if len(item.text) <= 5:
                continue
            if item.find_elements(By.CSS_SELECTOR, 'th'):
                continue
            try:
                if item.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span > span:nth-child(3)').text == 'P':
                    print('found P, pass')
                    continue
            except NoSuchElementException:
                print('position not found')
                continue
            name = item.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text  # 선수명
            position = item.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span > span:nth-child(3)').text # 포지션
            avg = item.find_element(By.CSS_SELECTOR, 'td:nth-child(24)').text  # 타율
            obp = item.find_element(By.CSS_SELECTOR, 'td:nth-child(25)').text  # 출루율
            slg = item.find_element(By.CSS_SELECTOR, 'td:nth-child(26)').text  # 장타율
            total_hit = item.find_element(By.CSS_SELECTOR, 'td:nth-child(9)').text  # 안타
            double_hit = item.find_element(By.CSS_SELECTOR, 'td:nth-child(10)').text  # 2루타
            triple_hit = item.find_element(By.CSS_SELECTOR, 'td:nth-child(11)').text  # 3루타
            home_run = item.find_element(By.CSS_SELECTOR, 'td:nth-child(12)').text  # 홈런
            BB = item.find_element(By.CSS_SELECTOR, 'td:nth-child(17)').text  # 볼넷
            SB = item.find_element(By.CSS_SELECTOR, 'td:nth-child(15)').text  # 도루
            Dead_Ball = item.find_element(By.CSS_SELECTOR, 'td:nth-child(18)').text  # 사구
            one_hit = int(total_hit) - int(double_hit) - int(triple_hit) - int(home_run)  # 1루타

            doc = {
                'name': name, 'position': position, 'avg': avg, 'obp': obp, 'slg': slg, 'total_hit': total_hit,
                'double_hit': double_hit, 'triple_hit': triple_hit, 'home_run': home_run, 'BB': BB, 'SB': SB,
                'Dead_Ball': Dead_Ball, 'one_hit': one_hit, 'year': year, 'team': team
            }
            data[year].append({
                'name': name, 'team': team, 'position': position, 'avg': avg, 'obp': obp, 'slg': slg, 'total_hit': total_hit,
                'double_hit': double_hit, 'triple_hit': triple_hit, 'home_run': home_run, 'BB': BB, 'SB': SB,
                'Dead_Ball': Dead_Ball, 'one_hit': one_hit,
            })
            
            print(year, team, name, '저장 완료')

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

driver.quit()