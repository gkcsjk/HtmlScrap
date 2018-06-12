from bs4 import BeautifulSoup
import requests
import random
import csv

url = 'https://free-proxy-list.net/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'cookies': '__cfduid=dc5399cae70c870d551f6faa3249506071527744656; identifier=9a19d501-e894-4d67-b1a2-0588eb8e9462; HotFrogClickThrough=OriginalReferrer=; __utmz=210638092.1527744658.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmz=1.1527744658.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=210638092.1943864752.1527744658.1527822867.1527826461.3; ASP.NET_SessionId=gvpev1gapiygtymjzwhz4a2l; __utmc=210638092; __utma=1.1450049340.1527744658.1527822868.1527827889.3; __utmc=1; __utmb=210638092.8.10.1527826461; __utmb=1.12.10.1527827889',
}


def get_ip_list_temp():
    ip_list = []
    with open("proxies_ip.csv") as proxies_file:
        proxies_reader = csv.reader(proxies_file)
        for row in proxies_reader:
            ip_list += row
    return ip_list


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    soup = soup.find("tbody")
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        if tds is not None:
            ip_list.append(tds[0].text + ':' + tds[1].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append("http://" + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {"http": proxy_ip, "https": proxy_ip}
    return proxies


# Read the URLs from [filename], return a list of URLs.
def read_url(filename):
    urls = []
    with open(filename) as inputUrl:
        for item in inputUrl:
            urls.append(item)
        return urls


# Write the result into the [filename].
def write_url(filename, result, fieldnames):
    with open(filename, 'a', newline='') as output:
        urlWriter = csv.DictWriter(output, fieldnames=fieldnames)
        for row in result:
            urlWriter.writerow(row)
