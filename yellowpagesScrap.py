import urllib3
import re
import requests
import utils
from bs4 import BeautifulSoup

# proxies = utils.get_random_ip(utils.get_ip_list(utils.url, headers=utils.headers))
http = urllib3.PoolManager()
urllib3.disable_warnings()
fieldnames = ['Name', 'Address', 'Suburb', 'Tel', 'Email', 'Website']


def process_url(url):
    results = []

    page = requests.get(url, headers=utils.headers)
    print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Change the code below to make it suitable for your target website
    data_list = soup.find_all(class_="search-contact-card-table-div")
    for data_block in data_list:
        company_name = data_block.find("a", class_="listing-name")
        result = {}
        if company_name is not None:
            # Company name is not empty, otherwise just skip
            company_name = company_name.text

            # Get company address and suburbs
            company_address = data_block.find("p", class_="listing-address")
            if company_address is not None:
                company_suburb = company_address["data-address-suburb"]
                company_address = company_address.text
            else:
                company_address = ""
                company_suburb = ""

            # Get company phone
            company_phone = data_block.find("a", class_="click-to-call")
            if company_phone is not None:
                company_phone = company_phone.text
                company_phone = re.sub(r'\n', '', company_phone)
            else:
                company_phone = ""

            # Get company email address
            company_email = data_block.find("a", class_="contact-email")
            if company_email is not None:
                company_email = company_email["data-email"]
            else:
                company_email = ""

            # Get company website
            company_web = data_block.find("a", class_="contact-url")
            if company_web is not None:
                company_web = company_web["href"]
            else:
                company_web = ""

            result['Name'] = company_name
            result['Address'] = company_address
            result['Suburb'] = company_suburb
            result['Tel'] = company_phone
            result['Email'] = company_email
            result['Website'] = company_web
            results.append(result)
    return results


def main():
    urls = utils.read_url("input.csv")
    i = 1
    for url in urls:
        print("Processing", url)
        utils.write_url("output.csv", process_url(url), fieldnames)
        i += 1


if __name__ == "__main__":
    main()
