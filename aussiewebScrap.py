# coding:utf-8
import urllib3
import requests
import utils
import time
from bs4 import BeautifulSoup

# urllib3 settings
http = urllib3.PoolManager()
urllib3.disable_warnings()


def read_by_lines():
    with open("aussieweb.csv") as ip:
        line = ip.readline()
        filename = 'default'
        while line:
            current_line = line
            line = ip.readline()

            # the line with a file name starts with "000"
            if current_line[0:3] == "000":
                filename = str(current_line[4:]).rstrip() + '.csv'
                print(filename)
                continue

            # the line with urls
            else:
                url = current_line.rstrip()  # remove '\n' or other useless chars.
                results = process_url(url)  # process the url

                # after get the results, write them into the file
                try:
                    utils.write_url(filename, results, fieldnames)
                except IOError:
                    print("Fail to open file...")
                print(filename + ' ' + url)


def process_url(url_loc):
    print(url_loc)
    results = []
    while True:
        try:
            page = requests.get(url_loc, headers=utils.headers, timeout=3)
            print(page.status_code)
            break
        except Exception:
            print("Connection Error, trying again...")
            time.sleep(5)
            continue

    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find("div", class_="panel-group")
    data_list = data.find_all("div", id="rowTable")

    for data_block in data_list:
        result = {}
        company_data = data_block.find_all("div", class_="pull-left")
        company_name = company_data[0]
        company_address = company_data[1]
        if company_name is not None:

            # company name
            company_name = company_name.find("a").text
            company_name = company_name.split(' ', 1)[1]

            # company_address & company_state
            if len(company_address.find_all('div')) == 2:
                company_address_1 = company_address.find_all("div")[0].text
                company_address_2 = company_address.find_all("div")[1].text
                company_address = company_address_1 + company_address_2
                company_state = company_address.split()[len(company_address.split())-2]
            else:
                company_address = ""
                company_state = ""

            # company_phone
            company_tel = data_block.find("div", class_="card-phone")
            if company_tel is not None:
                company_tel = company_tel.text
            else:
                company_tel = ""

            # company_web
            company_web = data_block.find("a", class_="website")
            if company_web is not None:
                company_web = company_web["href"]

            result['Name'] = company_name
            result['Address'] = company_address
            result['State'] = company_state
            result['Tel'] = company_tel
            result['Website'] = company_web
            results.append(result)
            print(result)

    return results


if __name__ == '__main__':
    # the fields needed in result csv file
    fieldnames = ['Name', 'Address', 'State', 'Tel', 'Website']
    read_by_lines()
