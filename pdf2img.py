#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wand.image import Image
from PyPDF2 import PdfFileReader
import logging
import os,sys
import warnings


def process(source):
    # 取文件名
    file_path = os.path.splitext(source)[0]
    input_file = PdfFileReader(file(source,'rb'))
    pages = input_file.getNumPages()
    logging.info('')
    for i in range(pages):
        with Image(filename=source + '[' + str(i) + ']',resolution=200) as converted:
            converted.compression_quality = 45
            newfile = file_path + '-' + str(i + 1) + '.png'
            converted.save(filename=newfile )
            logging.info(newfile)
    if not os.path.isfile(newfile): logging.warning('page of file is not found:[%s]' % (newfile))
    print 'Page Size:%s' % (pages)

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
        process(get_source)
    except Exception,e:
        logging.error(e)
        print 'Page Size:0'
