import json
import time
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='log.log',
                    filemode='w')

browser = webdriver.PhantomJS()
browser.get('http://proxylist.hidemyass.com/')

def scrape():
    proxies = []

    while True:
        pagination = browser.find_element_by_class_name('pagination')
        current_page = pagination.find_element_by_xpath('//li[@class="current"]')
        logging.info("Scraping page {}".format(current_page.text))

        table = browser.find_element_by_tag_name('table')
        tbody = table.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')

        #   go over all rows
        found_proxies = 0
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
            found_proxies += 1

        logging.info("Found {} proxies on page {}".format(found_proxies, current_page.text))

        try:
            next_button = pagination.find_element_by_xpath('//a[@class="next"]')
        except NoSuchElementException:
            logging.info("Reached the last page")
            break

        next_button.click()

        #   wait 5 seconds for the ajax response
        time.sleep(5)

    return proxies

if __name__ == "__main__":
    for proxy in scrape():
        print json.dumps(proxy)
