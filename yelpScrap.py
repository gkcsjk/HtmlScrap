import urllib3
import re
import requests
import utils
import sys
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
urllib3.disable_warnings()
# proxies_pool = utils.get_ip_list(utils.url, headers=utils.headers)
proxies_pool = utils.get_ip_list_temp()
fieldnames = ['Name', 'Address', 'State', 'Tel', 'Website']
proxies = utils.get_random_ip(proxies_pool)


def process_url(url_loc, proxies_loc):
    results = []
    while True:
        try:
            page = requests.get(url_loc, headers=utils.headers, proxies=proxies_loc)
            if page.status_code != 200:
                proxies_loc = proxy_test(url_loc)
                continue
            break
        except Exception:
            print("proxy cannot be connected, change another proxy...")
            proxies_loc = proxy_test(url_loc)
    soup = BeautifulSoup(page.text, 'html.parser')
    data_list = soup.find_all("a", class_="biz-name")
    for data_block in data_list:
        result = {}
        company_name = data_block.find("span")
        if company_name is not None:
            company_name = company_name.text
            sub_link = "https://www.yelp.com.au/" + data_block["href"]
            company_address, company_state, company_phone, company_web, proxies_loc = process_sub_url(sub_link, proxies_loc)
            result['Name'] = company_name
            result['Address'] = company_address
            result['State'] = company_state
            result['Tel'] = company_phone
            result['Website'] = company_web
            results.append(result)
            print(result)
    return results, proxies_loc


def process_sub_url(url_loc, proxies_loc):
    print("process sub url...")
    while True:
        try:
            page = requests.get(url_loc, headers=utils.headers, proxies=proxies_loc)
            if page.status_code != 200:
                print(page.status_code)
                proxies_loc = proxy_test(url_loc)
                continue
            break
        except Exception:
            print("proxy cannot be connected, change another proxy...")
            proxies_loc = proxy_test(url_loc)
    soup = BeautifulSoup(page.text, 'html.parser')

    # State
    company_state = soup.find("span", itemprop="addressRegion")
    if company_state is not None:
        company_state = company_state.text
        company_state = re.sub(r'\n', '', company_state).strip()
    else:
        company_state = ""

    # Address
    company_address = soup.find("div", class_="media-story")
    if company_address is not None:
        company_address = company_address.find("address")
        if company_address is not None:
            company_address = company_address.text
            company_address = re.sub(r'\n', '', company_address).strip()
        else:
            company_address = ""

    else:
        company_state = ""

    # Phone
    company_phone = soup.find("span", itemprop="telephone")
    if company_phone is not None:
        company_phone = company_phone.text
        company_phone = re.sub(r'\n', '', company_phone).strip()
    else:
        company_phone = ""

    # Website
    company_web = soup.find("span", class_="biz-website")
    if company_web is not None:
        company_web = company_web.find("a")
        if company_web is not None:
            company_web = "https://www.yelp.com.au/" + company_web["href"]
            company_web, proxies_loc = process_redirect_url(company_web, proxies_loc)
        else:
            company_web = ""
    else:
        company_web = ""

    return company_address, company_state, company_phone, company_web, proxies_loc


def process_redirect_url(url_loc, proxies_loc):
    print("process redirect url...")
    while True:
        try:
            page = requests.get(url_loc, headers=utils.headers, proxies=proxies_loc)
            if page.status_code != 200:
                proxies_loc = proxy_test(url_loc)
                continue
            break
        except Exception:
            print("proxy cannot be connected, change another proxy...")
            proxies_loc = proxy_test(url_loc)
    soup = BeautifulSoup(page.text, 'html.parser')
    company_web = soup.find("a")
    if company_web is not None:
        company_web = company_web["href"]
    else:
        company_web = ""
    return company_web, proxies_loc


# Choose ip from proxies pool and test if it works for current url
def proxy_test(url_loc):
    proxies = utils.get_random_ip(proxies_pool)
    print("Use proxy:", proxies)
    while True:
        try:
            status_code = requests.get(url_loc, headers=utils.headers, proxies=proxies, verify=False).status_code
            if status_code != 200:
                print(status_code)
                proxies = utils.get_random_ip(proxies_pool)
                continue
            break
        except Exception:
            print("cannot connect proxy... keep trying...")
            proxies = utils.get_random_ip(proxies_pool)

    return proxies


if __name__ == '__main__':
    urls = utils.read_url("input.csv")
    for url in urls:
        print("Processing", url)
        results, proxies = process_url(url, proxies)
        try:
            utils.write_url(sys.argv[1], results, fieldnames)
        except IOError:
            print("Fail to open file...")

