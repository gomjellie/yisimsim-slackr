from bs4 import BeautifulSoup
import requests

class Bus(object):
    def __init__(self):
        '''
        ex: http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=13157'
        '''

        self.url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp'

    def parse(self, station_number):
        self.res = requests.get(self.url, dict(strBusNumber=13157))
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.ret = ''

        for bus_name, left_time_1, left_time_2 in zip(self.soup.select('rtnm'),\
                self.soup.select('arrmsg1'), self.soup.select('arrmsg2')):
            self.ret += "bus_name: {0} left_time {1} ---- left_time {2}\n".format(\
                    bus_name.string, left_time_1.string, left_time_2.string)
        return self.ret

#            print("bus_name: {0} left_time {1} ---- left_time {2}".format(\
        #                    bus_name.string, left_time_1.string, left_time_2.string))

