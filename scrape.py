import json
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.PhantomJS()
browser.get('http://proxylist.hidemyass.com/')

def scrape():
    proxies = []

    while True:
        table = browser.find_element_by_tag_name('table')
        tbody = table.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')

        #   go over all rows
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            last_update = tds[0].text
            ip = tds[1].text
            port = int(tds[2].text)
            country = tds[3].text
            speed_indicator = tds[4].find_element_by_class_name('indicator')
            speed_indicator_style = speed_indicator.get_attribute('style')
            speed = int(speed_indicator_style.split('width:')[1].split('%')[0])
            connection_time_indicator = tds[5].find_element_by_class_name('indicator')
            connection_time_indicator_style = connection_time_indicator.get_attribute('style')
            connection_time = int(connection_time_indicator_style.split('width:')[1].split('%')[0])
            typ = tds[6].text
            anonymity = tds[7].text

            proxies.append([last_update, ip, port, country, speed, connection_time, typ, anonymity])
        try:
            next_button = browser.find_element_by_class_name('pagination')\
                                 .find_element_by_xpath('//a[@class="next"]')
        except NoSuchElementException:
            #   we've reached the last page
            break

        next_button.click()

        #   wait 5 seconds for the ajax response
        time.sleep(5)

    return proxies

if __name__ == "__main__":
    for proxy in scrape():
        print json.dumps(proxy)
