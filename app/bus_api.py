from bs4 import BeautifulSoup
import urllib
import requests

class bus_api:
    """
    ex: http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=13157'
    """

    url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp'

    def get_station_stat(station_number):
        res = requests.get(bus_api.url, dict(strBusNumber=station_number))
        soup = BeautifulSoup(res.text, 'html.parser')
        ret = ''

        for bus_name, left_time_1, left_time_2 in zip(soup.select('rtnm'),\
                soup.select('arrmsg1'), soup.select('arrmsg2')):
            ret += "-------------------\n| Bus:{0:<8}\n|{1:<10}\n|{2:<13}\n".format(\
                    bus_name.string, left_time_1.string, left_time_2.string)
        return ret + '-------------------'

#            print("bus_name: {0} left_time {1} ---- left_time {2}".format(\
        #                    bus_name.string, left_time_1.string, left_time_2.string))

