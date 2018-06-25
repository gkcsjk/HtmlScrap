import urllib3
import requests
import utils
import time
from bs4 import BeautifulSoup

# urllib3 settings
http = urllib3.PoolManager()
urllib3.disable_warnings()


def read_by_lines():
    with open("startlocal.csv") as ip:
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
    data_list = soup.find_all("div", class_='item')

    for data_block in data_list:
        result = {}
        data_block_1 = data_block.find('div', class_='title')
        company_name = data_block_1.find('a')
        if company_name is not None:
            company_name = company_name.text

            company_address = data_block_1.find('p', class_='info')
            if company_address is not None:
                company_address = company_address.text[1:]
                company_state = company_address.split(', ')[len(company_address.split(', '))-2]
            else:
                company_address = ""
                company_state = ""

            try:
                company_tel = data_block.find('ul', class_='links')
                company_tel = company_tel.find('a')['data-phone'][1:]
            except Exception:
                company_tel = ""

            result['Name'] = company_name
            result['Address'] = company_address
            result['State'] = company_state
            result['Tel'] = company_tel
            result['Website'] = ""
            results.append(result)
            print(result)

    return results


if __name__ == '__main__':
    fieldnames = ['Name', 'Address', 'State', 'Tel', 'Website']
    read_by_lines()
