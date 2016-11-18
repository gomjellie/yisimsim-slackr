import requests
import urllib

class subway_api:
    """
    ex: http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=13157'
    """
    station_name_url ='http://m.bus.go.kr/mBus/subway/getStatnByNm.bms'
    arrival_info_url = 'http://m.bus.go.kr/mBus/subway/getArvlByInfo.bms'


    def get_station_stat(station_name):
        station_name = urllib.parse.quote(station_name.replace('역', ''))
#숭실대입구역 -> 숭실대입구 로 변환해야 검색됨
#문제점 역삼역 같은경우 역삼역 -> 삼 으로 변환됨...!
        res = requests.get(subway_api.station_name_url + '?' + 'statnNm='+station_name.replace('%','%25'))
        jsn = res.json()

        if res.json().get('resultList') is None:
            return '그런역 없습니다 다른이름으로 검색하세요'
        subway_id = jsn.get('resultList')[0].get('subwayId')
        statn_id = jsn.get('resultList')[0].get('statnId')

        res = requests.get(subway_api.arrival_info_url + '?' +
                'subwayId='+subway_id+'&statnId='+statn_id)
        jsn = res.json()

        ret = jsn.get('resultList2')[0].get('statnNm') + '\n'
        
        for j in range(len(jsn.get('resultList'))):
            ret += '-----------------------\n|'
            ret += jsn.get('resultList')[j].get('trainLineNm') + '\n| '
            ret += jsn.get('resultList')[j].get('arvlMsg2') + '\n|'
            #for k in jsn.get('resultList')[j].keys():
            #	print(k, jsn.get('resultList')[j].get(k))
            #print('-------------------')

        return ret + '-----------------------'

