#!/usr/bin/env python
# coding: utf-8

import re
import os
import sys
import requests


def get_prefix(s=''):
    if s.rfind('.') == -1:
        return s
    else:
        return s[:s.rfind('.')]


def get_suffix(s=''):
    if s.rfind('.') == -1:
        return ''
    else:
        return s[s.rfind('.') + 1:]


def get_info(filepath=None):
    """Give a txt file, parse the folder name, each file
    id and the urls"""
    try:
        cnt = open(filepath, 'r').read()
        pat_url = 'https?://[^\s]+'
        pat_id = '^\d+'

        folder_name = get_prefix(os.path.basename(filepath))
        urls = re.findall(pat_url, cnt)
        ids = re.findall(pat_id, cnt, re.MULTILINE)

        return (folder_name, urls, ids)
    except:
        print 'Parse file info failed'
        sys.exit()


def gen_wget_scripts(urls=None, ids=None, folder_name=None):
    header = 'User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
    if len(urls) != len(ids):
        return
    script = ''
    for url, id in zip(urls, ids):
        out_path = os.path.join(folder_name, id)
        # script += 'wget --keep-session-cookies --header="%s" -c -t 3 %s -O %s\n' % (header, url, out_path)
        script += 'wget %s -O %s\n' % (url, out_path)
    return script


def str2file(s='', filename='down.sh', num_line=None):
    try:
        if num_line is None or s.count('\n') < num_line:
            open(filename, 'w').write(s)
        else:
            s_list = s.splitlines()
            s = '\n'.join(s_list[:num_line]) + '\n'
            open(filename, 'w').write(s)
    except:
        print 'convert string to file failed'
        sys.exit()

class Downloader():
    def __init__(self):
        self.session = requests.Session()
        self.init()

    def init(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
        self.session.headers.update(header)

    def download(self, url=None, id=None, folder_name=None):
        try:
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            ret = self.session.get(url).content
            filepath = os.path.join(folder_name, id)
            open(filepath, 'w').write(ret)
        except:
            print 'URL: %s downloaded error' % url
            # sys.exit()

    def download_batch(self, urls=None, ids=None, folder_name=None, num=None):
        if len(urls) != len(ids):
            print 'urls and ids not match'
            sys.exit()

        i = 0
        for url, id in zip(urls, ids):
            self.download(url, id, folder_name)
            i += 1
            if not num and i > num: break

def test4():
    filepath = 'A.J._Buckley.txt'
    (folder_name, urls, ids) = get_info(filepath)

    d = Downloader()
    d.download_batch(urls, ids, folder_name, 10)



def test3():
    filepath = 'vgg_face_dataset/files/A.J._Buckley.txt'
    (folder_name, urls, ids) = get_info(filepath)
    s = gen_wget_scripts(urls, ids, folder_name)

    str2file(s, 'down.sh', 100)


def test2():
    # 8s to parse all files
    filedir = 'vgg_face_dataset/files'
    for fl in os.listdir(filedir):
        if get_suffix(fl) != 'txt': continue
        filepath = os.path.join(filedir, fl)
        get_info(filepath)


def test():
    filepath = 'vgg_face_dataset/files/:q.txt'
    (folder_name, urls, ids) = get_info(filepath)
    # print folder_name
    # print len(urls)
    # print len(ids)

    # pair = zip(ids, urls)
    # print pair[0]
    print gen_wget_scripts(urls, ids, folder_name)


def main():
    # test()
    # test2()
    # test3()
    test4()

if __name__ == '__main__':
    main()
