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

def soup_func(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    return soup 

def investing_func(soup):
    value = soup.find("div",class_="main-current-data").find_all("span")[0].text
    percentage = soup.find("div",class_="main-current-data").find_all("span")[3].text
        
    return value, percentage



if __name__ == "__main__":
    
    kospi = investing_func(soup_func('https://kr.investing.com/indices/kospi'))
    kosdaq = investing_func(soup_func('https://kr.investing.com/indices/kosdaq'))
    usd = investing_func(soup_func("https://kr.investing.com/currencies/usd-krw"))
    oil = investing_func(soup_func('https://kr.investing.com/commodities/crude-oil'))
    gold = investing_func(soup_func("https://kr.investing.com/commodities/gold"))
    usa_debt = investing_func(soup_func("https://kr.investing.com/rates-bonds/u.s.-10-year-bond-yield"))  
    bitcoin = "비트코인: "+"{0:>10,}원".format(int(pyupbit.get_current_price("KRW-BTC")))
    
    ### 텔레그램 메세지 
    send_text = work_title+"\n"+"="*20+"\n"+"코스피 : "+kospi[0]+" "+kospi[1]+"\n"+\
        "코스닥: "+kosdaq[0]+" "+kosdaq[1]+"\n"+\
        "\n"+"USD 환율: "+usd[0]+" "+usd[1]+"\n"+\
        "오일: "+oil[0]+" "+oil[1]+"\n"+\
        "금: "+gold[0]+" "+gold[1]+"\n"+\
        "\n미국채 10년: "+usa_debt[0]+" "+usa_debt[1] +"\n"+bitcoin
   

    my_token = 'token' ##
    bot = telegram.Bot(token= my_token)  
    id = 'chat_id'  ##  
    
    bot.sendMessage(chat_id=id, text=send_text)



