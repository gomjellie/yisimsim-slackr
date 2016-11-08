class debug:
    def wlog(text, mode='c', filename=None, filepath=None):
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
            print (text)
        else:
            with open(filepath+'/'+filename,'a') as f:
                f.write(text)
