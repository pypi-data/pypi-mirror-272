import argparse
import sys
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from time import sleep
from pathlib import Path

EXPERTS_URL = "https://www.zacks.com/registration/ultimatetrader/welcome/eoffer/3393/?t="
headers = {'User-Agent': 'Mozilla/5.0'}
NEGATIVE = "At any given time"
DRIVER_PATH = Path.home().joinpath("geckodriver")

def args_handle():
    parser = argparse.ArgumentParser()
    # add long and short argument for the stock file
    parser.add_argument('-i', '--input', default=open("stock_list.txt", "r"), type=argparse.FileType('r'), help='input stock list name (default: stock_list.txt)')
    # add l, s for output file
    parser.add_argument('-o', '--output', default=sys.stdout, type=argparse.FileType('w'), help='output file name (default: stdout)')
    # add argument that shows negative picks
    parser.add_argument('-n', '--negative', default=False, action='store_true', help='show negative picks (default: False)')
    # add argument that customizes chromedriver path
    parser.add_argument('-d', '--driver', default=DRIVER_PATH, help='path to driver (default: $USER_HOME/geckodriver)')
    args = parser.parse_args()

    return args.input, args.output, args.negative, args.driver
    
def read_file_list(input_file):
    input_content = input_file.read().split("\n")
    file_list = [x for x in input_content if x]
    input_file.close()
    return file_list

def browser_setup(path):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    service = Service(executable_path=path)
    browser = webdriver.Firefox(options=options, service=service)
    return browser

def ticker_is_active(browser, url):
    browser.get(url)
    sleep(.1)
    element = browser.find_element("css selector", ".match")

    if element.value_of_css_property("display") == "none":
        return False
    return True

def get_experts_view(browser, file_list):
    negative_list = []
    positive_list = []
    with(alive_bar(len(file_list)) as bar):
        for stock_name in file_list:
            # create progress bar
            is_valid = ticker_is_active(browser, EXPERTS_URL + stock_name)
            if not is_valid:
                negative_list.append(stock_name)
            else:
                positive_list.append(stock_name)

            # print(negative_list)
            # print(positive_list)
            bar()

    return negative_list, positive_list

def experts_view():
    input_file, output_file, negative, driver = args_handle()
    file_list = read_file_list(input_file)
    browser = browser_setup(driver)
    negatives, positives = get_experts_view(browser, file_list)
    out_string = ""
    if negative:
        out_string += "Negative Picks:\n"
        for stock in negatives:
            out_string += stock + "\n"
        out_string += "Positive Picks:\n"
    for stock in positives:
        out_string += stock + "\n"

    output_file.write(out_string)
    output_file.close()


if __name__ == '__main__':
    experts_view()
