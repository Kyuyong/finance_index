import telegram
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import pyupbit

now_month = datetime.now().strftime('%m')
now_day = datetime.now().strftime('%d')
days = ['월','화','수','목','금','토','일','월']
days_select = datetime.today().weekday()
work_title = now_month+"."+now_day+"("+days[days_select]+")"+" 경제지표"

def naver_search(keyword):
    search_url = 'https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&query={}'
    url = search_url.format(keyword)
    
    return url

def soup_func(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    return soup 

## 코스피 ###
def kospi_func(soup):
    kospi = soup.find("div",class_="main-current-data").find_all("span")[0].text
    kospi_per = soup.find("div",class_="main-current-data").find_all("span")[3].text

    return kospi,kospi_per

## 코스닥 ###
def kosdaq_func(soup):
    kosdaq = soup.find("div",class_="main-current-data").find_all("span")[0].text
    kosdaq_per = soup.find("div",class_="main-current-data").find_all("span")[3].text

    return  kosdaq, kosdaq_per

## 환전 고시 ###
def usd_func(soup):
    usd = soup.find("div",class_="main-current-data").find_all("span")[0].text
    usd_per = soup.find("div",class_="main-current-data").find_all("span")[3].text
    
    return usd, usd_per


## 유가 ###
def oil_func(soup):
    oil = soup.find("div",class_="main-current-data").find_all("span")[0].text
    oil_per = soup.find("div",class_="main-current-data").find_all("span")[3].text
    
    return oil, oil_per

## 금시세 ###
def gold_func(soup):
    gold = soup.find("div",class_="main-current-data").find_all("span")[0].text
    gold_per = soup.find("div",class_="main-current-data").find_all("span")[3].text
    
    return gold, gold_per


## 미국채 10년물 금릴 ###
def usa_debt_func(soup):
    usa_debt_name = soup.find("div", class_="finance_info").find("div", class_="cm_tap_area").find("div", class_="select_tab").find("span", class_="menu").text
    usa_debt_money = soup.find("div", class_="finance_info").find("div", class_="top_info up").find("strong").text
    usa_debt_per = soup.find("div", class_="finance_info").find("div", class_="top_info up").find("span").text
    
    return usa_debt_name, usa_debt_money, usa_debt_per


if __name__ == "__main__":
    
    kospi = kospi_func(soup_func('https://kr.investing.com/indices/kospi'))
    kosdaq = kosdaq_func(soup_func('https://kr.investing.com/indices/kosdaq'))
    usd = usd_func(soup_func("https://kr.investing.com/currencies/usd-krw"))
    oil = oil_func(soup_func('https://kr.investing.com/commodities/crude-oil'))
    gold = gold_func(soup_func("https://kr.investing.com/commodities/gold"))
    
    keyword = "미국채 10년물 금리"
    usa_debt_url = naver_search(keyword)
    usa_debt = usa_debt_func(soup_func(usa_debt_url))

    bitcoin = "비트코인: "+"{0:>10,}원".format(int(pyupbit.get_current_price("KRW-BTC")))
    
    
    send_text = work_title+"\n"+"="*20+"\n"+"코스피 : "+kospi[0]+" "+kospi[1]+"\n"+\
        "코스닥: "+kosdaq[0]+" "+kosdaq[1]+"\n"+\
        "\n"+"USD 환율: "+usd[0]+" "+usd[1]+"\n"+\
        "오일: "+oil[0]+" "+oil[1]+"\n"+\
        "금: "+gold[0]+" "+gold[1]+"\n"+\
        "\n"+usa_debt[0]+": "+usa_debt[1] +"\n"+bitcoin

   
    
    ### 정인 Chat-id 텔레그램 보내기     
    my_token = 'token' ## mvpcouple token
    bot = telegram.Bot(token= my_token)  
    id = 'chat_id'  ##neos 개인 chatid    
    
    bot.sendMessage(chat_id=id, text=send_text)



