import requests
import json
import os
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import unquote
import random
import re


# header={

# 'cookie':'Hm_lvt_085e0fa100dbc0e0e42931c16bf3e9e6=1723085957; HMACCOUNT=55597F704F1409F2; _AuthSubAccountSystem=LZCXn3k4UHRvFC1QaP2q2VmhqMAmWbAu0+Y5ev9UKwdCTtzEwNJB7giFOyZBD5118Dt2+qeXse5Z5fHLSVF+Lm+PT83rclII44gHvW4e654=; Hm_lpvt_085e0fa100dbc0e0e42931c16bf3e9e6=1724056764',#个人cookie

# }


### 获取日志相关信息

def get_user_parm(header):
    """
    获取用户参数
    :return:用户参数字典
    """

    url='http://wdsj.3enetwork.cn/api/WDPracticeInternshipPlugin/api/v1/InternshipStudent/GetInternshipStudentWithRelateCountPageListByUser?pageNumber=1&pageSize=10'

    res=requests.get(url,headers=header)

    # print(res.text)
    data=json.loads(res.text)

    user_parm={}
    content_list=data['Content']['List']
    for content in content_list:
        if content['cInternshipName'] == '专业实习-21级':
            print(content['cInternshipName'],content['cRealName'])
            print('fInternshipInfoId:',content['fInternshipInfoId'])
            print('fInternshipStudentId:',content['fInternshipStudentId'])
            print('fTemplateBatchInfoId:',content['fTemplateBatchInfoId'])
            user_parm['fInternshipInfoId']=content['fInternshipInfoId']
            user_parm['fInternshipStudentId']=content['fInternshipStudentId']
            user_parm['fTemplateBatchInfoId']=content['fTemplateBatchInfoId']
            break

    return user_parm



def get_all_diary(header,user_parm):
    """
    获取所有日志信息
    :return:Diary列表
    """

    # header={

    # 'cookie':'Hm_lvt_085e0fa100dbc0e0e42931c16bf3e9e6=1723085957; HMACCOUNT=55597F704F1409F2; _AuthSubAccountSystem=LZCXn3k4UHRvFC1QaP2q2VmhqMAmWbAu0+Y5ev9UKwdCTtzEwNJB7giFOyZBD5118Dt2+qeXse5Z5fHLSVF+Lm+PT83rclII44gHvW4e654=; Hm_lpvt_085e0fa100dbc0e0e42931c16bf3e9e6=1724056764',#个人cookie

    # }

    url='http://wdsj.3enetwork.cn/api/WDPracticeInternshipPlugin/api/v1/InternshipDiary/GetInternshipDiaryPageList'
    parm={
        'fInternshipInfoId': user_parm['fInternshipInfoId'],
        'fInternshipStudentId': user_parm['fInternshipStudentId'],
        'fTemplateBatchInfoId': user_parm['fTemplateBatchInfoId'],
        'fIsNeedDiaryReview1': '1',
        'fIsNeedDiaryReview2': '1',
        '_pageHeader': '专业实习-21级',
        'fType': '3',
        'pageNumber': '1',
        'pageSize': '10'
    }

    response=requests.get(url,headers=header,params=parm)

    data=json.loads(response.text)# print(data)

    diary_list=[]
    data_list=data['Content']['List']
    for item in data_list:
        # print(item)
        dirname=item['cDiaryName']
        id=item['fInternshipDiaryId']
        creat_time=item['tCreateDate']
        diary_list.append([dirname,id,creat_time])
        # print(dirname,id,creat_time)
    return diary_list


def get_diary_detail(id,header):
    '''
    获取日志详情
    :param id:日志id
    :return:日志详情
    '''
    print('正在获取日志详情...')
#     header={

#     'cookie':'Hm_lvt_085e0fa100dbc0e0e42931c16bf3e9e6=1723085957; HMACCOUNT=55597F704F1409F2; _AuthSubAccountSystem=LZCXn3k4UHRvFC1QaP2q2VmhqMAmWbAu0+Y5ev9UKwdCTtzEwNJB7giFOyZBD5118Dt2+qeXse5Z5fHLSVF+Lm+PT83rclII44gHvW4e654=; Hm_lpvt_085e0fa100dbc0e0e42931c16bf3e9e6=1724056764',
# }

    url='http://wdsj.3enetwork.cn/api/WDPracticeInternshipPlugin/api/v1/InternshipDiaryItem/GetInternshipDiaryItemPageList'
    parm={
        'fInternshipDiaryId': id
    }

    response=requests.get(url,params=parm,headers=header)
    diary_dic_detial={}
    data=json.loads(response.text)
    datalist=data['Content']['List']
    for item in datalist:
        name=item['cDiaryItemName']
        id=item['fInternshipDiaryItemId']

        # print(name,id)
        diary_dic_detial[name]=id
    return diary_dic_detial



def write_diary(id,header,user_parm,diary_dic_detial,ai_answer_dic,diary_base_info,img_path):
    '''
    填写日志

    :param id:日志id

    :return:
    '''
#     header={

#     'cookie':'Hm_lvt_085e0fa100dbc0e0e42931c16bf3e9e6=1723085957; HMACCOUNT=55597F704F1409F2; _AuthSubAccountSystem=LZCXn3k4UHRvFC1QaP2q2VmhqMAmWbAu0+Y5ev9UKwdCTtzEwNJB7giFOyZBD5118Dt2+qeXse5Z5fHLSVF+Lm+PT83rclII44gHvW4e654=; Hm_lpvt_085e0fa100dbc0e0e42931c16bf3e9e6=1724056764',

# }

    data={"cDiaryName":diary_base_info[0],
        #   "templateIdFormItemIdMapJSON":"{\"972f3a6fda32442b8aaaca4b84d7df5f\":\"7cb555c6ff964eec93559b330544c0f4\",\"c026f4cbc6be4f679b495107fe4ef503\":\"84fc86c267c44c539e7ee845c3a36ebf\",\"953818a79c5f41bca3df0db444dabb7c\":\"88a3005876844c539143a6cd9fe5fc9b\",\"ebc40620c9dc4575b9192b316813288c\":\"76346d223bab46d7b1cf05bd5c71f02b\",\"4ac401eb11934f89be71129ff017ff23\":\"b0f5edba51c243d8ae162b6912a36ef8\",\"84bf928255f74634bccb39b691149d44\":\"351265fb48ef4a799d0f18c81b0de379\",\"99882750f0c347e19ae4da8bea4a45c0\":\"0323981ce4fd4e8ea222c925bfabbb06\",\"cf365fe1ad5b4d4792c5a8578bbda5ce\":\"80ec214af3694fd0af482fe4ea950d9d\",\"67354e1880574dab8d0bba189e4d9fff\":\"8f8c5cd08ceb42a0aef13d19d6f295d7\",\"e292ff9ce8b54050a8bac3e42d4a160d\":\"2d01669c825d4a6fa50e8c41ecec6966\",\"3de6e7bf3ba842d082df8dcf026e0cbd\":\"6cc56eec0b604d3aba2034f8ec92c66e\",\"8efb68bac013461b8d2f97d2836e6dd5\":\"c8ddef4c100e4740967086084ea83a0e\",\"4dbb1547d8db47fab8db4be0270e5600\":\"c9b1bacd2f2342b6839e627610f83da7\"}",
        "fInternshipStudentId":user_parm['fInternshipStudentId'],
        "fInternshipDiaryId":id,
        "fSubmitType":1,
        "fInternshipInfoId":user_parm['fInternshipInfoId'],
        "fTemplateBatchInfoId":user_parm['fTemplateBatchInfoId'],
        "fIsNeedDiaryReview1":"1",
        "fIsNeedDiaryReview2":"1",
        "fType":"3",
        f"{diary_dic_detial['工作时间']}":f"{diary_base_info[1]} 00:00:00",
        f"{diary_dic_detial['工作地点']}":diary_base_info[2],
        f"{diary_dic_detial['工作任务与内容']}":f"{ai_answer_dic['工作任务与内容']}",
        f"{diary_dic_detial['相关人员']}":f"{ai_answer_dic['相关人员']}",
        f"{diary_dic_detial['工作要点记录']}":f"{ai_answer_dic['工作要点记录']}",
        f"{diary_dic_detial['相关讨论与资料']}":f"{ai_answer_dic['相关讨论与资料']}",
        f"{diary_dic_detial['主要问题']}":f"{ai_answer_dic['主要问题']}",
        f"{diary_dic_detial['下步计划']}":f"{ai_answer_dic['下步计划']}",
        f"{diary_dic_detial['主要风险']}":f"{ai_answer_dic['主要风险']}",
        f"{diary_dic_detial['工作体会']}":f"{ai_answer_dic['工作体会']}",
        f"{diary_dic_detial['实习场景']}":f"oss/default/internship/{img_path}",
        f"{diary_dic_detial['实习场景（多张）']}":"",
        f"{diary_dic_detial['导师建议']}":f"{ai_answer_dic['导师评价和建议']}"}
    url='http://wdsj.3enetwork.cn/api/WDPracticeInternshipPlugin/api/v1/InternshipDiaryItem/EditInternshipDiaryItemList'
    response=requests.post(url,headers=header,json=data)
    print(response.text)
    print(response.status_code)


###大模型回答

def get_answer(content,api):
    '''
    获取ai回答（星火大模型免费版）
    :param content:你的信息
    :return:ai回答
    
    '''
    retry=0
    while True:

        try:

            url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
            data = {
                    "model": "general", # 指定请求的模型
                    "messages": [
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                    
                }
            header = {
                "Authorization": f"Bearer {api}" # 注意此处替换自己的APIPassword
            }
            response = requests.post(url, headers=header, json=data)
            # print(response.text)
            answer=response.json()['choices'][0]['message']['content']
            # print(answer)
            return answer
        except:
            print('获取ai回答失败，请检查网络连接或API密码是否正确')
            retry+=1
            if retry>=3:
                print('获取ai回答失败，请检查网络连接或API密码是否正确')
                return None


def get_all_answer(content,name,api):
    '''
    获取所有信息并回答

    :param content:你的信息
    :return:所有信息的回答
    '''
    print('正在获取所有的信息并ai回答...')
    # content='今天完成了两个脚本需求，和一部分的爬虫内容。\n第一个脚本，从需求分析到脚本开发测试一共花了大概3小时\n第二个脚本，是一个小需求将目标文件夹中的图片筛选并移动。\n爬虫脚本开发部分，目前完成了需求分析，了解了整体的爬取思路；并完成了目标整体商品url的爬取。还缺少商品详细商品图片以及相关推荐爬取。\n体会到了，当一个需求很急切的时候的内心急躁感。'
    # data='工作任务与内容（）;相关人员（）;工作要点记录（）;相关讨论与资料（）;主要问题（）;下步计划（）;主要风险（）;工作体会（）;'
    keyword=['工作任务与内容','相关人员','工作要点记录','相关讨论与资料','主要问题','下步计划','主要风险','工作体会','导师评价和建议']
    value_dict={
        '工作任务与内容':'请你告诉我详细的工作任务与内容，不要分段，一段内容，详细回答',
        '相关人员':f'请你总结出此内容中的相关人员，例如：需求方：xxx，开发人员：{name}，测试人员：{name}。简要回答',
        '工作要点记录':'请你总结一下此段内容的工作要点，分点概况但要求一段话。',
        '相关讨论与资料':'请你告诉一下此段内容所查阅了哪些相关资料，简要回答',
        '主要问题':'请你总结一下此段内容所遇到的主要问题。',
        '下步计划':'请你根据此段内容的工作情况，给出下一步的工作计划。',
        '主要风险':'请你根据此段内容的工作情况，给出此段内容的主要风险。',
        '工作体会':'请你根据此段内容的工作情况，给出此段内容的工作体会。要求400字',
        '导师评价和建议':'你现在作为我的导师的身份，请你对此段内容给出你的导师评价和建议。',
    }
    all_dic={}
    for key in keyword:
        print(f'正在编写{key}的信息...')
        messages =  f'根据以下内容{content}，{value_dict[key]}，只需列出内容，不需要其他信息。'
        answer=get_answer(messages,api)
        all_dic[key]=answer
    return all_dic

### 获取其他相关资料

def get_pic_path(img_path,login_info):
    '''
    图片上传云端oss并获取图片路径
    :param img_path:图片路径
    :param login_info:登录信息
    :return:图片路径
    '''
    print('正在上传图片到oss并获取oss图片路径...')
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

        target_page=edge.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/section/div/div/div/div[2]/div[3]/table/tbody/tr[3]/td[13]/div/a')
        target_page.click()

        first_label=edge.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/section/div/div/div/div/div/div/div[3]/div[3]/table/tbody/tr[1]/td[3]/div/a')
        first_label.click()
        time.sleep(1)
        try:

            delete_label=edge.find_element(By.XPATH, "//span[@class='el-upload-list__item-actions']")
            delete_label.click()
            ActionChains(edge).send_keys(Keys.DELETE).perform()

        except:
            print('no delete label')
        time.sleep(1)
        pic_put=edge.find_element(By.XPATH, "*//div[@class='el-upload el-upload--picture-card']/input")
        pic_put.send_keys(os.path.abspath(img_path))
        time.sleep(3)
        get_pic_path=edge.find_element(By.XPATH, "//ul[@class='el-upload-list el-upload-list--picture-card']//img")
        pic_path=get_pic_path.get_attribute('src')
        # print(pic_path)
        # 获取当前时间戳（以秒为单位）
        img_real_path=pic_path.split('?')[0].split('%2F')[-1]
        # print('oss图片路径:',img_real_path)
        # current_timestamp = time.time()
        # print("当前时间戳（秒）:", current_timestamp)

        edge.quit()
        if '---' in img_real_path:
            print('oss图片路径:',img_real_path)
            break
        else:
            print('上传失败，正在重新上传')
            retry+=1
            if retry>=3:
                print('上传失败，请手动上传实习图片')
                break
            

    return unquote(img_real_path)


def get_random_pic_path(dir_path):
    '''
    一个获取随机图片路径的函数
    :param dir_path:图片文件夹路径
    :return:随机图片路径
    '''
    pic_list=[]
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if os.path.splitext(file)[1] in ['.jpg','.png','.jpeg']:
                pic_list.append(os.path.join(root, file))
    return random.choice(pic_list)


def get_location(address):
    '''
    获取目标地址的经纬度坐标
    adresss:目标地址
    return:目标名字，经纬度坐标
    '''
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
            


if __name__=='__main__':
    print('*'*50)
    print('欢迎使用自动填写日志脚本！')
    print('版本：v0.1 ')
    print('日期:2024/08/26')
    print('*'*50)
    with open('user_fixation.json','r',encoding='utf-8') as f:
        user_fixation=json.load(f)
    
    header={
    'cookie':user_fixation['cookie'],#个人cookie
    }
    user_parm=get_user_parm(header)

    diary_list=get_all_diary(header,user_parm)
    print('\n以下是你的日志列表：')
    print(f'序号 日志名称 日志id 日志创建时间')
    for i,item in enumerate(diary_list):
        print(i,item)
    print('请输入你需要AI写入的日志编号：')
    nun=int(input())
    id=diary_list[nun][1]

    diary_dic_detial=get_diary_detail(id,header)

    # diary_name='曾振铭20240819'
    # work_time='2024/08/19'
    # work_place="虹软大厦,30.192639,120.206354"
    diary_name=input('请输入日志名称（如：刘骏飞20240819）：')
    work_time=input('请输入日志日期（如：2024/08/19）：')
    work_place=user_fixation['location']
    # work_place=get_location(input('请输入日志地址（如：杭州市滨江虹软）：'))
    
    diary_base_info=[diary_name,work_time,work_place]

    content=input('请输入需要填充日志内容：')
    dir_img_path=input('请输入实习图片路径或者图片文件夹路径：')

    ai_answer=get_all_answer(content,user_fixation['name'],api=user_fixation['api_key'])

    login_info={
        # 'username':'15924375282',
        # 'password':'375282',
        'username':user_fixation['username'],
        'password':user_fixation['password'],
    }
    
    if os.path.isdir(dir_img_path):
        print('目标路径为文件夹，随机选择一张图片')
        img_path=get_random_pic_path(dir_img_path)
    else:
        print('目标路径为文件，直接上传')
        img_path=dir_img_path
    img_real_path=get_pic_path(img_path,login_info)

    write_diary(id,header,user_parm,diary_dic_detial,ai_answer,diary_base_info,img_real_path)
    # write_diary(id,diary_dic_detial,ai_answer_dic,diary_name,work_time,work_place,img_path)


    # diary_dic_detial=get_diary_detail(id)
    # write_diary(id,diary_dic_detial)