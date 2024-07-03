from ast import keyword
from sklearn.linear_model import LinearRegression, Ridge, Lasso
# from sklearn.datasets import load_boston
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
from mer2 import get_url, get_data
# %matplotlib inline
sns.set()

item_url=[]
item_url_ls=[]
Scaler=StandardScaler()
Scaler1 = StandardScaler()
keyword=input('キーワードを入力してください：')
# boston = load_boston()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)#r"C:\Users\81809\Downloads\chromedriver_win32\chromedriver.exe",options=options)
item_url_ls=get_url(keyword,browser)
item_ls=get_data(keyword,item_url_ls,browser)
# california_housing = fetch_california_housing()
# X, y = california_housing.data, california_housing.target
X=[[r[1]] for r in item_ls] #定価とランクのリスト(関係性)
y=[[r[0]] for r in item_ls]
print(X)
print(y)
# y = y.reshape(-1, 1)
X = Scaler.fit_transform(X)
# print(X)
# print(y)
y = Scaler1.fit_transform(y)
# y.reshape(-1, 1)
# print(type(X))
# print(len(X))
# print(type(y))
# print(len(y))
train_X=X[:int(len(X)*0.8)]
train_y=y[:int(len(y)*0.8)]
test_X=X[int(len(X)*0.8):]
test_y=y[int(len(y)*0.8):]
clf1 = LinearRegression().fit(train_X, train_y)
clf2 = Ridge(alpha=10).fit(train_X, train_y)
clf3 = Ridge(alpha=100).fit(train_X, train_y)
result1 = clf1.predict(test_X)
result1 = result1.reshape(-1,1)
# print(result1)
# result1 = Scaler.inverse_transform(result1)#xを使って標準化したもの戻す
result2 = clf2.predict(test_X)
result3 = clf3.predict(test_X)
# print(y)
# print(result1)
print(r2_score(result1,test_y))  #適合率　グラフがどれくらい重なっているか 0.75~0.8を超えれば使える。
# plt.plot(clf1.coef_, label='alpha=0', color='r', linestyle=':') #coef_・・・変回帰変数
# plt.plot(clf2.coef_, label='alpha=10', color='g', linestyle='-.')
# plt.plot(clf3.coef_, label='alpha=100', color='b', linestyle='--')
plt.scatter(result1,test_y)
plt.xlabel('Features', fontsize=12)
plt.ylabel('Coefficient', fontsize=12)
plt.legend()
plt.show()