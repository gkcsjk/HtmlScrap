# HtmlScrap
This project is to retrieve data from some websites and write into csv files.
## Project Structure
    .
    ├── aussiewebScrap.py           # https://www.aussieweb.com.au/
    ├── hotfrogScrap.py             # https://www.hotfrog.com.au/
    ├── main.py                     # The simplest html scraping template for https://www.desimarket.com.au/
    ├── proxies_ip.csv              # Manually build the proxies pool
    ├── requirements.txt            # requirements generated by pip
    ├── startlocalScrap.py          # https://www.startlocal.com.au/
    ├── utils.py                    # Tools and utilities: choosing proxy; reading & writing files 
    ├── yellowpagesScrap.py         # https://www.yellowpages.com.au/
    ├── yelpScrap.py                # https://www.yelp.com/
    └── README.md
## Getting start
### Requirements
You need to config your python environment before getting data.
* You may use virtualenv to build your python environment. 
```
https://virtualenv.pypa.io/en/stable/
```
* Python 3.6 with pip should be installed. 
* Please refer to ```requirements.txt```. To install all requirements:
```
pip install -r requirements.txt
```
* You may use Pycharm IDE to create your virtual environment as well:
```
https://www.jetbrains.com/help/pycharm/quick-start-guide.html
```
### Installing 
After the environment is well built. You can simply clone the repository.
```
git clone https://github.com/gkcsjk/HtmlScrap.git
```
## Running existing scripts
If you are using virtualenv, you need to active the environment first:
```
source venv/bin/active
```
### Example_1: main.py | yellowpageScrap.py
These two scripts will get input URLs from ```input.csv```. Please ensure you have a input.csv file in your root folder.
Each row contains only one URLs, please ensure there no duplicated '\n' or other chars. 
The result will export into ```output.csv```.
To run to scripts:
```
python main.py
```
or
```
python yellowpageScrap.py
```
These two websites do not have IP-block protection but may check your http headers. 
You may find some useful information of setting http headers [here](https://www.tutorialspoint.com/http/http_header_fields.htm).
The most important field is ```user-agent```, which defines your browser and other request information.
### Example_2: yelpScrap.py
Yelp will check your http headers and has very strict IP-block protection. Therefor, it is necessary to use proxies to retrieve data.
So that you can change to another IP if they block your current one.
#### Build your Proxies pool manually 
You can search for proxies on the internet and copy&paste them into ```proxies_ip.csv```. The format should be:
```
127.0.0.0:8888
127.0.0.1:9999      #ip:port
...
```
[This website](http://free-proxy.cz/en/) can filter ips by countries and also can order the ips by speed/uptime/response. It can also export the ip list so that you can copy them to your ```proxies_ip.csv```.
#### Get proxies from websites automatically
In ```util.py```, I gave a example to dynamically get proxies from [Free Proxy List](https://free-proxy-list.net/).
The way to get proxies from websites is still HTML scrap. For example:
```
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
```
In this example, I used Beautiful soup to get rows from the proxy list table on the web page. 
Because the list is updating regularly, every time you call this method, it will return the newest proxies. 
To run the script:
```
python yelpScrap.py [filename.csv]
```
You can customized the out put filename yourself by setting the second argument in the command line.
### Example_3: aussiewebScrap.py | hotfrogScrap.py | startlocalScrap.py
These websites will not block your ip address but will check your http header. So we do not need to use proxies.
In this example, we use a different kind of input format. The filename would be ```web_name.csv```(eg.```aussieweb.csv```, ```hotfrog.csv```).
And inside the file, it would be:
```
000 category1_childCategory1
URL_1
URL_2
...
URL_n
000 category1_childCategory2
URL_1
URL_2
...
URL_n
000 category2_childCategory1
URL_1
...
```
For example:
```
000 Health_Health_Care
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=Health+care&query2=Melbourne%2C+VIC%2C+3000
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=Health%20care;query2=Melbourne%2C%20VIC%2C%203000;mh=25;;nh=2
000 Health_GP
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=GP&query2=Melbourne%2C+VIC%2C+3000
000 Health_Chiropractor
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=chiropractor&query2=Melbourne%2C+VIC%2C+3000
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=chiropractor;query2=Melbourne%2C%20VIC%2C%203000;mh=25;;nh=2
000 Lawyers_Legal_Support
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=legal+support&query2=
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=legal%20support;mh=25;;nh=2
000 Lawyers_Patent_Attorney
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=patent+attorney&query2=
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=patent%20attorney;mh=25;;nh=2
000 Logistics_Domestic_Shipping
https://www.startlocal.com.au/cgi-bin/directory/search.cgi?query=domestic+shipping&query2=
```
To run the script:
```
python aussieweb.py
```
or
```
python hotfrog.py
```
or 
```
python startlocal.py
```
The result will be exported into different files with the filename of categories (eg.```Lawyer_Legal_Support.csv```).
## Steps of Building Scripts for New Website
Please refer to [this file](https://github.com/gkcsjk/HtmlScrap/blob/master/User%20guide%20of%20HTML%20Scraper.pdf), which is base on ```main.py```. It gives you the basic idea of using Beautiful soup.
Here are some tips:
* View the website and determine how will you get the data. In Chrome, using the key```F12``` into developer mode is always a useful tool and 80% html scraping issues can be solved base on it.
* Use Beautiful Soup to create your on method to get the data and store them into proper data structure in python.
* If you can not get the data you want, you may have to move to the child URLs. It will largely increase the times that you send your requests and decrease the efficiency of scraping, but will increase the accuracy of the data.
* Give a few (only a few) testing URLs to test if your code works. You may want to record the status_code to help you figure out whether the website have some protection mechanisms. 
* If everything is okay, you can move to your real URLs and do some pressure test the same time. For example, if the website has IP-block protection, you may not access to it after you
make hundreds of requests in a short period. In this case, you may want to use dynamic proxies to access to the website.
## Shortcomings
* It is very slow when using proxies from [Free-Proxy-List](https://free-proxy-list.net/).
* When you use overseas proxies, you may get blocked because some of the website will block the IPs from overseas. 
* Did not handle the Robot-Check.
* Did not handle the cookies (Some websites may use cookies to identify whether you are a human been or a robot.
* It is not user friendly and users need to modify codes every time they want data from a different website.





