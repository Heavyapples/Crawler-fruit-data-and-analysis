import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException

def write_to_csv(data):
    with open("fruit_data.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # 根据实际情况修改此路径
firefox_options = FirefoxOptions()
firefox_options.binary_location = firefox_binary_path

firefox_service = FirefoxService(executable_path="D:\\geckodriver\\geckodriver.exe")
driver = webdriver.Firefox(options=firefox_options, service=firefox_service)

url = "http://www.wbncp.com/?m=home&c=Lists&a=index&tid=69"
driver.get(url)

# 等待用户操作
input("请在网页中进行操作，完成后按回车键继续：")

if not os.path.isfile("fruit_data.csv"):
    with open("fruit_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["品名", "产地", "最高价", "最低价", "均价", "日期"])

while True:
    # 获取表格数据
    data_rows = driver.find_elements("css selector", "tbody.ivu-table-tbody > tr")

    for row in data_rows:
        product_name = row.find_element("css selector", "td:nth-child(2) span").text
        origin = row.find_element("css selector", "td:nth-child(3) span").text
        highest_price = row.find_element("css selector", "td:nth-child(6) span").text
        lowest_price = row.find_element("css selector", "td:nth-child(7) span").text
        average_price = row.find_element("css selector", "td:nth-child(8) span").text
        date = row.find_element("css selector", "td:nth-child(9) span").text

        write_to_csv([product_name, origin, highest_price, lowest_price, average_price, date])

    # 尝试找到并点击下一页按钮
    try:
        next_page_button = driver.find_element("css selector", "li.ivu-page-next a")
        next_page_button.click()
        time.sleep(3)  # 等待页面加载完成
    except NoSuchElementException:
        break  # 没有下一页时退出循环

driver.quit()
