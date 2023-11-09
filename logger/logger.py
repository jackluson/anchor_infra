'''
Desc:
File: /infra/logger/logger.py
File Created: Wednesday, 4th October 2023 9:51:34 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import logging
import os
from pythonjsonlogger import jsonlogger

class Logger(logging.Logger):

    def __init__(self,
                 name='root',
                 logger_level=logging.DEBUG,
                 file=None,
                 show_stream=True,
                 logger_format=" [%(asctime)s]  %(levelname)s %(filename)s [ line:%(lineno)d ] %(message)s"
                 ):
        super().__init__(name)
        self.setLevel(logger_level)
        fmt = logging.Formatter(logger_format)
        # logHandler.setFormatter(formatter)
        if file:
            os.makedirs(os.path.dirname(file), exist_ok=True)  
            file_handler = logging.FileHandler(file)
            # 4、设置 file_handler 级别
            file_handler.setLevel(logger_level)
            datefmt="%Y-%m-%dT%H:%M:%S"
            formatter = jsonlogger.JsonFormatter(fmt=logger_format, datefmt=datefmt,json_ensure_ascii=False)  
            # formatter = jsonlogger.JsonFormatter(logger_format)
            # 6、设置handler格式
            file_handler.setFormatter(formatter)
            # 7、添加handler
            self.addHandler(file_handler)
        if show_stream:
            stream_handler = logging.StreamHandler()
            # 4、设置 stream_handler 级别
            stream_handler.setLevel(logger_level)
            # 6、设置handler格式
            stream_handler.setFormatter(fmt)
            # 7、添加handler
            self.addHandler(stream_handler)

error_logger = Logger(file='log/error.log', show_stream=True, logger_level=logging.ERROR)

logger = Logger(file='log/log.log',show_stream=True)
