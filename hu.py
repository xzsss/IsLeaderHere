import http.client
import requests
import threading
import time
import MySQLdb
def checkGhu(): 
    global isthereGhu 
    nowhour =str(time.strftime("%H", time.localtime()))
    if ( isthereGhu and  nowhour in ['17','18','19','20','21']) or ( not isthereGhu and  nowhour in ['08','09','10','11']):
        insertLog("--",'开始查询',"ghu")
        url = "https://bmeparkapi.capitaland.com.cn/api/park/guest_get_parked_info?mall_id=96&car_no=%E8%8B%8FE88F69&is_test=0&mallId=96&portalId=82"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        datatext = response.text
        if '操作成功' not in datatext:
            insertLog(datatext,'查询失败',"ghu")
            print(datatext)
            exit()
        if '查询到当前车辆的入场信息' in datatext:
            newstatus=False
            message ="%E8%83%A1%E8%80%81%E5%B8%88%E8%B5%B0%E4%BA%86"
        else:
            newstatus= True
            message ="%E8%83%A1%E8%80%81%E5%B8%88%E4%BB%96%E6%9D%A5%E4%BA%86"
        if newstatus!=isthereGhu:
            insertLog(datatext,'状态更新',"ghu")
            conn = http.client.HTTPSConnection("sctapi.ftqq.com")
            payload = ''
            headers = {}
            conn.request("GET", "/SCT102166TzGvZfWHTvJYEsuDyccVlxH5B.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            insertLog(conn,'发送信息1成功',"ghu")
            isthereGhu=newstatus
            insertSQL("ghu",isthereGhu)
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
            conn.request("GET", "/SCT102623TQAVuxokNPcVWKAcHn4k0FW05.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            insertLog(conn,'发送信息2成功',"ghu")
            isthereGhu=newstatus
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
    timer = threading.Timer(300,checkGhu)
    timer.start()

def checkChenn(): 
    global isthereChenn 
    nowhour =str(time.strftime("%H", time.localtime()))
    nowweek =str(time.strftime("%w", time.localtime()))
    if ( nowhour in ['18','19','20']) or (nowweek=="6" and  nowhour in ['09','10','11','12','13','14','15','16','17','18'] ):
        insertLog("--",'开始查询',"chenn")
        url = "https://bmeparkapi.capitaland.com.cn/api/park/guest_get_parked_info?mall_id=96&car_no=%E8%8B%8FEQ377P&is_test=0&mallId=96&portalId=82"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        datatext = response.text
        if '操作成功' not in datatext:
            print(datatext)
            insertLog(datatext,'查询失败',"chenn")
            exit()
        if '查询到当前车辆的入场信息' in datatext:
            newstatus=False
            message ="%E5%A5%B3%E4%B8%8A%E5%8F%B8%E8%B5%B0%E4%BA%86"
        else:
            newstatus= True
            message ="%E5%A5%B3%E4%B8%8A%E5%8F%B8%E6%9D%A5%E4%BA%86"
        if newstatus!=isthereChenn:
            insertLog(datatext,'状态更新',"chenn")
            conn = http.client.HTTPSConnection("sctapi.ftqq.com")
            payload = ''
            headers = {}
            conn.request("GET", "/SCT102166TzGvZfWHTvJYEsuDyccVlxH5B.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            insertLog(datatext,'发送信息1成功',"chenn")
            isthereChenn=newstatus
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
            conn.request("GET", "/SCT102623TQAVuxokNPcVWKAcHn4k0FW05.send?title="+message+"&desp="+message, payload, headers)
            res = conn.getresponse()
            data = res.read()
            insertLog(datatext,'发送信息2成功',"chenn")
            isthereChenn=newstatus
            insertSQL("chenn",isthereChenn)
            if 'SUCCESS' not in data.decode("utf-8"):
                print(data.decode("utf-8"))
                print( time.localtime())
    timer = threading.Timer(650,checkChenn)
    timer.start()

def insertSQL(name,action):
    conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='TEST',charset='utf8')
    cur=conn.cursor()
    cur.execute(" insert into IsLeaderHere(Date,LeaderName,NewAction) values(now(),'"+str(name)+"','"+str(action)+"');")
    conn.commit()
    cur.close()
    conn.close()
def insertLog(log,action,user):
    conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='TEST',charset='utf8')
    cur=conn.cursor()
    cur.execute(" insert into IslLeaderHere_log(time,log,action,user) values(now(),'"+str(log)+"','"+str(action)+"','"+str(user)+"');")
    conn.commit()
    cur.close()
    conn.close()
if __name__ == "__main__":  
    isthereGhu =False
    isthereChenn =False
    insertLog("--","程序开始",'xuz')
    timer = threading.Timer(1,checkGhu)
    timer.start()  
    timer = threading.Timer(5,checkChenn)
    timer.start()           