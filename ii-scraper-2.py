import config
from selenium import webdriver
import pickle
import time
import datetime
import pandas as pd
from pandas import DataFrame

def scrape1(url):
    driver.get(url)
    time.sleep(sleep_time)
    print("scraping",url)

    #Expand recommendations table to show maximum number of results on single page
    results_dropdown = driver.find_element_by_xpath('//button[contains(@class, "btn btn-default dropdown-toggle ng-binding")]')
    results_dropdown.click()
    results_dropdown_250 = driver.find_element_by_xpath('//ul[contains(@class, "dropdown-menu")]/li[contains(@class, "ng-scope")][5]/a[contains(@class, "ng-binding")]')
    results_dropdown_250.click()

    #Read data in table

    field_xpath = '//*[@id="DataTables_Table_0"]/tbody/tr[{0}]/td[{1}]'

    table_length = len(driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]').text.split('\n'))
    table_length -=1
    table_length /=2
    #print('table_length=',table_length)

    #iterate over companies
    for i in range(1,int(table_length+1)):
        data.append([])
        #iterate over fields
        for j in range(1,8):
            field=driver.find_element_by_xpath(field_xpath.format(i,j))
            text=field.text
            data[-1].append(text)
            #scrape URL for company overview
            if j==2:
                link=field.find_element_by_css_selector('a').get_attribute('href')
                data[-1].append(link)
        #print(data[-1])


def scrape2(url,j):
    driver.get(url)
    time.sleep(sleep_time)
    print("scraping",url)

    #Get Ticker
    title_xpath = "//h1[@class='page-title']"
    try:
        ticker = driver.find_element_by_xpath(title_xpath).text[-4:-1]
        data[j].append(ticker)
    except Exception as e:
        print(e)
        data[j].append('N/A')

    #Get Price Guides ("limits")
    limit_types=["buy","hold","sell"]
    limits={}
    for i in limit_types:
        limit_xpath = "//li[@class='guide-item guide-{0}']/span[@class='guide-limit']"
        try:
            limit_field = driver.find_element_by_xpath(limit_xpath.format(i))
            data[j].append(limit_field.text.split(' ')[-1])
        except Exception as e:
            print(e)
            data[j].append('N/A')

    #Get Risk Guides
    #'Max Portfolio Weighting','Business Risk','Share Price Risk'
    risks={}
    for i in range(3,6):
        risk_xpath = "//li[@class='company-overview-item'][{0}]/span[@class='company-overview-value']"
        try:
            risk_field = driver.find_element_by_xpath(risk_xpath.format(i))
            data[j].append(risk_field.text)
        except Exception as e:
            print(e)
            data[j].append('N/A')


def scrape3(ticker,j):
    driver.get("https://www.marketindex.com.au/asx/"+ticker)
    time.sleep(sleep_time)
    print("scraping","https://www.marketindex.com.au/asx/"+ticker)

    try:
        price = driver.find_element_by_xpath("""//*[@id="taxonomy-term-1"]/div[2]/div[1]/div[1]/p[1]""").text
        updated = driver.find_element_by_xpath("""//*[@id="taxonomy-term-1"]/div[2]/div[1]/div[1]/p[2]""").text
        change = driver.find_element_by_xpath("""//*[@id="taxonomy-term-1"]/div[2]/div[1]/div[2]/p[1]/span[2]""").text
        change_percent = driver.find_element_by_xpath("""//*[@id="taxonomy-term-1"]/div[2]/div[1]/div[2]/p[1]/span[3]""").text[1:-1]

        data[j].append(price)
        data[j].append(updated)
        data[j].append(change)
        data[j].append(change_percent)

    except Exception as e:
        data[j].append("N/A")
        data[j].append("N/A")
        data[j].append("N/A")
        data[j].append("N/A")


def timestamp():
    y=str(datetime.datetime.now().year)
    mo=str(datetime.datetime.now().month)
    d=str(datetime.datetime.now().day)
    h=str(datetime.datetime.now().hour)
    m=str(datetime.datetime.now().minute)
    s=str(datetime.datetime.now().second)
    return y+"-"+mo+"-"+d+" "+h+":"+m+":"+s

def generate_filename():
    #generates a filename based on todays date
    import datetime
    date = datetime.datetime.now()
    if len(str(date.day)) == 1:
        day_str = "0"+str(date.day)
    else:
        day_str = str(date.day)
    if len(str(date.month)) == 1:
        month_str = "0"+str(date.month)
    else:
        month_str = str(date.month)  
    return str(date.year)+month_str+day_str

def export_to_excel():
    data_dict = {}
    for i in range(len(column_titles)):
        data_dict[column_titles[i]]=[data[j][i] for j in range(len(data))]

    df=DataFrame(data_dict)

    currentPrices = df["07. Current Price"]
    buyBelows = df["09. Buy Below"]
    sellAboves = df["11. Sell Above"]

    extraBuyMargin = []
    for i in range(len(data)):
        try:
            buyBelow = float(buyBelows[i])
            currentPrice = float(currentPrices[i][1:])
            extraBuyMargin.append( ( buyBelow - currentPrice ) / buyBelow )
        except Exception as e:
            extraBuyMargin.append("N/A")
    print("extraBuyMargin:",extraBuyMargin)

    extraSellMargin = []
    for i in range(len(data)):
        try:
            sellAbove = float(sellAboves[i])
            currentPrice = float(currentPrices[i][1:])
            extraSellMargin.append( ( currentPrice - sellAbove ) / sellAbove )
        except Exception as e:
            extraSellMargin.append("N/A")
    print("extraSellMargin:",extraSellMargin)

    df["99.0 Extra BUY margin"] = extraBuyMargin
    df["99.1 Extra SELL margin"] = extraSellMargin

    writer = pd.ExcelWriter(generate_filename()+".xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name=generate_filename(), index=False)
    writer.save()
    print("Data saved to "+generate_filename()+".xlsx")

#Global variables
sleep_time=2 #increase for full automation!!!
data = []
column_titles=['Recommendation',
         'Company',
         'URL',
         'Industry',
         'Analyst',
         'Review Date',
         'Review Price',
         'Current Price',
         'Ticker',
         'Buy Below',
         'Hold Up To',
         'Sell Above',
         'Business Risk',
         'Share Price Risk',
         'Max Portfolio Weighting']

#Add 2-digit number to each column title
for i in range(len(column_titles)):
    if len(str(i))==1:
        column_titles[i]='0'+str(i)+'. '+column_titles[i]
    else:
        column_titles[i]=str(i)+'. '+column_titles[i]

#Print configurations
print("*** II-Scraper Version 2 ***")
print("\n")
print("Configuration settings:")
print("\tDEV_MODE =", config.DEV_MODE)
print("\tLOAD_PICKLE_NAME =", config.LOAD_PICKLE_NAME)
print("\tSAVE_PICKLE =", config.SAVE_PICKLE)
print("\tSAVE_PICKLE_NAME =", config.SAVE_PICKLE_NAME)
print("\n")

#Load existing file - useful for development and testing
if config.DEV_MODE:
    #Load data from pickle file
    print("Loading data from",config.LOAD_PICKLE_NAME,"...")
    data=pickle.load(open(config.LOAD_PICKLE_NAME,"rb"))
    print("Data for",len(data),"companies successfully loaded.\n")

else:
    #Start driver
    driver = webdriver.Chrome(config.DRIVER_LOCATION)

    #Login to website and start scraping sequence
    driver.get("https://www.intelligentinvestor.com.au/user")
    time.sleep(sleep_time)
    print("Time: ",timestamp())
    print("Logging in...")
    username=config.KEYS["username"]
    pwd=config.KEYS["password"]

    username_field = driver.find_element_by_xpath('//input[@id="Email"]')
    username_field.click()
    username_field.send_keys(username)
    
    pwd_field = driver.find_element_by_xpath('//input[@id="Password"]')
    pwd_field.click()
    pwd_field.send_keys(pwd)
    
    login_btn = driver.find_element_by_xpath('//input[contains(@class, "btn btn-primary btn-fw btn-brand-style-with-pad")]')
    login_btn.click()
    time.sleep(sleep_time)
    print("\nFinished: ",timestamp())

    #Scrape URL list for all companies covered if no data pre-loaded
    all_recommendations_url='https://www.intelligentinvestor.com.au/research/recommendations'
    print("\nTime: ",timestamp())
    print("Scraping Intelligent Investor Reccommendations...")    
    scrape1(all_recommendations_url)
    print("\nFinished: ",timestamp())

    #Scrape price and risk guides for each company
    print("\nTime: ",timestamp())
    print("Scraping Intelligent Investor Price and Risk Guides...")

    url_list=[i[2] for i in data]
    j=0
    for url in url_list:
        scrape2(url,j)
        j+=1
    print("\nFinished: ",timestamp())

#Export to .CSV spreadsheet
export_to_excel()

#Save memory state to pickle file
if config.SAVE_PICKLE:
    pickle.dump(data,open(config.SAVE_PICKLE_NAME,"wb"))



