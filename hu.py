import http.client
import requests
import threading
import time
def printHello(): 
    global isthere 
    nowhour =str(time.strftime("%H", time.localtime()))
    if ( isthere and  nowhour in ['17','18','19','20','21']) or ( not isthere and  nowhour in ['08','09','10','11']):
        print(time.localtime())
        url = "https://bmeparkapi.capitaland.com.cn/api/park/guest_get_parked_info?mall_id=96&car_no=%E8%8B%8FE88F69&is_test=0&mallId=96&portalId=82"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        datatext = response.text
        if '操作成功' not in datatext:
            print(datatext)
            exit()
        if '查询到当前车辆的入场信息' in datatext:
            newstatus=False
            message ="%E8%83%A1%E8%80%81%E5%B8%88%E8%B5%B0%E4%BA%86"
        else:
            newstatus= True
            message ="%E8%83%A1%E8%80%81%E5%B8%88%E4%BB%96%E6%9D%A5%E4%BA%86"
        if newstatus!=isthere:
            conn = http.client.HTTPSConnection("sctapi.ftqq.com")
            payload = ''
            headers = {}
            conn.request("GET", "/SCT102166TzGvZfWHTvJYEsuDyccVlxH5B.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            print( time.localtime())
            isthere=newstatus
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
            conn.request("GET", "/SCT102623TQAVuxokNPcVWKAcHn4k0FW05.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            print( time.localtime())
            isthere=newstatus
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
    timer = threading.Timer(300,printHello)
    timer.start()
if __name__ == "__main__":  
    isthere =False
    timer = threading.Timer(1,printHello)
    timer.start()           