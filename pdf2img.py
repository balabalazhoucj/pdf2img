#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wand.image import Image
from PyPDF2 import PdfFileReader
import logging
import os,re,sys
import warnings


def process(source):
    # 取文件名
    file_path = os.path.splitext(source)[0]
    input_file = PdfFileReader(file(source,'rb'))
    pages = input_file.getNumPages()
    path = os.path.split(file_path)
    print path

    logging.info('')
    for i in range(pages):
        with Image(filename=source + '[' + str(i) + ']',resolution=200) as converted:
            converted.compression_quality = 45
            newfile = file_path + '-' + str(i + 1) + '.png'
            converted.save(filename=newfile )
            logging.info(newfile)

    # 验证文件数量
    # 取文件名
    p = re.compile(path[1])
    all_file = ','.join(os.listdir(path[0]))
    if len(p.findall(all_file)) - 2 == pages or len(p.findall(all_file)) - 3 == pages:
        print 'Page Size:%s' % (pages)
    else:
        print pages
        logging.warning(' '.join(os.listdir(path[0])))

if __name__ == '__main__':
    try:
        # 禁用警告
        warnings.filterwarnings('ignore')

        # 设置logging
        if not os.path.exists('logs'): os.mkdir('logs')
        log_filename = 'logs/pdf2img.log'
        logging.basicConfig(filename=log_filename, filemode='a', level=logging.DEBUG,
                            format = '%(asctime)s %(filename)s [%(levelname)s] %(message)s',
                            datefmt = '[%Y-%m-%d %H:%M:%S]',
                            )

        get_source = 'test/test1/bbb.pdf'
        #get_source = sys.argv[1]
        if get_source:
            process(get_source)
        else:
            logging.error('no file')
    except Exception,e:
        print 'Page Size:0'
