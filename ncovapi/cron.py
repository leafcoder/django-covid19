# -*- coding: utf-8 -*-
from django.conf import settings

from datetime import datetime

import os
import sys
import json
import posixpath

SPIDER_DIR = posixpath.join(settings.BASE_DIR, 'spider')
SCRAPY_CMD = settings.SCRAPY_CMD

def crawl_dxy():
    sys.stdout.write('开始：%s\n' % datetime.now())
    commands = []
    commands.append('cd %s' % SPIDER_DIR)
    commands.append('%s crawl dxy' % SCRAPY_CMD)
    command = '&&'.join(commands)
    sys.stdout.write('命令：%s\n' % command)
    sys.stdout.write('结果：%s\n' % os.popen(command).read())
    sys.stdout.write('完成：%s\n' % datetime.now())