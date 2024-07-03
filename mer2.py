import re
from numpy import average
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime
import csv
import traceback


def situ_check(situ):
    if situ=="新品、未使用":
        return 6
    elif situ=="未使用に近い":
        return 5
    elif situ=="目立った傷や汚れなし":
        return 4
    elif situ=="やや傷や汚れあり":
        return 3
    elif situ=="傷や汚れあり":
        return 2
    elif situ=="全体的に状態が悪い":
        return 1
    else:
        return 0



def get_url(KEYWORD,browser):
    item_url_ls=[]
    page = 1
    count = 1
    #売り切れ表示
    url_ini = 'https://jp.mercari.com/search?keyword=' + KEYWORD + '&status=sold_out%7Ctrading'
    url=url_ini

    while page < 2:
        try:
            browser.get(url)
            browser.implicitly_wait(5)
            #商品の詳細ページのURLを取得する
            item_box = browser.find_elements(By.CSS_SELECTOR,'#item-grid > ul > li') #これで多分url取れた
            if len(item_box) != 0:
                for item_elem in item_box:
                    item_url_ls.append(item_elem.find_element(By.XPATH, '//div/a').get_attribute('href'))
                    count+=1
            else:
                break
            #next_pageの取得
            try:
                next_page=browser.find_elements(By.CSS_SELECTOR,'#search-result > div > div > div > div.Pagination__PaginationControlsContainer-sc-17at9ov-0.jHAXvG.mer-spacing-t-32 > mer-button')
                if len(next_page) != 0:
                    page+=1
                    param='&page_token=v1%3A'+str(page)
                    next_url=url_ini+param
                    url=next_url
                    next_url=''
                else:
                    break
            except:
                break
        except:
            message=traceback.print_exc()
            print(message)

    print(len(item_url_ls))
    return item_url_ls


def get_data(KEYWORD,item_url_ls,browser):
    item_ls = []

    #商品情報の詳細を取得する
    for item_url in item_url_ls:
        browser.get(item_url)
        time.sleep(2) #サーバーに処理
        #値段
        if (price_shadow := browser.find_elements(By.CSS_SELECTOR,'#item-info > section:nth-child(1) > section:nth-child(2) > div > div > div > span:nth-child(2)')) == []:
            price_shadow=browser.find_element(By.CSS_SELECTOR,'#product-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)').text
        else:
            price_shadow=browser.find_element(By.CSS_SELECTOR,'#item-info > section:nth-child(1) > section:nth-child(2) > div > div > div > span:nth-child(2)').text

        #商品の状態
        # situ_shadow=browser.find_element(By.CSS_SELECTOR,'#item-info > section.layout__StyledSection-sc-1lyi7xi-7.kdAFPN > div > mer-display-row:nth-child(3)').shadow_root
        situ=browser.find_element(By.CSS_SELECTOR,'#item-info > section.sc-8251d49d-7.gWvqlX > div.sc-4bd02274-0.fmFHWs > div:nth-child(2) > div.body__32cba457 > span').text#'#item-info > section.layout__Section-sc-1lyi7xi-7.BycTx > div > mer-display-row:nth-child(2) > span:nth-child(2)').text
        situ_num=situ_check(situ)
        numbers = re.sub(r'[^0-9]', '', price_shadow)
        data=[int(numbers),situ_num]
        item_ls.append(data)
    return item_ls


def main():
    item_url_ls=[]
    item_ls=[]
    #ブラウザの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #ブラウザの起動
    browser = webdriver.Chrome()#r"C:\Users\81809\Downloads\chromedriver_win32 (1)\chromedriver.exe",options=options)
    browser.implicitly_wait(3)
    #キーワード設定
    KEYWORD = input("キーワードを入力してください:")
    csv_date = datetime.datetime.today().strftime("%Y%m%d")
    csv_file_name = KEYWORD +'_'+ csv_date + '.csv'
    item_url_ls=get_url(KEYWORD,browser)
    item_ls=get_data(KEYWORD,item_url_ls,browser)
    print(item_ls)
    pd.DataFrame(item_ls).to_csv(csv_file_name)

if __name__ == '__main__':
    main()