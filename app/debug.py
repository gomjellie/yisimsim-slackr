from app.singletone import singletone
import os
import logging

class debug(metaclass = singletone):
    def __init__(self, level=logging.DEBUG):
        self.logger=logging.getLogger('app')
        self.logger.addHandler(logging.StreamHandler())

        self.level=level
        self.logger.setLevel(self.level)
    def set_logger_level(self,level):
        self.level=level
        self.logger.setLevel(self.level)
    def wlog(self,text, mode='c', filename=None, filepath=None):
        '''
            has 2 modes; console and file
            mode can have 2 values 'c' and 'f' which stands for console and file each
            default debug mode is 'c'(console)

            filename should include extension

            ex> debug.wlog('c',"i love debugging") ==> prints i love debugging to console
                debug.wlog('f',"i love debugging", 'log.txt', 'debugginh/master')
                 ==> appends text to debugginh/master/log.txt
        '''
        if mode == "c":
            self.logger.debug(text)
        else:
            if not os.path.exists(filepath):
                os.mkdir(filepath)

            full_path=filepath+'/'+filename

            self.logger.basicConfig(filename=full_path,level=self.level)
            self.logger.debug(text)
