import argparse
import sys
import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup

EXPERTS_URL = "https://www.zacks.com/registration/ultimatetrader/welcome/eoffer/3393/?t="
headers = {'User-Agent': 'Mozilla/5.0'}
NEGATIVE = "Not"
POSITIVE = "One"

def args_handle():
    parser = argparse.ArgumentParser()
    # add long and short argument for the stock file
    parser.add_argument('-i', '--input', default=open("stock_list.txt", "r"), type=argparse.FileType('r'), help='input stock list name (default: stock_list.txt)')
    # add l, s for output file
    parser.add_argument('-o', '--output', default=sys.stdout, type=argparse.FileType('w'), help='output file name (default: stdout)')
    # add argument that shows negative picks
    parser.add_argument('-n', '--negative', default=False, action='store_true', help='show negative picks (default: False)')
    args = parser.parse_args()

    return args.input, args.output, args.negative
    
def read_file_list(input_file):
    input_content = input_file.read().split("\n")
    file_list = [x for x in input_content if x]
    input_file.close()
    return file_list

def get_experts_view(file_list):
    negative_list = []
    positive_list = []
    with(alive_bar(len(file_list)) as bar):
        for i, stock_name in enumerate(file_list):
            # create progress bar
            site = BeautifulSoup(requests.get(EXPERTS_URL + stock_name, headers=headers).content, 'html.parser')
            data = site.find("span", {"class": "match"}).contents[0].split(" ")
            if data[1].lower() == NEGATIVE.lower():
                negative_list.append(stock_name)
            elif data[1].lower() == POSITIVE.lower():
                positive_list.append(stock_name)
            else:
                print("Error: ", stock_name, data)
            bar()

    return negative_list, positive_list

def experts_view():
    input_file, output_file, negative = args_handle()
    file_list = read_file_list(input_file)
    negatives, positives = get_experts_view(file_list)
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