import random
import time

from selenium import webdriver


def get_movie_links(nums=1000):
    browser.get(url)
    link_list = set()
    links = browser.find_elements_by_xpath("html//div[@class='list-wp']//a[@target='_blank']")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    while len(links) < nums:
        print('nums:', len(links))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.randint(1, 10) / 10)
        more = browser.find_element_by_xpath("html//a[@class='more']")
        while len(browser.window_handles) > 1:
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        print(more.get_attribute('href'))

        more.click()
        links = browser.find_elements_by_xpath("html//div[@class='list-wp']//a[@target='_blank']")
    num = 0
    while num < nums:
        for link in links:
            href = link.get_attribute('href')
            print('href', href)
            if href not in link_list:
                link_list.add(href)
                num += 1
        with open('movie_links_1.csv', 'a')as opener:
            for href in link_list:
                opener.write(href + '\n')


if __name__ == '__main__':
    url = 'https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1,2010%E5%B9%B4%E4%BB%A3'
    option = webdriver.ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=option)
    get_movie_links(2000)
    browser.close()
