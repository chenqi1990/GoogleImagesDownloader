# -*- coding: utf-8 -*-
# @Author: WuLC
# @Date:   2017-09-27 23:02:19
# @Last Modified by:   Qi Chen
# @Last Modified time: 2018-10-30

import os
import json
import time
import logging
import fire
import configparser
from urllib.parse import unquote

from multiprocessing import Pool
from selenium import webdriver


def check():
    file_name = 'geckodriver'
    if not os.path.exists(file_name):
        try:
            cmd = "wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-macos.tar.gz"
            os.system(cmd)
            cmd = "tar -zxf geckodriver-v0.23.0-macos.tar.gz"
            os.system(cmd)
        except Exception as e:
            logging.error("install geckodriver failed")
            return False
    return True


def get_image_links_vcg(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """
    img_urls = set()

    try:
        driver = webdriver.Firefox(executable_path='./geckodriver')
        for i in range(len(supplemented_keywords)):
            search_query = main_keyword + supplemented_keywords[i]
            url = "https://www.vcg.com/creative/search_2?phrase=" + search_query
            driver.get(url)
            driver.refresh()
            for page_id in range(300):
                print('page_id = %s' % page_id)
                for __ in range(10):
                    # multiple scrolls needed to show all 400 images
                    driver.execute_script("window.scrollBy(0, 1000)")
                    time.sleep(1)

                imges = driver.find_elements_by_xpath('//a[contains(@class, "imgWaper")]//img')
                for img in imges:
                    img_url = img.get_attribute('src')
                    if img_url is None:
                        continue
                    img_urls.add(img_url)
                print("img urls = %s" % len(img_urls))
                # to load next 400 images
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//div[contains(@class,"nextpage")]').click()
                except Exception as e:
                    print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))
                    break
            print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    except Exception as e:
        print(e)

    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Vcg: Store all the links in file {0}'.format(link_file_path))


def get_image_links_veer(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """
    img_urls = set()

    try:
        driver = webdriver.Firefox(executable_path='./geckodriver')
        for i in range(len(supplemented_keywords)):
            search_query = main_keyword + supplemented_keywords[i]
            url = "https://www.veer.com/query/image?phrase=" + search_query
            driver.get(url)
            driver.refresh()
            for page_id in range(300):
                print('page_id = %s' % page_id)
                for __ in range(10):
                    # multiple scrolls needed to show all 400 images
                    driver.execute_script("window.scrollBy(0, 1000)")
                    time.sleep(1)

                imges = driver.find_elements_by_xpath('//a[contains(@class, "search_result_asset_link")]//img')
                for img in imges:
                    img_url = img.get_attribute('src')
                    if img_url is None:
                        continue
                    img_urls.add(img_url)
                print("img urls = %s" % len(img_urls))
                # to load next 400 images
                time.sleep(3)
                try:
                    driver.find_element_by_xpath('//div[contains(@class,"next")]').click()
                except Exception as e:
                    print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))
                    break
            print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    except Exception as e:
        print(e)

    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Veer: Store all the links in file {0}'.format(link_file_path))


def get_image_links_tuchong_community(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """
    img_urls = set()
    try:
        driver = webdriver.Firefox(executable_path='./geckodriver')
        for i in range(len(supplemented_keywords)):
            search_query = main_keyword + supplemented_keywords[i]
            url = "https://tuchong.com/search/post/?query="+search_query
            print('url = %s' % url)
            driver.get(url)

            for __ in range(10000000):
                # multiple scrolls needed to show all 400 images
                driver.execute_script("window.scrollBy(0, 1000)")
                time.sleep(2)
                end = driver.find_element_by_xpath('//i[contains(@class, "icon-end")]')
                if end.get_attribute('style') == '':
                    print("finished")
                    break
            time.sleep(5)

            imges = driver.find_elements_by_xpath('//div[@data-lazy-url]')
            print("imges = %s" % len(imges))
            for img in imges:
                img_url = img.get_attribute('data-lazy-url')
                if img_url is None:
                    continue
                # img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
                img_urls.add('https:' + img_url)
            print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
        print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
        driver.quit()
    except Exception as e:
        print(e)

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Tuchong Community: Store all the links in file {0}'.format(link_file_path))


def get_image_links_tuchong(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """
    img_urls = set()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    for i in range(len(supplemented_keywords)):
        search_query = main_keyword + supplemented_keywords[i]
        url = "https://stock.tuchong.com/search?term=" + search_query
        driver.get(url)
        driver.refresh()
        for page_id in range(50):
            print('page_id = %s' % page_id)
            for __ in range(10):
                # multiple scrolls needed to show all 400 images
                driver.execute_script("window.scrollBy(0, 500)")
                time.sleep(1)

            print("xpath")
            try:
                imges = driver.find_elements_by_xpath('//img')
            except Exception as e:
                print(e)
                continue
            for img in imges:
                img_url = img.get_attribute('src')
                if img_url is None or 'pstatp' not in img_url:
                    continue
                img_urls.add(img_url)
            print("img urls = %s" % len(img_urls))
            # to load next 400 images
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//a[contains(@class,"page-next")]').click()
            except Exception as e:
                print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))
                break

        print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Tuchong: Store all the links in file {0}'.format(link_file_path))


def get_image_links_google(main_keyword, supplemented_keywords, link_file_path, num_requested = 1000):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """
    number_of_scrolls = int(num_requested / 400) + 1
    # number_of_scrolls * 400 images will be opened in the browser

    img_urls = set()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    for i in range(len(supplemented_keywords)):
        search_query = main_keyword + ' ' + supplemented_keywords[i]
        url = "https://www.google.com/search?q="+search_query+"&source=lnms&tbm=isch"
        driver.get(url)

        for _ in range(number_of_scrolls):
            for __ in range(10):
                # multiple scrolls needed to show all 400 images
                driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(2)
            # to load next 400 images
            time.sleep(5)
            try:
                driver.find_element_by_xpath("//input[contains(@class, 'mye4qd')]").click()
            except Exception as e:
                print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))
                break

        # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
        # imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')  # not working anymore
        imges = driver.find_elements_by_xpath('//a[contains(@class,"wXeWr")]')
        if len(imges) <= 0:
            continue
        for img in imges:
            img.click()
            img.click()
            img_url = img.get_attribute('href')
            try:
                img_url = img_url.split('imgurl=')[1].split('&imgrefurl=')[0]
                img_url = unquote(img_url)
            except Exception as e:
                continue
            print(img_url)
            # img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
            img_urls.add(img_url)
        print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Google: Store all the links in file {0}'.format(link_file_path))


def get_image_links_baidu(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """

    img_urls = set()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    for i in range(len(supplemented_keywords)):
        search_query = main_keyword + ' ' + supplemented_keywords[i]
        url = "https://image.baidu.com/search/index?tn=baiduimage&word="+search_query+"&ie=utf-8"
        driver.get(url)

        for __ in range(30):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(1)
        # to load next 400 images
        time.sleep(5)

        print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))


        # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
        imges = driver.find_elements_by_xpath('//li[contains(@class,"imgitem")]')
        for img in imges:
            img_url = img.get_attribute('data-objurl')
            img_urls.add(img_url)
        print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Baidu: Store all the links in file {0}'.format(link_file_path))


def get_image_links_bing(main_keyword, supplemented_keywords, link_file_path):
    """get image links with selenium

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download

    Returns:
        None
    """

    img_urls = set()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    for i in range(len(supplemented_keywords)):
        search_query = main_keyword + ' ' + supplemented_keywords[i]
        url = "https://www.bing.com/images/search?q="+search_query+"&adlt=False"
        driver.get(url)

        for __ in range(30):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(1)
        # to load next 400 images
        time.sleep(5)

        print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))


        # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
        imges = driver.find_elements_by_xpath('//a[contains(@class,"iusc")]')
        for img in imges:
            img_url = json.loads(img.get_attribute('m'))["murl"]
            img_urls.add(img_url)
        print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Bing: Store all the links in file {0}'.format(link_file_path))


def main(config_file, topic_name):
    if not check():
        return

    cf = configparser.ConfigParser()
    cf.read(config_file)

    main_keywords = json.loads(cf.get(topic_name, "main_keywords"))
    supplemented_keywords = json.loads(cf.get(topic_name, "supplemented_keywords"))

    result_dir = cf.get(topic_name, "result_dir")
    search_engine = json.loads(cf.get(topic_name, "search_engine"))
    process_num = int(cf.get(topic_name, "process_num"))

    print('\n##################################')
    print('main keywords: %s' % main_keywords)
    print('supplemented_keywords: %s' % supplemented_keywords)
    print('result dir: %s' % result_dir)
    print('search engine: %s' % search_engine)
    print('process num: %s' % process_num)
    print('##################################\n')


    ###################################
    # get image links and store in file
    ###################################


    os.system("mkdir %s" % result_dir)
    os.system("mkdir %s/%s" % (result_dir, topic_name))
    for engine in search_engine:
        # multiple processes
        p = Pool(process_num)
        for keyword in main_keywords:
            link_file_path = os.path.join(result_dir, topic_name, keyword + '_' + engine + '.txt')
            print("start searching '%s' in %s " % (keyword, engine))
            if engine == 'bing':
                p.apply_async(get_image_links_bing, args=(keyword, supplemented_keywords, link_file_path))
            elif engine == 'google':
                p.apply_async(get_image_links_google, args=(keyword, supplemented_keywords, link_file_path))
            elif engine == 'tuchong':
                p.apply_async(get_image_links_tuchong, args=(keyword, supplemented_keywords, link_file_path))
            elif engine == 'tuchong_community':
                p.apply_async(get_image_links_tuchong_community, args=(keyword, supplemented_keywords, link_file_path))
            elif engine == 'veer':
                p.apply_async(get_image_links_veer, args=(keyword, supplemented_keywords, link_file_path))
            elif engine == 'vcg':
                p.apply_async(get_image_links_vcg, args=(keyword, supplemented_keywords, link_file_path))
            else:
                p.apply_async(get_image_links_baidu, args=(keyword, supplemented_keywords, link_file_path))
        p.close()
        p.join()
        os.system("cat %s/%s/* > %s/%s_%s_url.txt" % (result_dir, topic_name, result_dir, topic_name, engine))
        print('%s: Fininsh getting all image links' % engine)



if __name__ == "__main__":
    fire.Fire(main)
