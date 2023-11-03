from flask import Flask, render_template
from bp.chatbot import chatbot_bp
from bp.dictionary import dictionary_bp
from bp.mapapi import mapapi_bp
from bp.fraud import fraud_bp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'


app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(dictionary_bp, url_prefix='/dictionary')
app.register_blueprint(fraud_bp, url_prefix='/fraud')
app.register_blueprint(mapapi_bp, url_prefix='/mapapi')





@app.route('/')
def home():
    menu = {'ho':1, 'ol':0, 'ba':0, 'fr':0, 'mp':0 }
    #flash('Welcome to my Web!!!')
    return render_template('home.html', menu=menu)

##################################################



def get_naver_news_titles():
    url = 'https://land.naver.com/news/headline.naver'
    
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드 활성화
    options.add_argument("--disable-gpu")  # GPU 사용 안 함
    options.add_argument("--window-size=1920x1080")  # 창 크기 설정
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안 함
    options.add_argument("--no-sandbox")  # Sandbox 모드 비활성화
    options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # WebDriverWait를 사용하여 뉴스 항목이 로드될 때까지 최대 10초간 기다립니다.
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.land_news_list > li')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_items = soup.select('.land_news_list > li')[:5]

    news_data = []

    for news_item in news_items:
        title = news_item.select_one('.title').get_text(strip=True)
        publisher = news_item.select_one('.description.source').get_text(strip=True)
        link = news_item.select_one('a')['href']
        
        news_data.append({
            'title': title,
            'publisher': publisher,
            'url': link
        })
        
    # 크롤링 결과를 출력합니다.
    for news in news_data:
        print("Title:", news['title'])
        print("Publisher:", news['publisher'])
        print("URL:", news['url'])
        print()
        
    driver.quit()
    return news_data

@app.route('/get_news_titles')
def get_news_titles():
    news_titles = get_naver_news_titles()
    return {'news_titles': news_titles}

if __name__ == '__main__':
    app.run(host='192.168.0.66', debug=True)