from bs4 import BeautifulSoup
import urllib
import requests

class bus_api:
    """
    ex: http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=13157'
    """

    url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp'

    def get_station_stat(station_number):
        res = requests.get(bus_api.url, dict(strBusNumber=13157))
        soup = BeautifulSoup(res.text, 'html.parser')
        ret = ''

        for bus_name, left_time_1, left_time_2 in zip(soup.select('rtnm'),\
                soup.select('arrmsg1'), soup.select('arrmsg2')):
            ret += "-------------------\n| Bus:{0:<8}\n|{1:<10}\n|{2:<13}\n".format(\
                    bus_name.string, left_time_1.string, left_time_2.string)
        return ret + '-------------------'

#            print("bus_name: {0} left_time {1} ---- left_time {2}".format(\
        #                    bus_name.string, left_time_1.string, left_time_2.string))

class villageBus_api:
    def get_station_stat(station_name):
        original_name = station_name
        search_by_name_url = 'http://m.bus.go.kr/mBus/bus/getRttpStationByName.bms'
        search_by_ars_id_url = 'http://m.bus.go.kr/mBus/bus/getRttpStationByUid.bms'
        station_name = urllib.parse.quote(station_name)
        res = requests.get(search_by_name_url+'?stSrch='+station_name.replace('%','%25')+'&stRttp=2')
        jsn = res.json()
        ret = ''
        if jsn.get('resultList') is None:
            return '그런역 없습니다'
        ret += original_name+'으로 검색한 결과'+str(len(jsn.get('resultList')))+'개 정류소 발견\n'
        for idx in range(len(jsn.get('resultList'))):
            arsId = jsn.get('resultList')[idx].get('arsId')
            ret += '|'+jsn.get('resultList')[idx].get('stNm')+'역\n'
            res = requests.get(search_by_ars_id_url+'?arsId='+arsId+'&stRttp=2')
            resultList = res.json().get('resultList')
            if resultList is None:
                return 'resultList is None'
            for result_idx in range(len(resultList)):
                result = resultList[result_idx]
                ret += '|-'+result.get('stnNm')+result.get('adirection')+'방면\n|'+result.get('arrmsg1')+'\n|'+result.get('arrmsg2')+'\n'

        return ret

