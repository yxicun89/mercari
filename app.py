from flask import Flask, render_template, request
import re
from numpy import average
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
import time
import pandas as pd
import datetime
from mer2 import get_url, get_data

item_url_ls=[]
item_ls=[]
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/calc",methods=['GET','POST'])
def calculation():
    if request.method == "GET":
        chart_exist=False
        return render_template('calculation.html',chart_exist=chart_exist)
    elif request.method == "POST":
        #ブラウザの設定
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #ブラウザの起動
        browser = webdriver.Chrome(r"C:\Users\81809\Downloads\chromedriver_win32 (1)\chromedriver.exe",options=options)
        browser.implicitly_wait(3)
        keyword = request.form['keyword'] 
        item_url_ls=get_url(keyword,browser)
        item_ls=get_data(keyword,item_url_ls,browser)
        item_x=[r[1] for r in item_ls]
        item_y=[r[0] for r in item_ls]
        chart_exist=True
        return render_template('calculation.html',chart_exist=chart_exist,item_x=item_x,item_y=item_y)
        
if __name__ == "__main__":
    app.run(debug=True)