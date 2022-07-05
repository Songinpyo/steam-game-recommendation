from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

driver = webdriver.Chrome(executable_path=r"C:\Users\rihot\Desktop\Deep_learning\steam_recommend\chromedriver.exe")
URL = "https://store.steampowered.com/search/?filter=topsellers"
driver.get(URL)
time.sleep(1)

filter = driver.find_element(By.XPATH, '//*[@id="additional_search_options"]/div[3]/div[1]').click()
games = driver.find_element(By.XPATH, '//*[@id="narrow_category1"]/div[1]/span').click()
time.sleep(1)

f = open("./steam_games_information.csv", "w", newline='', encoding="utf-8-sig")
wtr = csv.writer(f)
wtr.writerow(['game', 'rate', 'genre', 'review1','tag1', 'tag2', 'tag3', 'tag4', 'tag5'])

for i in range(50):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down
    time.sleep(0.5)

for i in range(1, 501):
    try:
        game = driver.find_element(By.XPATH, f'//*[@id="search_resultsRows"]/a[{i}]')
        link = game.get_attribute("href")

        driver.execute_script('window.open("https://google.com");')  # 구글 창 새 탭으로 열기
        time.sleep(1)

        driver.switch_to.window(driver.window_handles[-1])  # 새로 연 탭으로 이동
        driver.get(link)
        time.sleep(3)

        title = driver.find_element(By.XPATH, '//*[@id="appHubAppName"]').text
        recentrating = driver.find_element(By.XPATH, '//*[@id="userReviews"]/div/div[2]').text
        if recentrating == "No user reviews":
            rate = "none"
        else:
            ratings = driver.find_element(By.XPATH, '//*[@id="userReviews"]/div[2]/div[2]/meta[2]')
            rate = ratings.get_attribute('content')

        genre = driver.find_element(By.XPATH, '//*[@id="tabletGrid"]/div[1]/div[2]/div[1]/div[1]/a[2]').text

        tag1 = driver.find_element(By.XPATH, '//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a[1]').text
        tag2 = driver.find_element(By.XPATH, '//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a[2]').text
        tag3 = driver.find_element(By.XPATH, '//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a[3]').text
        tag4 = driver.find_element(By.XPATH, '//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a[4]').text
        tag5 = driver.find_element(By.XPATH, '//*[@id="glanceCtnResponsiveRight"]/div[2]/div[2]/a[5]').text
        wtr.writerow([title, rate, genre, tag1, tag2, tag3, tag4, tag5])

        driver.close()  # 링크 이동 후 탭 닫기
        driver.switch_to.window(driver.window_handles[-1])  # 다시 이전 창(탭)으로 이동
        time.sleep(2)
    except:
        pass

time.sleep(1)

driver.close()

f.close()