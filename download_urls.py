import sys
import os
import fire
from multiprocessing.dummy import Pool as ThreadPool


def load_datas(urls_files):
    urls = []
    with open(urls_files) as f:
        lines = f.readlines()
        for line in lines:
            urls.append(line.strip())
    return urls


def main(urls_file, dst_folder, thread_num=20):
    urls = load_datas(urls_file)
    print('total = %s' % (len(urls)))

    def download_func(idx_url):
        idx, url = idx_url
        terms = url.split('?')
        terms = terms[0].split('/')
        img_name = terms[-1]
        if not(img_name.lower().endswith('jpg') or img_name.lower().endswith('jpeg') or img_name.lower().endswith('png')):
            return
        # cmd = 'curl -s -f %s -o %s/%s' % (url, dst_folder, img_name)
        cmd = 'wget "%s" -O %s/%s' % (url, dst_folder, img_name)
        os.system(cmd)
        if idx % 1000 == 0:
            print(cmd)

    pool = ThreadPool(thread_num)
    pool.map(download_func, [(i, url) for i, url in enumerate(urls)])
    pool.close()


if __name__ == '__main__':
    fire.Fire(main)
