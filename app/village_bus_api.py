import urllib
import requests

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

