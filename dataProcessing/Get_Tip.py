import pymysql
from bs4 import BeautifulSoup
import requests
import re
class Get_Tip(object):
    def __init__(self):
        #存储各个专业大类的元组
        self.key = (
            ('电气','电网','自动化'),                                 #0电气及其自动化
            ('机械','车辆','材料成型'),                                         #1机械学院
            ('人工智能','算法','软件','信息安全','数学','物联网'),        #2数计
            ('石油','化工','材料','环保','制药','能源'),                          #3石油化工，化学，材料学院
            ('建筑','土木','房产'),                                             #4建筑+土木
            ('管理','会计','工商','金融','国际经济','外贸','经济'),                       #5经管
            ('生物','制药','食品'),                                             #6生工
            ('外语','翻译','日语','德语'),                                       #7外语
            ('电子','通信','微电子','集成电路','光电','物理','物联网'),           #8物信
            ('矿'),                                                          #9紫金学院
            ('法学','法律')                                                     #10法学院
               )
        self.db = pymysql.connect(host="*******",user="********",password="**********",database="recruitment")
        self.cur= self.db.cursor()       #取信息所用
        self.cur2 = self.db.cursor()     #存信息所用


    def Get_Mes_Status(self,url):      #获取校招项目需要检索的信息
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",'Connection': 'close'}
        html = requests.get(url, headers=headers, timeout=10)
        html.encoding=html.apparent_encoding
        soup = BeautifulSoup(html.text,'html.parser')
        string = soup.get_text()
        string = re.findall(r'(?s)举办.+主办',string)
        if string != []:
            strin = string[0]  #返回str类型
        else:
            strin = 'None'
        return strin


    def Get_Mes_Network(self,url):           #获取网络招生
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",'Connection': 'close'}
        html = requests.get(url, headers=headers, timeout=10)
        html.encoding=html.apparent_encoding
        soup = BeautifulSoup(html.text,'html.parser')
        string = soup.get_text()
        string = re.findall(r'(?s)二、.+三、',string)
        if string != []:
            strin = string[0]
        else:
            strin = 'None'
        return strin


    def Give_Tip(self,string):               #打标签,如果符合某一专业，则在专业前打勾
        back = ''  #返回数据所用
        for major_index in range(0,11):
            for phyrase_index in range(0,len(self.key[major_index])):
                if(self.key[major_index][phyrase_index] in string):
                    back = back + str(1)
                    break
                else:
                    if(phyrase_index == len(self.key[major_index])-1 ):
                        back = back + str(0)
        return back


    def Tip(self):
        sql = "SELECT * FROM rec_info "   #未分类时  #WHERE type0 is Null
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
            ###################
            while(result!=None):
             ####################
                if(result[1]==0):
                    mes = self.Get_Mes_Network(result[2])
                else:
                    mes = self.Get_Mes_Status(result[2])
                tip = self.Give_Tip(mes)
                sql2 = "UPDATE rec_info SET type0='%s',type1='%s',type2='%s',type3='%s',type4='%s',type5='%s',type6='%s',type7='%s',type8='%s',type9='%s',\
                 type10='%s' WHERE url = '%s'"%(tip[0],tip[1],tip[2],tip[3],tip[4],tip[5],tip[6],tip[7],tip[8],tip[9],tip[10],result[2])  #更新数据库
                self.cur2.execute(sql2)
                self.db.commit()
                result = self.cur.fetchone()
        except Exception as e:
            print(e)
            self.db.rollback()

    def __del__(self):
        self.cur.close()
        self.cur2.close()
        self.db.close()
if __name__=='__main__':
    print("程序启动")
    demo = Get_Tip()
    demo.Tip()

