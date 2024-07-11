import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import collections

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def company_name(driver):
    driver.get('https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_brief.php?code=20')
    company_name = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[1]/div[3]/div[1]/table/tbody/tr[1]/td[3]').text
    return company_name
def financial_year(driver):
    driver.get("https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_ratio.php?code=20")
    finan_ratio_table = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[1]/div[3]/div[2]/div[2]")
    financial_year = driver.find_element(By.CSS_SELECTOR,".figureTable").text
    financial_year_list = financial_year.split("\n")
    return financial_year_list

def financial_ratio(driver, financial_year_list, company_name):
    driver.get("https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_ratio.php?code=20")
    finan_ratio_table = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[1]/div[3]/div[2]/div[2]")
    master = []
    for index,financial_stat_table in enumerate(finan_ratio_table.find_elements(By.CSS_SELECTOR,".figureTable")):
        if index == 0:
            continue
        for financial_stat_row in financial_stat_table.find_elements(By.TAG_NAME, "tr"):
            financial_stat_row = financial_stat_row.text.replace(" / ","")
            for year_index,financial_stat_each in enumerate(financial_stat_row.split(" ")[2:]):
                dict={
                    "公司": company_name,
                    "財政年度": financial_year_list[year_index],
                    f"{financial_stat_row.split(" ")[0]}": financial_stat_each.replace(",","")
                }
                master.append(dict)
    super_master = []
    for year in financial_year_list:
        dict = {}
        for data in master:
            if data['財政年度'] == year:
                dict.update(data)
        super_master.append(dict)
    pd.DataFrame(super_master).to_csv("./data_source/財務比率.csv",index = False)

def balance_sheet(driver,financial_year_list, company_name):
    driver.get("https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_pl.php?code=20")
    balance_sheet_table = driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div[4]/div[1]/div[3]/div[2]/div[3]/table/tbody")
    master = []
    for row in balance_sheet_table.find_elements(By.TAG_NAME, "tr")[1:]:
        if len(row.text) <= 10:
            continue
        row_data_list = row.text.replace(" / ", "/").replace("--", "N/A").split(" ")
        del row_data_list[2]
        for index, element in enumerate(row_data_list[1:]):
            dict = {
                "公司": company_name,
                "財政年度": financial_year_list[index],
                f"{row_data_list[0]}": element.replace('"', '').strip("()").replace(',', '')
            }
            master.append(dict)
    super_master = []
    for year in financial_year_list:
        dict = {}
        for data in master:
            if data['財政年度'] == year:
                dict.update(data)
        super_master.append(dict)
    pd.DataFrame(super_master).to_csv("./data_source/損益表.csv",index = False)

def financial_situation(driver, financial_year_list, company_name):
    driver.get("https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_bs.php?code=20")
    financial_situation = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[1]/div[3]/div[2]/div[3]")
    master = []
    for row in financial_situation.find_elements(By.TAG_NAME, "tr")[1:]:
        row_data_list = row.text.replace(" / ", "/").replace("--", "N/A").split(" ")
        if len(row.text) <= 10 or "," in row_data_list[0] or len(row_data_list[0]) < 2:
            continue
        print(row_data_list)
        del row_data_list[2]
        for index, element in enumerate(row_data_list[1:]):
            dict = {
                "公司": company_name,
                "財政年度": financial_year_list[index],
                f"{row_data_list[0]}": element.replace('"', '').strip("()").replace(",","")
            }
            print(element.replace('"', '').strip("()").replace(",",""))
            master.append(dict)
    super_master = []
    for year in financial_year_list:
        dict = {}
        for data in master:
            if data['財政年度'] == year:
                dict.update(data)
        super_master.append(dict)
    pd.DataFrame(super_master).to_csv("./data_source/財務狀況.csv",index = False)

def cash_flow(driver, financial_year_list, company_name):
    driver.get('https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_cashflow.php?code=20')
    cash_flow_table = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[3]/div[2]/div[3]/table/tbody")
    master = []
    for row in cash_flow_table.find_elements(By.TAG_NAME, "tr")[1:]:
        row_data_list = row.text.replace(" / ", "/").replace("--", "N/A").split(" ")
        if len(row.text) <= 10 or "," in row_data_list[0] or len(row_data_list[0]) < 2:
            continue
        for index, element in enumerate(row_data_list[1:]):
            dict = {
                "公司": company_name,
                "財政年度": financial_year_list[index],
                f"{row_data_list[0]}": element.replace("(","").replace(")","").replace(",","")
            }
            master.append(dict)
    super_master = []
    for year in financial_year_list:
        dict = {}
        for data in master:
            if data['財政年度'] == year:
                dict.update(data)
        super_master.append(dict)
    pd.DataFrame(super_master).to_csv("./data_source/現金流量表.csv",index = False)

company_name = company_name(driver)
# financial_year_list = financial_year(driver)
# financial_ratio(driver, financial_year_list, company_name)
# financial_situation(driver, financial_year_list, company_name)
# balance_sheet(driver, financial_year_list, company_name)
# cash_flow(driver,financial_year_list, company_name)
