# -*- coding: utf-8 -*-
from django.conf import settings

from datetime import datetime

import os
import json
import logging
import posixpath

logger = logging.getLogger()

SPIDER_DIR = posixpath.join(settings.BASE_DIR, 'spider')
SCRAPY_CMD = settings.SCRAPY_CMD

def crawl_dxy():
    logger.info('开始', datetime.now())
    commands = []
    commands.append('cd %s' % SPIDER_DIR)
    commands.append('/home/zhanglei3/.virtualenvs/covid19/bin/scrapy crawl dxy')
    command = '&&'.join(commands)
    logger.info('命令', command)
    logger.info('结果', os.popen(command).read())
    logger.info('完成', datetime.now())