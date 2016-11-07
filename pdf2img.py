#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wand.image import Image
from PyPDF2 import PdfFileReader
import logging
import os,sys
import warnings
import threading


def process(source,beginning,ending):
    # 取文件名（test/test1/ab）
    file_path = os.path.splitext(source)[0]
    logging.info('=========>>> Start')
    for i in range(beginning,ending):
        with Image(filename=source + '[' + str(i) + ']',resolution=200) as converted:
            converted.compression_quality = 45
            newfile = file_path + '-' + str(i + 1) + '.jpg'
            converted.save(filename=newfile )
            logging.info(threading.current_thread().getName() + ' ' + newfile)
    if not os.path.isfile(newfile): logging.warning('page of file is not found:[%s]' % (newfile))

if __name__ == '__main__':

    # 禁用警告
    warnings.filterwarnings('ignore')

    # 设置logging
    if not os.path.exists('logs'): os.mkdir('logs')
    log_filename = 'logs/pdf2img.log'
    logging.basicConfig(filename=log_filename, filemode='a', level=logging.DEBUG,
                        format = '%(asctime)s %(filename)s [%(levelname)s] %(message)s',
                        datefmt = '[%Y-%m-%d %H:%M:%S]',
                        )

    try:
        # get_source = 'test/test1/ab.pdf'
        get_source = sys.argv[1]
        # 线程数
        threads = 4
        # 获取页数
        input_file = PdfFileReader(file(get_source, 'rb'))
        pages = input_file.getNumPages()
        step = pages / threads
        ending_page = 0
        # 线程
        threads_list = []
        for i in range(threads):
            beginning_page = ending_page
            ending_page = beginning_page + step
            t = threading.Thread(target=process,args=(get_source,beginning_page,ending_page))
            threads_list.append(t)
        # 启动线程
        for t in threads_list:
            t.setDaemon(True)
            t.start()
        t.join()
        process(get_source,ending_page,pages)
        print 'Page Size:%s' % (pages)
        logging.info('<<<========= End')
    except Exception,e:
        logging.error(e)
        print 'Page Size:0'


