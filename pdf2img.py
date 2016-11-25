#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wand.image import Image
from PyPDF2 import PdfFileReader
import logging
import os
import warnings
import multiprocessing
import re


def logs():
    # 禁用警告
    warnings.filterwarnings('ignore')
    # 设置logging
    if not os.path.exists('logs'): os.mkdir('logs')
    log_filename = 'logs/pdf2img.log'
    logging.basicConfig(filename=log_filename, filemode='a', level=logging.DEBUG,
                        format='%(asctime)s %(filename)s [%(levelname)s] %(message)s',
                        datefmt='[%Y-%m-%d %H:%M:%S]',
                        )


def process(single_page):
    pattern = re.compile('\[|\]')
    # 页码
    page_num = pattern.split(single_page)[1]
    with Image(filename=single_page, resolution=200) as converted:
        converted.compression_quality = 45
        newfilename = file_text + page_num + '.jpg'
        converted.save(filename=newfilename)
        logging.info(multiprocessing.current_process().name + '' + newfilename)
    if not os.path.isfile(newfilename): logging.warning('page of file is not found:[%s]' % (newfilename))


def get_pages(filename):
    return PdfFileReader(file(filename, 'rb')).getNumPages()


if __name__ == '__main__':
    logs()
    try:
        get_source = 'test/test1/large.pdf'
        file_text = os.path.splitext(get_source)[0]
        # get_source = sys.argv[1]
        pages = get_pages(get_source)
        # 进程程数
        process_num = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=process_num)
        # 生成一个列表包含所有页码
        # ['test/test1/ab.pdf[0]', 'test/test1/ab.pdf[1]', 'test/test1/ab.pdf[2]', 'test/test1/ab.pdf[3]']
        page_list = [get_source + "[" + str(i) + "]" for i in range(pages)]
        logging.info('=========>>>> Start [Process num: %s]' % (process_num))
        pool.map(process, page_list)
        pool.close()
        pool.join()
        print 'Page Size:%s' % (pages)
        logging.info('<<<========= End')
    except Exception, e:
        logging.error(e)
        print 'Page Size:0'
