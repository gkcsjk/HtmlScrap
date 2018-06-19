# coding:utf-8

"""
This script should work with utils.py and proxies_ip.csv
This is just a example and will only work at hotfrog.com.au
You need to check the source code of your target website and test their
protection mechanism to determine how to retrieve information from it.
"""
import urllib3
import requests
import utils
import time
from bs4 import BeautifulSoup

# urllib3 settings
http = urllib3.PoolManager()
urllib3.disable_warnings()


# get the proxies ip with two methods

# method 1: get proxy IPs directly from https://free-proxy-list.net/
# proxies_pool = utils.get_ip_list(utils.url, headers=utils.headers)

# method 2: get IPs from proxies_ip.csv (need to be type-in/copy-paste manually)
proxies_pool = utils.get_ip_list_temp()


# read from hotfrog.csv
def read_by_lines(proxies_loc):
    with open("hotfrog.csv") as ip:
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
                results, proxies_loc = process_url(url, proxies_loc)  # process the url

                # after get the results, write them into the file
                try:
                    utils.write_url(filename, results, fieldnames)
                except IOError:
                    print("Fail to open file...")
                print(filename + ' ' + url)


# process the url
def process_url(url_loc, proxies_loc):
    print(url_loc)
    results = []

    # If we use proxies
    # (not in this case, because it will ask for a robot check if the ip is not fro Au)
    if proxies_loc is not False:
        while True:
            try:
                print("Uss proxy:", proxies_loc)
                page = requests.get(url_loc, proxies=proxies_loc, headers=utils.headers, timeout=3)
                if page.status_code != 200:
                    print(page.status_code)
                    proxies_loc = proxy_test(url_loc)
                    continue
                break
            except Exception:
                print("Proxy cannot be connected, change to another proxy...")
                proxies_loc = proxy_test(url_loc)

    # If we do NOT use proxies
    else:
        while True:
            try:
                page = requests.get(url_loc, headers=utils.headers, timeout=3)
                break
            except Exception:
                print("Connection error. trying again...")
                time.sleep(5)
                continue

    # get the page content using beautiful soup
    soup = BeautifulSoup(page.text, 'html.parser')

    # find all <div>s with class "tile-content" into a list
    data_list = soup.find_all("div", class_="tile-content")

    # for each <div> in the list, we get information from it
    # in this case, we need to go through its child page to get required information
    # So we get the its child link call method "process_sub_url()"
    for data_block in data_list:
        result = {}
        company_name = data_block.find("a")
        if company_name is not None:
            sub_link = company_name["href"]
            company_name = company_name.text
            company_address, company_state, company_tel, company_web = process_sub_url(sub_link)
            result['Name'] = company_name
            result['Address'] = company_address
            result['State'] = company_state
            result['Tel'] = company_tel
            result['Website'] = company_web
            results.append(result)
            print(result)

    return results, proxies_loc


# process the child link
def process_sub_url(url_loc):
    # in the case that proxy is used, we need to handle the proxy here as well
    # for example:
    # def process_sub_url(url_loc, proxies_loc):
    # if proxies_loc is not False:
    #     while True:
    #         try:
    #             print("Uss proxy:", proxies_loc)
    #             page = requests.get(url_loc, proxies=proxies_loc, headers=utils.headers, timeout=3)
    #             if page.status_code != 200:
    #                 print(page.status_code)
    #                 proxies_loc = proxy_test(url_loc)
    #                 continue
    #             break
    #         except Exception:
    #             print("Proxy cannot be connected, change to another proxy...")
    #             proxies_loc = proxy_test(url_loc)

    while True:
        try:
            page = requests.get(url_loc, headers=utils.headers, timeout=3)
            break
        except Exception:
            print("connection error, trying again...")
            time.sleep(5)
            continue
    soup = BeautifulSoup(page.text, 'html.parser')
    contact = soup.find('div', class_='company-contact-info')

    # company address and state
    company_state = contact.find('span', class_='data-state')
    if company_state is not None:
        company_state = company_state.text
    else:
        company_state = ''
    company_address1 = contact.find('span', class_='data-address1')
    company_city = contact.find('span', class_='data-city')
    company_postcode = contact.find('span', class_='data-postcode')
    if company_address1 is not None:
        company_address1 = company_address1.text
    else:
        company_address1 = ''
    if company_city is not None:
        company_city = company_city.text
    else:
        company_city = ''
    if company_postcode is not None:
        company_postcode = company_postcode.text
    else:
        company_postcode = ''

    company_address = company_address1 + ', ' + company_city + ', ' + company_state + ' '+ company_postcode

    # company phone
    company_tel = contact.find('span', class_='data-phone')
    if company_tel is not None:
        company_tel = company_tel.text
    else:
        company_tel = ''

    # company web
    company_web = contact.find('a', class_='company-url-website')
    if company_web is not None:
        company_web = company_web['href']
    else:
        company_web = ''

    return company_address, company_state, company_tel, company_web


# Choose ip from proxies pool and test if it works for current url
def proxy_test(url_loc):
    proxies_loc = utils.get_random_ip(proxies_pool)
    print("Use proxy:", proxies_loc)
    while True:
        try:
            print(url_loc)
            status_code = requests.get(url_loc, headers=utils.headers, proxies=proxies_loc).status_code
            if status_code != 200:
                print(status_code)
                proxies_loc = utils.get_random_ip(proxies_pool)
                continue
            break
        except Exception:
            proxies_loc = utils.get_random_ip(proxies_pool)
            print("cannot connect proxy... keep trying:", proxies_loc)

    return proxies


if __name__ == '__main__':

    # the fields needed in result csv file
    fieldnames = ['Name', 'Address', 'State', 'Tel', 'Website']

    # if we are going to use proxy
    if_proxies = False
    if if_proxies is True:
        proxies = utils.get_random_ip(proxies_pool)
        read_by_lines(proxies)
    else:
        read_by_lines(if_proxies)
