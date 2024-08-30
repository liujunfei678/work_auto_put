import requests
import re
import time
import json
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def get_pic_path(login_info):
    '''
    获取用户cookie
    :param login_info:登录信息
    :return:图片路径
    '''
    print('正在获取用户cookie...')
    retry=0
    while True:

        url = 'http://wdsj.3enetwork.cn/practice/practice-manage/diaries-student?fInternshipInfoId=b3d8addf72194399b08aaaf17685ef93&fInternshipStudentId=608d714d76cb41c0b715f5724655a0f4&fTemplateBatchInfoId=70169adeec1544bca61be93cfb52aa7b&fIsNeedDiaryReview1=1&fIsNeedDiaryReview2=1&_pageHeader=%E4%B8%93%E4%B8%9A%E5%AE%9E%E4%B9%A0-21%E7%BA%A7&fType=3'

        edge_options = Options()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        edge_options.add_argument(f'user-agent={user_agent}')
        edge_options.add_argument('--headless')
        edge_options.add_argument('--disable-gpu') 
        edge_options.add_argument('--enable-javascript')
        # edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge = webdriver.Chrome(options=edge_options)
        edge.implicitly_wait(10)

        edge.get(url)
        time.sleep(1)
        user_input= edge.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/form/div[3]/div/div[1]/input')
        user_input.send_keys(login_info['username'])

        password_input= edge.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/form/div[4]/div/div/input')
        password_input.send_keys(login_info['password'])

        login_button= edge.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/form/button')
        login_button.click()
        time.sleep(1)
        cookie=edge.get_cookies()
        # print(cookie)
        real_cookie=''
        for i in cookie:
            real_cookie+=i['name']+'='+i['value']+'; '
        print('你的cookie是：',real_cookie)
        if len(cookie)>0:
            return real_cookie
        else:
            retry+=1
            if retry>=3:
                print('获取cookie失败，请手动输入cookie')
                return input('请输入cookie：')
            print('获取cookie失败，正在重试...')
            edge.quit()
            time.sleep(1)




def get_location(address):
    '''
    获取目标地址的经纬度坐标
    adresss:目标地址
    return:目标名字，经纬度坐标
    '''
    print('正在获取经纬度...')
    while True:
        retry=0
        try:
            header={

                'cookie':'search_gray=1; home_gray=1; Hm_lvt_c8ac07c199b1c09a848aaab761f9f909=1724584174; HMACCOUNT=B754010050C7ADED; cna=8v5RH0D6wwACAXPGPXb7MXCq; xlly_s=1; passport_login=Njk1MDE4MTI1LGFtYXBDQWNza2xqWlosZHJxNHcydXlqcndpcHhtendteGUyZ2J5dXc1azVidmksMTcyNDU4NDI2OCxPVGN3Tm1VMFptUTRaRFJpT1dOaU1HTXlaakUzWmpaaU9HRTJNV00wTWpVPQ%3D%3D; oauth_state=a86c496fdc7399eeb6425be8e4425bbc; gray_auth=2; AMAPID=d3df79af1344bb9c0cb03841298726ef; Hm_lpvt_c8ac07c199b1c09a848aaab761f9f909=1724585222; isg=BKys_Lqp5rQX6vKIpjNyhexcfYreZVAP138K8Qbs_Nf6EU0bO3dHnwXnMdmpmYhn; tfstk=fLfjiT1gWmmfSdbWjKUyFTwl0uA1fiNUhVTO-NhqWIdY5d_94rv4nCWWfgIWDfR2gPt92NQVgizDBqf5Afl4m-bt1CRTYkPUTZ4DsCEFmexIomYB5xFwHFnR42dM-kPUTZAi34VYYPjogn-6WCLvBKL8PF8xXCL9DztJ5eDtDGdTPaKk5A3v6fL8weYs6Xy-RFwXmZaRGCXadX5Ak3GCrtLxFHPH2fddZEpf6ZKWzU5WlKtpUDk9zsIPWs5DEJDesaWCfOI8Njs1k9I90_EK1hWH5NLB9W0B2s_1NKXrDxLBGn9dML3EOZvOF_OVMlDhzatvdQWzEoJwGi6HxKeuqG_W0GCXemZyb97PMLsL4bsMCtIXyBIzmX-QUFksPpc6PHz7PADaFs6M9Ej9dEpvrE9zPziAIKLkPHz7PADMHUYX4zaSDOf..',
                'referer':'https://lbs.amap.com/tools/picker',

            }

            parm={
            'platform': 'JS',
            's': 'rsv3',
            'logversion': '2.0',
            'key': 'f7d40927ba4d64fb91ebe2bb9cda0995',
            'sdkversion': '2.0.6.1',
            'appname': 'https%3A%2F%2Flbs.amap.com%2Ftools%2Fpicker',
            'csid': '7A14ACE3-C465-46FA-B27C-27908D5B1E8B',
            'city': '110000',
            'page': '1',
            'offset': '1',
            'extensions': 'all',
            'language': 'zh_cn',
            's': 'rsv3',
            'children': '',
            'type_': 'KEYWORD',
            'antiCrab': 'true',
            'keywords': address,
            'callback': 'jsonp_497439_1724585235974_',
            }

            url='https://lbs.amap.com/AMapService/v3/place/text'

            res=requests.get(url,headers=header,params=parm)
            restext=res.text
            datatxt=re.findall(r'jsonp_\d+_\d+_\((.*?)\)',restext)[0]
            data_json=json.loads(datatxt)
            name=data_json['pois'][0]['name']
            location=data_json['pois'][0]['entr_location']
            print(data_json)
            print(name,location)
            return f'{name},{location}'
        except:
            print('获取经纬度失败，检查输入地址是否有误！')
            time.sleep(1)
            retry+=1
            if retry>=3:
                print('获取经纬度失败(考虑可能cookie过期)，请手动输入经纬度')
                return input('请输入经纬度（如：）：虹软大厦,30.192639,120.206354')
            


'v0.2:增加自动获取cookie功能'
if __name__ == '__main__':
    # 输入用户名、密码、cookie、地址

    print('*'*50)
    print('* 导入你的信息，用于实习日志生成 *')
    print('版本：v0.2')
    print('日期：2024-08-26')
    print('*'*50)
    name=input('请输入你的姓名（实习日志生成使用）：')
    username=input('请输入用户名：')
    password=input('请输入密码：')
    # cookie=input('请输入用户cookie：')
    api_key=input('星火API_KEY：')
    address=input('请输入工作地址：')
    cookie=get_pic_path({'username':username,'password':password})
    location=get_location(address)

    all_dic={
        'name':name,
        'username':username,
        'password':password,
        'cookie':cookie,
        'location':location,
        'api_key':api_key
    }
    with open('user_fixation.json','w',encoding='utf-8') as f:
        json.dump(all_dic,f,indent=4)
    print('信息保存成功！可以正常使用了！请运行主程序！')

