from flask import Flask, render_template, request, flash, session
from bp.chatbot import chatbot_bp
from bp.dictionary import dictionary_bp
from bp.mapapi import mapapi_bp
from bp.fraud import fraud_bp
import os, random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
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

def get_naver_news_title():
    url = 'https://land.naver.com/news/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    naver_newstitle = soup.select_one('.group .news_list dt span').get_text()
    news_title_tag = soup.select_one('.group .news_list dt a')
    news_url = news_title_tag['href']
    news_publisher = soup.select_one('.group>.news_list>dd>.writing').get_text()
    return naver_newstitle, news_url, news_publisher



@app.route('/get_news_title')
def get_news_title():
    news_title, news_url, news_publisher = get_naver_news_title()
    return {'news_title': news_title, 'news_url': 'https://land.naver.com/' + news_url, 'news_publisher': news_publisher}

def inject_news_title():
    news_title = get_naver_news_title()
    return dict(news_title=news_title)

def get_naver_news_titles():
    url = 'https://land.naver.com/news/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    newstitle_list = soup.select('.group2>ul>li')
    
    news_data = []
    for nl in newstitle_list[:5]:  # 리스트의 첫 5개 항목만 처리
        nl_title = nl.select_one('span').get_text(strip=True)
        nl_url = 'https://land.naver.com/' + nl.select_one('span>a')['href']
        nl_publisher = nl.select_one('.writing').get_text(strip=True)
        
        news_data.append({
            'title': nl_title,
            'url': nl_url,
            'publisher': nl_publisher
        })
        
    return news_data

@app.route('/get_news_titles')
def get_news_titles():
    news_titles = get_naver_news_titles()
    return {'news_titles': news_titles}



if __name__ == '__main__':
    app.run(debug=True)