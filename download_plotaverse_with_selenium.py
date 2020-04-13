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



def get_image_links_plotaverse(link_file_path):
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
    url = "https://plotaverse.com/#!/?tab=loops&search-category=members&profile=Portfolios&preview=Comments#854441"
    print('get: %s' % url)
    driver.get(url)
    print('finished get')

    for idx in range(2000):
        try:
            print("scrollBy: %d/2000" % idx)
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 5000000)")

            time.sleep(3)
            imges = driver.find_elements_by_xpath("//img[contains(@class, 'plotagraph-mask') and contains(@class, 'gallery')]")
            for img in imges:
                img_url = img.get_attribute('src')
                img_urls.add(img_url)
            print('totally get %s images' % len(img_urls))
            dst_path = '%s_%03d.txt' % (link_file_path, idx)
            with open(dst_path, 'w') as wf:
                for url in img_urls:
                    video_url = 'https://d1q2ihaj00z0i4.cloudfront.net/plotagraph-community/large/video/%s.mp4' % (url.split('/')[-1])
                    wf.write(url +'\t' + video_url + '\n')
            print('Store all the links in file {0}'.format(dst_path))
        except Exception as e:
            print(e)

    driver.quit()



def main(result_path):
    if not check():
        return

    get_image_links_plotaverse(result_path)

    print('Fininsh getting all image links')



if __name__ == "__main__":
    fire.Fire(main)