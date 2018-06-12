import urllib3
import csv
import re
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
urllib3.disable_warnings()


# Read the URLs from [filename], return a list of URLs.
def read_url(filename):
    urls = []
    with open(filename) as inputUrl:
        urlReader = csv.reader(inputUrl)
        for row in urlReader:
            for item in row:
                urls.append(item)
        return urls


# Write the result into the [filename].
def write_url(filename, result):
    with open(filename, 'a') as output:

        # Change the code below to change the output format
        fieldnames = ['Name', 'Address', 'Tel', 'Website']
        urlWriter = csv.DictWriter(output, fieldnames=fieldnames)
        # Change the code above

        for row in result:
            urlWriter.writerow(row)


# Process the each URL and find out the list of company links.
def process_url(url):
    sub_pages = []
    results = []
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'lxml')

    # Change the code below to make it suitable for your target website
    data_list = soup.find_all('h2')
    for item in data_list:
        if item.a is not None:
            sub_pages.append(item.a.attrs['href'])

    print("Now, processing the sub-links inside...")
    for sub_page in sub_pages:
        sub_page = 'https://www.desimarket.com.au/' + sub_page
        results.append(process_sub_url(sub_page))
    # Change the code above

    write_url('output.csv', results)


# Process each company link to get the information needed.
def process_sub_url(url):
    sub_result = {}
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'lxml')
    company_name = soup.h1.string
    address = soup.address.string
    tel = soup.find('a', class_='tel')
    if tel is not None:
        tel = tel.text
        tel = re.search('(?:\+?(61))? ?(?:\((?=.*\)))?(0?[2-57-8])\)? ?(\d\d(?:[- ](?=\d{3})|(?!\d\d[- ]?\d[- ]))\d\d[- ]?\d[- ]?\d{3})', tel)
        if tel is not None:
            tel = tel.group(0)
        else:
            tel = ''
    web = soup.find('a', class_='url')
    if web is not None:
        web = web.text
    print(company_name, address, tel, web)
    sub_result['Name'] = company_name
    sub_result['Address'] = address
    sub_result['Tel'] = tel
    sub_result['Website'] = web
    return sub_result


def main():
    urls = read_url("input.csv")
    i = 1
    for url in urls:
        print("Processing the", i, "link from input.csv")
        process_url(url)
        i += 1


if __name__ == "__main__":
    main()
